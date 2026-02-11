import json
import os

import psycopg2
from psycopg2.extras import Json


def get_connection():
    return psycopg2.connect(
        host=os.environ["POSTGRES_HOST"],
        port=os.environ.get("POSTGRES_PORT", 5432),
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )


def _python_type_to_pg(value):
    if isinstance(value, bool):
        return "BOOLEAN"
    if isinstance(value, int):
        return "BIGINT"
    if isinstance(value, float):
        return "DOUBLE PRECISION"
    return "TEXT"


def _extract_scalar_fields(event):
    """Return {field_name: pg_type} for top-level scalar values."""
    fields = {}
    for key, value in event.items():
        if value is None or isinstance(value, (str, int, float, bool)):
            pg_type = "TEXT" if value is None else _python_type_to_pg(value)
            fields[key] = pg_type
    return fields


def ensure_table(conn, table_name, sample_event, match_id):
    scalar_fields = _extract_scalar_fields(sample_event)
    columns = ["id SERIAL PRIMARY KEY", "match_id INTEGER"]
    for col, pg_type in scalar_fields.items():
        safe_col = col.replace('"', '""')
        columns.append(f'"{safe_col}" {pg_type}')
    columns.append("raw_data JSONB")

    ddl = f'CREATE TABLE IF NOT EXISTS "{table_name}" (\n  ' + ",\n  ".join(columns) + "\n);"
    with conn.cursor() as cur:
        cur.execute(ddl)
    conn.commit()
    return list(scalar_fields.keys())


def insert_events(conn, table_name, events, scalar_keys, match_id):
    if not events:
        return 0

    col_names = ["match_id"] + [f'"{k}"' for k in scalar_keys] + ["raw_data"]
    placeholders = ", ".join(["%s"] * len(col_names))
    sql = f'INSERT INTO "{table_name}" ({", ".join(col_names)}) VALUES ({placeholders})'

    rows = []
    for event in events:
        values = [match_id]
        for key in scalar_keys:
            values.append(event.get(key))
        values.append(Json(event))
        rows.append(values)

    with conn.cursor() as cur:
        cur.executemany(sql, rows)
    conn.commit()
    return len(rows)
