# %%
import streamlit as st
from nba_api_utils.input_data import select_player_by_game, select_game
from utils.visualizations import Visualizer
from nba_api_utils.shot_chart import ShotChart
from nba_api_utils.button import ButtonHandler

# %%
def select_mode():
    """
    ボタンを使用してモードを選択する。
    """
    button = ButtonHandler()
    mode = button.select_mode()
    return mode
# %%
def run_player_analysis(output_col):
    """
    プレイヤー単位のショットチャート分析。
    """
    game_id, player_id, season, player_name, game, date = select_player_by_game()
    if game_id:
        shot_chart = ShotChart(season)
        shot_chart_data = shot_chart.get_game_shot_data(game_id, player_id)
        with output_col:
            visualizer = Visualizer(shot_chart_data, game, date)
            visualizer.plot_shot_chart_of_player(player_name)
# %%
def run_game_analysis(output_col):
    """
    チーム単位のショットチャート分析。
    """
    game_id, team_id, season, team_name, game, date = select_game()
    if game_id:
        shot_chart = ShotChart(season)
        shot_chart_data = shot_chart.get_team_game_shot_data(game_id, team_id)
        with output_col:
            visualizer = Visualizer(shot_chart_data, game, date)
            visualizer.plot_shot_chart_of_game(team_name)
# %%
def run():
    """
    アプリケーションのエントリーポイント。
    """
    st.title("NBAのショットチャートを作ってみよう！")
    # 左右のカラムを作成（1:1の比率）
    left_col, right_col = st.columns([1, 1])
    with left_col:
        mode = select_mode()
        if mode == "プレイヤーのショットチャート":
            run_player_analysis(right_col)
        elif mode == "チームのショットチャート":
            run_game_analysis(right_col)
        else:
            st.error("モードが選択されていません。")
