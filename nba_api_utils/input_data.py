from nba_api_utils.player import Player
from nba_api_utils.game import Game
import streamlit as st

def select_player_by_game():
    # シーズンと日付の入力
    season = st.text_input("Enter Season (e.g., 2023-24):", "")
    if not season:
        st.stop()

    date = st.date_input("Enter Game Date (YYYY-MM-DD):")
    if not date:
        st.stop()
    formatted_date = date.strftime("%Y-%m-%d")

    # 試合情報の取得
    game = Game(season, formatted_date)
    games_on_date = game.game_log

    if games_on_date.empty:
        st.warning("No games found for the given date.")
        st.stop()

    # 試合選択
    game_options = {row["MATCHUP"]: row["GAME_ID"] for _, row in games_on_date.iterrows()}
    # "vs" を含むキーだけを抽出
    filtered_keys = [key for key in game_options.keys() if "vs" in key]
    selected_game = st.selectbox("Select a game:", filtered_keys)
    if not selected_game:
        st.stop()

    game_id = game_options[selected_game]

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

    player = Player(selected_player_name)
    
    return game_id, player.id, season
