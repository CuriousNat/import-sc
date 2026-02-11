import argparse
import json
import sys

from dotenv import load_dotenv
import os

from skillcorner.client import SkillcornerClient


def get_client():
    return SkillcornerClient(
        username=os.environ["SKILLCORNER_USERNAME"],
        password=os.environ["SKILLCORNER_PASSWORD"],
    )


def get_match_events(client, match_id, output="db"):
    print(f"Fetching dynamic events for match {match_id}...")
    if output == "csv":
        os.makedirs("outputs", exist_ok=True)
        filepath = f"outputs/{match_id}_events.csv"
        if os.path.exists(filepath):
            os.remove(filepath)
        client.save_dynamic_events(match_id, params={'file_format': 'csv'}, filepath=filepath)
        print(f"Saved to {filepath}")
    else:
        print("Placeholder: save to database")


def get_competitions(client):
    print("Placeholder: get_competitions")


def get_matches_in_comp_season(client, competition_id, season_id):
    print(f"Placeholder: get_matches_in_comp_season(competition_id={competition_id}, season_id={season_id})")


def get_teams_in_competition(client, competition_id):
    print(f"Placeholder: get_teams_in_competition(competition_id={competition_id})")


def get_players_in_match(client, match_id):
    print(f"Placeholder: get_players_in_match(match_id={match_id})")


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Fetch data from SkillCorner")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # match-events
    p_events = subparsers.add_parser("match-events", help="Get dynamic events for a match")
    p_events.add_argument("match_id", type=int, help="SkillCorner match ID")
    p_events.add_argument("--output", choices=["db", "csv"], default="db", help="Output destination (default: db)")

    # competitions
    subparsers.add_parser("competitions", help="Get all competitions")

    # matches-in-comp-season
    p_matches = subparsers.add_parser("matches-in-comp-season", help="Get matches in a competition season")
    p_matches.add_argument("competition_id", type=int, help="Competition ID")
    p_matches.add_argument("season_id", type=int, help="Season ID")

    # teams-in-competition
    p_teams = subparsers.add_parser("teams-in-competition", help="Get teams in a competition")
    p_teams.add_argument("competition_id", type=int, help="Competition ID")

    # players-in-match
    p_players = subparsers.add_parser("players-in-match", help="Get players in a match")
    p_players.add_argument("match_id", type=int, help="Match ID")

    args = parser.parse_args()
    client = get_client()

    if args.command == "match-events":
        get_match_events(client, args.match_id, args.output)
    elif args.command == "competitions":
        get_competitions(client)
    elif args.command == "matches-in-comp-season":
        get_matches_in_comp_season(client, args.competition_id, args.season_id)
    elif args.command == "teams-in-competition":
        get_teams_in_competition(client, args.competition_id)
    elif args.command == "players-in-match":
        get_players_in_match(client, args.match_id)


if __name__ == "__main__":
    main()
