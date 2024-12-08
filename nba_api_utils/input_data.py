from nba_api_utils.player import Player
from nba_api_utils.game import Game
from nba_api_utils.team import Team
import streamlit as st
from datetime import timedelta

def input_season():
    # シーズンの入力
    season = st.text_input("シーズンを選択する (e.g., 2023-24):", "")
    if not season:
        st.stop()

    return season

def input_date():
    # 日付の入力
    date = st.date_input("日付を選択する (YYYY-MM-DD):")
    if not date:
        st.stop()
    date = date - timedelta(days=1)  # Adjust date to the day before
    formatted_date = date.strftime("%Y-%m-%d")

    return formatted_date, date

def select_game_from_date(season, formatted_date):
    # 試合情報の取得
    game = Game(season, formatted_date)
    games_on_date = game.game_log

    if games_on_date.empty:
        st.warning(f"{formatted_date}に行われた試合のデータは存在しません。")
        st.stop()

    # 試合選択
    game_options = {row["MATCHUP"]: row["GAME_ID"] for _, row in games_on_date.iterrows()}
    filtered_keys = [key for key in game_options.keys() if "vs" in key]
    selected_game = st.selectbox("試合を選択する:", filtered_keys)
    if not selected_game:
        st.stop()

    return game, game_options[selected_game], selected_game

def select_team(game, game_id):
    # チーム選択
    teams = game.get_teams(game_id)
    selected_team = st.selectbox("Select a team:", teams)
    if not selected_team:
        st.stop()

    return selected_team

def select_player(game, game_id, selected_team):
    # プレイヤー選択
    players_on_team = game.get_player_names(game_id, selected_team)
    selected_player_name = st.selectbox("Select a player:", players_on_team)
    if not selected_player_name:
        st.stop()

    return selected_player_name

def select_player_by_game():
    season = input_season()
    formatted_date, date = input_date()
    game, game_id, selected_game = select_game_from_date(season, formatted_date)
    selected_team = select_team(game, game_id)
    selected_player_name = select_player(game, game_id, selected_team)

    player = Player(selected_player_name)

    return game_id, player.id, season, selected_player_name, selected_game, date

def select_game():
    season = input_season()
    formatted_date, date = input_date()
    game, game_id, selected_game = select_game_from_date(season, formatted_date)
    selected_team = select_team(game, game_id)

    team = Team(selected_team)

    return game_id, team.id, season, selected_team, selected_game, date
