import datetime
from datetime import timedelta

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from nba_api_utils.player import Player
from nba_api_utils.game import Game

from utils.helpers import get_player_stats, prepare_cumlative_stats, fill_missing_career_years

def _draw_court(ax=None, color: str='black', lw: int=2):
    """バスケットコートを描画する

    Args:
        ax (_type_, optional): Matplotlibの軸オブジェクト. Defaults to None.
        color (str, optional): コートの線の色. Defaults to 'black'.
        lw (int, optional): コートの線の太さ. Defaults to 2.
    """
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


def plot_cumulative_comparison(player1: Player, player2: Player, stat_name: str, color1: str, color2: str):
    """2選手の累積スタッツを比較するグラフを描画"""

    # データ取得
    player_stats1 = get_player_stats(player1)
    player_stats2 = get_player_stats(player2)

    # 累積スタッツを計算
    player_stats1 = prepare_cumlative_stats(player_stats1, stat_name)
    player_stats2 = prepare_cumlative_stats(player_stats2, stat_name)

    # キャリアが短い方をゼロ埋め
    player_stats1, player_stats2 = fill_missing_career_years(player_stats1, player_stats2, stat_name)

    # プロット
    fig = go.Figure()

    for stats, player, color in [(player_stats1, player1, color1), (player_stats2, player2, color2)]:
        fig.add_trace(go.Bar(
            x=stats['CAREER_YEAR'],
            y=stats[f'CUMULATIVE_{stat_name}'],
            name=player.name,
            marker=dict(
                color=color,
                line=dict(color='black', width=1),
                opacity=[1.0 if played else 0.7 for played in stats['IS_PLAYED']]
            ),
            hovertemplate='<b>Year: %{x}</b><br>%{y}<br>%{customdata}<extra></extra>',
            customdata=["✔ Played" if played else "✖ Not Played" for played in stats['IS_PLAYED']]
        ))

    fig.update_layout(
        title=dict(text=f'Cumulative {stat_name} Comparison: {player1.name} vs {player2.name}', font=dict(size=20, color='black')),
        xaxis=dict(title='Career Year', titlefont=dict(size=16, color='black'), tickfont=dict(size=14, color='black')),
        yaxis=dict(title=f'Cumulative {stat_name}', titlefont=dict(size=16, color='black'), tickfont=dict(size=14, color='black')),
        legend=dict(font=dict(size=14), bgcolor='rgba(255,255,255,0.8)', bordercolor='black', borderwidth=1),
    )

    st.plotly_chart(fig)



def show_donuts_chart(stat, name, color):
    fig = go.Figure(data=[go.Pie(
        labels=['成功', '失敗'],
        values=[stat, 100 - stat],
        hole=0.6,
        marker=dict(colors=[color, 'rgba(220, 220, 220, 0.5)']),
        textinfo="none",
        rotation=360 * stat * 0.01 if stat < 50 else 0
    )])
    fig.update_layout(
        showlegend=False,
        template="plotly_dark",
        annotations=[
            dict(
                text=f"{stat:.1f}%", x=0.5, y=0.5,
                font=dict(size=40, color="black", family="Arial Black"), showarrow=False
                ),
            dict(
                text=name, x=0.05, y=0.95,
                font=dict(size=40, color=color, family="Arial Black"), showarrow=False
                ),
        ],
        width=500,
        height=500,
    )
    st.plotly_chart(fig, use_container_width=True)


def show_stats(stat, name, color):
    if name == "GAME PLAYED":
        st.markdown(
            f'<div style="border: 4px solid {color}; padding: 15px; border-radius: 30px; background-color: #f9f9f9; text-align: center;">'
            f'<h1 style="font-size: 50px; margin: 0; color: black;">{name}</h1>'
            f'<h1 style="font-size: 50px; margin: 0; color: black;">{stat:.0f}</h1></div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div style="border: 4px solid {color}; padding: 15px; border-radius: 30px; background-color: #f9f9f9; text-align: center;">'
            f'<h1 style="font-size: 50px; margin: 0; color: black;">{name}</h1>'
            f'<h1 style="font-size: 50px; margin: 0; color: black;">{stat:.1f}</h1></div>',
            unsafe_allow_html=True
        )