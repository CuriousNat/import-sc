# SkillCorner Import Tool

A CLI tool for fetching soccer/football data from the SkillCorner API.

## Prerequisites

- Python 3.x
- SkillCorner account with API access

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your SkillCorner credentials:
   ```
   SKILLCORNER_USERNAME=your_username
   SKILLCORNER_PASSWORD=your_password
   ```

## Usage

### Fetch Match Events

Download dynamic events for a match:

```bash
python main.py match-events <match_id> [--output db|csv]
```

Options:
- `--output db` (default) - Save to database (not yet implemented)
- `--output csv` - Save to CSV file in `outputs/` folder

Examples:
```bash
# Save to database (default)
python main.py match-events 2016339

# Save to CSV
python main.py match-events 2016339 --output csv
```

CSV files are saved to `outputs/<match_id>_events.csv`.

### Other Commands

The following commands are available but not yet implemented:

```bash
# List all competitions
python main.py competitions

# Get matches in a competition season
python main.py matches-in-comp-season <competition_id> <season_id>

# Get teams in a competition
python main.py teams-in-competition <competition_id>

# Get players in a match
python main.py players-in-match <match_id>
```

## Help

View all available commands:

```bash
python main.py --help
```

View help for a specific command:

```bash
python main.py match-events --help
```
