import matplotlib.pyplot as plt
from nba_api.stats.endpoints import shotchartdetail
import streamlit as st

class Visualizer:
    def __init__(self, game_id, player_id, season):
        self.player_id = player_id
        self.game_id = game_id
        self.season = season
        self.shot_chart_data = None

    def fetch_shot_chart_data(self):
        response = shotchartdetail.ShotChartDetail(
            team_id=0,
            player_id=self.player_id,
            season_nullable=self.season,
            game_id_nullable=self.game_id,
            context_measure_simple='FGA'
        )
        self.shot_chart_data = response.get_data_frames()[0]
        st.write(self.shot_chart_data)

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

    def plot_shot_chart(self):
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

        # タイトルと凡例
        ax.set_title(f"Shot Chart for Player ID: {self.player_id} in Game ID: {self.game_id}", color='white')
        ax.legend(loc='upper right')
        ax.set_xlabel("Court X-Coordinate", color='white')
        ax.set_ylabel("Court Y-Coordinate", color='white')
        ax.tick_params(colors='white')  # 軸のラベル色を白に設定

        # Streamlitで表示
        st.pyplot(fig)


