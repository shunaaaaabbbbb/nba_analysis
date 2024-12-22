from datetime import timedelta

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from nba_api_utils.player import Player

def _draw_court(ax=None, color='black', lw=2):
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

def plot_shot_chart_of_player(shot_chart_data, player_name, game, date):
    if shot_chart_data is None:
        raise ValueError("Shot chart data is not fetched. Call fetch_shot_chart_data() first.")

    # 成功と失敗のシュート座標
    x_made = shot_chart_data[shot_chart_data['SHOT_MADE_FLAG'] == 1]['LOC_X']
    y_made = shot_chart_data[shot_chart_data['SHOT_MADE_FLAG'] == 1]['LOC_Y']
    x_missed = shot_chart_data[shot_chart_data['SHOT_MADE_FLAG'] == 0]['LOC_X']
    y_missed = shot_chart_data[shot_chart_data['SHOT_MADE_FLAG'] == 0]['LOC_Y']

    # プロットの準備
    fig, ax = plt.subplots(figsize=(12, 11))
    ax.set_facecolor('black')

    # 成功と失敗のシュートをプロット
    ax.scatter(x_made, y_made, c='turquoise', alpha=1, label='Made Shot', s=100)
    ax.scatter(x_missed, y_missed, c='deeppink', alpha=1, label='Missed Shot', s=100)

    # コートを描画
    _draw_court(ax=ax, color='white')

    # 軸の設定
    ax.set_xlim(-250, 250)
    ax.set_ylim(422.5, -47.5)

    # 軸を非表示にする
    ax.set_xticks([])  # x軸の目盛りを非表示
    ax.set_yticks([])  # y軸の目盛りを非表示
    
    # タイトルと凡例
    ax.set_title(f"Shot Chart for {player_name} ({game} : {date + timedelta(days=1)})",  color='black', weight="bold", fontsize=20)
    ax.legend(loc='lower right', fontsize=20)

    # Streamlitで表示
    st.pyplot(fig)

def plot_shot_chart_of_game(shot_chart_data, team_name, game, date):
    if shot_chart_data is None:
        raise ValueError("Shot chart data is not fetched. Call fetch_shot_chart_data() first.")

    # 成功と失敗のシュート座標
    x_made = shot_chart_data[shot_chart_data['SHOT_MADE_FLAG'] == 1]['LOC_X']
    y_made = shot_chart_data[shot_chart_data['SHOT_MADE_FLAG'] == 1]['LOC_Y']
    x_missed = shot_chart_data[shot_chart_data['SHOT_MADE_FLAG'] == 0]['LOC_X']
    y_missed = shot_chart_data[shot_chart_data['SHOT_MADE_FLAG'] == 0]['LOC_Y']

    # プロットの準備
    fig, ax = plt.subplots(figsize=(12, 11))
    ax.set_facecolor('black')

    # 成功と失敗のシュートをプロット
    ax.scatter(x_made, y_made, c='turquoise', alpha=1, label='Made Shot', s=100)
    ax.scatter(x_missed, y_missed, c='deeppink', alpha=1, label='Missed Shot', s=100)

    # コートを描画
    _draw_court(ax=ax, color='white')

    # 軸の設定
    ax.set_xlim(-250, 250)
    ax.set_ylim(422.5, -47.5)

    # 軸を非表示にする
    ax.set_xticks([])  # x軸の目盛りを非表示
    ax.set_yticks([])  # y軸の目盛りを非表示
    
    # タイトルと凡例
    ax.set_title(f"Shot Chart for {team_name} ({game} : {date + timedelta(days=1)})",  color='black', weight="bold", fontsize=20)
    ax.legend(loc='lower right', fontsize=20)

    # Streamlitで表示
    st.pyplot(fig)


def plot_cumulative_points_comparison(player_name1, player_name2, stat_name):
    player1 = Player(player_name1)
    player2 = Player(player_name2)
    
    player_stats1 = player1.get_player_career_stats(player1.id, stat_name)
    player_stats2 = player2.get_player_career_stats(player2.id, stat_name)

    # 累積得点を計算
    player_stats1[f'CUMULATIVE_{stat_name}'] = player_stats1[stat_name].cumsum()
    player_stats2[f'CUMULATIVE_{stat_name}'] = player_stats2[stat_name].cumsum()
    # シーズンをキャリア年数に変換
    max_career_length = max(len(player_stats1), len(player_stats2))
    player_stats1['CAREER_YEAR'] = range(1, len(player_stats1) + 1)
    player_stats2['CAREER_YEAR'] = range(1, len(player_stats2) + 1)

    # 補完処理（短い方をゼロ埋めする）
    if len(player_stats1) < max_career_length:
        filler = max_career_length - len(player_stats1)
        additional_rows = {
            'CAREER_YEAR': range(len(player_stats1) + 1, max_career_length + 1),
            f'CUMULATIVE_{stat_name}': 0 * filler
        }
        player_stats1 = pd.concat([player_stats1, pd.DataFrame(additional_rows)], ignore_index=True)

    if len(player_stats2) < max_career_length:
        filler = max_career_length - len(player_stats2)
        additional_rows = {
            'CAREER_YEAR': range(len(player_stats2) + 1, max_career_length + 1),
            f'CUMULATIVE_{stat_name}': 0 * filler
        }
        player_stats2 = pd.concat([player_stats2, pd.DataFrame(additional_rows)], ignore_index=True)
    
    # プロット
    fig = go.Figure()

    # Player 1: 出場/非出場シーズンを1つのトレースにまとめる
    fig.add_trace(go.Bar(
        x=player_stats1['CAREER_YEAR'],
        y=player_stats1[f'CUMULATIVE_{stat_name}'],
        name=f'{player_name1}',
        marker=dict(
            color='gold',
            line=dict(color='black', width=1),
            opacity=[1.0 if played else 0.7 for played in player_stats1['IS_PLAYED']]
        ),
        hovertemplate='<b>Year: %{x}</b><br>%{y}<br>' +
                      '%{customdata}<extra></extra>',
        customdata=["Played" if played else "Not Played" for played in player_stats1['IS_PLAYED']]
    ))

    # Player 2: 出場/非出場シーズンを1つのトレースにまとめる
    fig.add_trace(go.Bar(
        x=player_stats2['CAREER_YEAR'],
        y=player_stats2[f'CUMULATIVE_{stat_name}'],
        name=f'{player_name2}',
        marker=dict(
            color='blue',
            line=dict(color='black', width=1),
            opacity=[1.0 if played else 0.7 for played in player_stats2['IS_PLAYED']]
        ),
        hovertemplate='<b>Year: %{x}</b><br>%{y}<br>' +
                      '%{customdata}<extra></extra>',
        customdata=["Played" if played else "Not Played" for played in player_stats2['IS_PLAYED']]
    ))

    
    fig.update_layout(
        title=dict(
            text=f'Cumulative {stat_name} Comparison: {player_name1} vs {player_name2}',
            font=dict(size=20, color='black'),
            x=0
        ),
        xaxis=dict(
            title='Career Year',
            titlefont=dict(size=16, color='black'),
            tickfont=dict(size=14, color='black')
        ),
        yaxis=dict(
            title=f'Cumulative {stat_name}',
            titlefont=dict(size=16, color='black'),
            tickfont=dict(size=14, color='black')
        ),
        legend=dict(
            font=dict(size=14),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='black',
            borderwidth=1
        ),
    )

    st.plotly_chart(fig)