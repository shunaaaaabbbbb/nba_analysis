import streamlit as st
from nba_api_utils.input_data import select_player_by_game
from utils.visualizations import Visualizer

st.title("NBA Game and Player Analyzer")

# プレイヤー選択フロー
game_id, player_id, season = select_player_by_game()

# 選択結果の表示
if game_id:
    visualizer = Visualizer(player_id, game_id, season)
    visualizer.fetch_shot_chart_data()
    visualizer.plot_shot_chart()
