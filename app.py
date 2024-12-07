import streamlit as st
from nba_api_utils.input_data import select_player_by_game, select_game
from utils.visualizations import Visualizer
from nba_api_utils.shot_chart import ShotChart
from nba_api_utils.button import ButtonHandler

st.title("NBA Game and Player Analyzer")

# ボタンを利用してモードを選択
mode = ButtonHandler.select_mode()

if mode == "プレイヤー単位":
    game_id, player_id, season, player_name, game, date = select_player_by_game()
    if game_id:
        shot_chart = ShotChart(season)
        shot_chart_data = shot_chart.get_game_shot_data(game_id, player_id)
        visualizer = Visualizer(shot_chart_data, game, date)
        visualizer.plot_shot_chart_of_player(player_name)
elif mode == "試合単位":
    game_id, team_id, season, team_name, game, date = select_game()
    if game_id:
        shot_chart = ShotChart(season)
        shot_chart_data = shot_chart.get_team_game_shot_data(game_id, team_id)
        visualizer = Visualizer(shot_chart_data, game, date)
        visualizer.plot_shot_chart_of_game(team_name)
