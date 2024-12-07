from nba_api_utils.player import Player
from nba_api_utils.game import Game
from nba_api_utils.team import Team
import streamlit as st
from datetime import timedelta

def input_season_and_date():
    # シーズンと日付の入力
    season = st.text_input("Enter Season (e.g., 2023-24):", "")
    if not season:
        st.stop()

    date = st.date_input("Enter Game Date (YYYY-MM-DD):")
    if not date:
        st.stop()
    date = date - timedelta(days=1)  # Adjust date to the day before
    formatted_date = date.strftime("%Y-%m-%d")

    return season, formatted_date, date

def select_game_from_date(season, formatted_date):
    # 試合情報の取得
    game = Game(season, formatted_date)
    games_on_date = game.game_log

    if games_on_date.empty:
        st.warning("No games found for the given date.")
        st.stop()

    # 試合選択
    game_options = {row["MATCHUP"]: row["GAME_ID"] for _, row in games_on_date.iterrows()}
    filtered_keys = [key for key in game_options.keys() if "vs" in key]
    selected_game = st.selectbox("Select a game:", filtered_keys)
    if not selected_game:
        st.stop()

    return game, game_options[selected_game], selected_game

def select_team_and_player(game, game_id):
    # チーム選択
    teams = game.get_teams(game_id)
    selected_team = st.selectbox("Select a team:", teams)
    if not selected_team:
        st.stop()

    # プレイヤー選択
    players_on_team = game.get_player_names(game_id, selected_team)
    selected_player_name = st.selectbox("Select a player:", players_on_team)
    if not selected_player_name:
        st.stop()

    return selected_team, selected_player_name

def select_player_by_game():
    season, formatted_date, date = input_season_and_date()
    game, game_id, selected_game = select_game_from_date(season, formatted_date)
    selected_team, selected_player_name = select_team_and_player(game, game_id)

    player = Player(selected_player_name)

    return game_id, player.id, season, selected_player_name, selected_game, date

def select_game():
    season, formatted_date, date = input_season_and_date()
    game, game_id, selected_game = select_game_from_date(season, formatted_date)

    # チーム選択
    teams = game.get_teams(game_id)
    selected_team = st.selectbox("Select a team:", teams)
    if not selected_team:
        st.stop()

    team = Team(selected_team)

    return game_id, team.id, season, selected_team, selected_game, date
