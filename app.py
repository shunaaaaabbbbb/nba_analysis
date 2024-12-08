import streamlit as st
from nba_api_utils.input_data import select_player_by_game, select_game
from utils.visualizations import Visualizer
from nba_api_utils.shot_chart import ShotChart
from nba_api_utils.button import ButtonHandler


class NBAAnalyzerApp:
    def __init__(self):
        # Wideモードを有効にし、アプリタイトルを設定
        st.set_page_config(layout="wide")
        st.title("NBAのショットチャートを作ってみよう！")
        button = ButtonHandler()
        self.mode = button.select_mode()

    def run(self):
        # 左右のカラムを作成（1:1の比率）
        left_col, right_col = st.columns([1, 1])

        with left_col:
            # 左側にデータ入力画面
            if self.mode == "プレイヤーのショットチャート":
                self.run_player_analysis(right_col)
            elif self.mode == "チームのショットチャート":
                self.run_game_analysis(right_col)
            else:
                st.error("モードが選択されていません。")

    def run_player_analysis(self, output_col):
        game_id, player_id, season, player_name, game, date = select_player_by_game()
        if game_id:
            # ショットチャートデータを取得
            shot_chart = ShotChart(season)
            shot_chart_data = shot_chart.get_game_shot_data(game_id, player_id)
            # 右側のカラムにグラフを表示
            with output_col:
                visualizer = Visualizer(shot_chart_data, game, date)
                visualizer.plot_shot_chart_of_player(player_name)

    def run_game_analysis(self, output_col):
        game_id, team_id, season, team_name, game, date = select_game()
        if game_id:
            # ショットチャートデータを取得
            shot_chart = ShotChart(season)
            shot_chart_data = shot_chart.get_team_game_shot_data(game_id, team_id)
            # 右側のカラムにグラフを表示
            with output_col:
                visualizer = Visualizer(shot_chart_data, game, date)
                visualizer.plot_shot_chart_of_game(team_name)


if __name__ == "__main__":
    app = NBAAnalyzerApp()
    app.run()
