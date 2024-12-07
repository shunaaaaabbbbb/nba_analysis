import matplotlib.pyplot as plt
import streamlit as st
from datetime import timedelta

class Visualizer:
    def __init__(self, shot_chart_data, game, date):
        self.shot_chart_data = shot_chart_data
        self.game = game
        self.date = date

    @staticmethod
    def draw_court(ax=None, color='black', lw=2):
        from matplotlib.patches import Circle, Rectangle, Arc
        if ax is None:
            ax = plt.gca()

        hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)
        backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)
        paint = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
        free_throw_top = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color)
        free_throw_bottom = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color, linestyle='dashed')
        restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)
        corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
        corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
        three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)

        court_elements = [hoop, backboard, paint, free_throw_top, free_throw_bottom,
                          restricted, corner_three_a, corner_three_b, three_arc]

        for element in court_elements:
            ax.add_patch(element)

    def plot_shot_chart_of_player(self, player_name):
        if self.shot_chart_data is None:
            raise ValueError("Shot chart data is not fetched. Call fetch_shot_chart_data() first.")

        # 成功と失敗のシュート座標
        x_made = self.shot_chart_data[self.shot_chart_data['SHOT_MADE_FLAG'] == 1]['LOC_X']
        y_made = self.shot_chart_data[self.shot_chart_data['SHOT_MADE_FLAG'] == 1]['LOC_Y']
        x_missed = self.shot_chart_data[self.shot_chart_data['SHOT_MADE_FLAG'] == 0]['LOC_X']
        y_missed = self.shot_chart_data[self.shot_chart_data['SHOT_MADE_FLAG'] == 0]['LOC_Y']

        # プロットの準備
        fig, ax = plt.subplots(figsize=(12, 11))
        ax.set_facecolor('black')

        # 成功と失敗のシュートをプロット
        ax.scatter(x_made, y_made, c='turquoise', alpha=1, label='Made Shot', s=100)
        ax.scatter(x_missed, y_missed, c='deeppink', alpha=1, label='Missed Shot', s=100)

        # コートを描画
        self.draw_court(ax=ax, color='white')

        # 軸の設定
        ax.set_xlim(-250, 250)
        ax.set_ylim(422.5, -47.5)

        # 軸を非表示にする
        ax.set_xticks([])  # x軸の目盛りを非表示
        ax.set_yticks([])  # y軸の目盛りを非表示
        
        # タイトルと凡例
        ax.set_title(f"Shot Chart for {player_name} ({self.game} : {self.date + timedelta(days=1)})",  color='black', weight = "bold", fontsize = 20)
        ax.legend(loc='lower right', fontsize = 20)

        # Streamlitで表示
        st.pyplot(fig)

    def plot_shot_chart_of_game(self, team_name):
        if self.shot_chart_data is None:
            raise ValueError("Shot chart data is not fetched. Call fetch_shot_chart_data() first.")

        # 成功と失敗のシュート座標
        x_made = self.shot_chart_data[self.shot_chart_data['SHOT_MADE_FLAG'] == 1]['LOC_X']
        y_made = self.shot_chart_data[self.shot_chart_data['SHOT_MADE_FLAG'] == 1]['LOC_Y']
        x_missed = self.shot_chart_data[self.shot_chart_data['SHOT_MADE_FLAG'] == 0]['LOC_X']
        y_missed = self.shot_chart_data[self.shot_chart_data['SHOT_MADE_FLAG'] == 0]['LOC_Y']

        # プロットの準備
        fig, ax = plt.subplots(figsize=(12, 11))
        ax.set_facecolor('black')

        # 成功と失敗のシュートをプロット
        ax.scatter(x_made, y_made, c='turquoise', alpha=1, label='Made Shot', s=100)
        ax.scatter(x_missed, y_missed, c='deeppink', alpha=1, label='Missed Shot', s=100)

        # コートを描画
        self.draw_court(ax=ax, color='white')

        # 軸の設定
        ax.set_xlim(-250, 250)
        ax.set_ylim(422.5, -47.5)

        # 軸を非表示にする
        ax.set_xticks([])  # x軸の目盛りを非表示
        ax.set_yticks([])  # y軸の目盛りを非表示
        
        # タイトルと凡例
        ax.set_title(f"Shot Chart for {team_name} ({self.game} : {self.date + timedelta(days=1)})",  color='black', weight = "bold", fontsize = 20)
        ax.legend(loc='lower right', fontsize = 20)

        # Streamlitで表示
        st.pyplot(fig)
