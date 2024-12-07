import streamlit as st
from nba_api_utils.input_data import select_player_by_game
from utils.visualizations import Visualizer
from nba_api_utils.shot_chart import ShotChart

st.title("NBA Game and Player Analyzer")

# プレイヤー選択フロー
game_id, player_id, season, player_name, game, date = select_player_by_game()

# 選択結果の表示
if game_id:
    
    shot_chart = ShotChart(player_id, season)
    shot_chart_data = shot_chart.get_game_shot_data(game_id)
    visualizer = Visualizer(game_id, player_id, season, player_name, shot_chart_data, game, date)
    visualizer.plot_shot_chart()
