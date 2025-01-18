import streamlit as st
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import pandas as pd
import plotly.graph_objects as go

def run():
    # ページタイトル
    st.title("NBA 選手シーズンスタッツ表示")
    st.markdown("選手を選択して、シーズンスタッツを確認しましょう。")

    # 選手名とシーズンの入力
    player_name = st.text_input("選手名を入力してください（例: LeBron James）", "LeBron James")
    season = st.text_input("シーズンを入力してください（例: 2024-25）", "2024-25")

    if player_name and season:
        # 選手IDを取得
        player_list = players.get_players()
        player = next((p for p in player_list if p['full_name'].lower() == player_name.lower()), None)

        if not player:
            st.error("該当する選手が見つかりません。名前を確認してください。")
            return

        # 選手のキャリアスタッツを取得
        career_stats = playercareerstats.PlayerCareerStats(player_id=player['id'])
        stats_df = career_stats.get_data_frames()[0]

        # データフレームを整形
        stats_df = stats_df.rename(columns={
            'SEASON_ID': 'シーズン',
            'PTS': '得点',
            'AST': 'アシスト',
            'REB': 'リバウンド',
            'STL': 'スティール',
            'BLK': 'ブロック',
            'GP': '試合数',
            'MIN': 'プレイ時間',
            'FG_PCT': 'FG%',
            'FG3_PCT': '3P%',
            'FT_PCT': 'FT%',
        })

        # 必要な列を選択
        display_columns = ['シーズン', '得点', 'アシスト', 'リバウンド', 'スティール', 'ブロック', '試合数', 'FG%', '3P%', 'FT%']
        stats_df = stats_df[display_columns]

        # 指定されたシーズンのデータを取得
        selected_season = stats_df[stats_df['シーズン'] == season]

        if selected_season.empty:
            st.error(f"{season} シーズンのデータが見つかりません。")
            return

        # スタッツを取得
        fg_pct = selected_season.iloc[0]['FG%'] * 100
        fg3_pct = selected_season.iloc[0]['3P%'] * 100
        ft_pct = selected_season.iloc[0]['FT%'] * 100

        # 3つのカラムを作成
        col1, col2, col3, col4 = st.columns(4)

        # ドーナツグラフ1: FG%
        with col1:
            fig_fg = go.Figure(data=[go.Pie(
                labels=['成功', '失敗'],
                values=[fg_pct, 100 - fg_pct],
                hole=0.3,
                marker=dict(colors=['rgba(135, 206, 250, 0.7)', 'rgba(220, 220, 220, 0.5)'])
            )])
            fig_fg.update_layout(
                showlegend=False,
                template="plotly_dark",
                annotations=[dict(
                    text=f"FG%", x=0.5, y=0.5,
                    font=dict(size=20, color="black", family="Arial Black"), showarrow=False
                )]
            )
            st.plotly_chart(fig_fg, use_container_width=True)

        # ドーナツグラフ2: 3P%
        with col2:
            fig_3p = go.Figure(data=[go.Pie(
                labels=['成功', '失敗'],
                values=[fg3_pct, 100 - fg3_pct],
                hole=0.3,
                marker=dict(colors=['rgba(30, 144, 255, 0.7)', 'rgba(220, 220, 220, 0.5)'])
            )])
            fig_3p.update_layout(
                showlegend=False,
                template="plotly_dark",
                annotations=[dict(
                    text=f"3P%", x=0.5, y=0.5,
                    font=dict(size=20, color="black", family="Arial Black"), showarrow=False
                )]
            )
            st.plotly_chart(fig_3p, use_container_width=True)

        # ドーナツグラフ3: FT%
        with col3:
            fig_ft = go.Figure(data=[go.Pie(
                labels=['成功', '失敗'],
                values=[ft_pct, 100 - ft_pct],
                hole=0.3,
                marker=dict(colors=['rgba(0, 191, 255, 0.7)', 'rgba(220, 220, 220, 0.5)'])
            )])
            fig_ft.update_layout(
                showlegend=False,
                template="plotly_dark",
                annotations=[dict(
                    text=f"FT%", x=0.5, y=0.5,
                    font=dict(size=20, color="black", family="Arial Black"), showarrow=False
                )]
            )
            st.plotly_chart(fig_ft, use_container_width=True)

        # データ全体をテーブルで表示
        st.subheader("詳細なスタッツデータ")
        st.dataframe(stats_df, use_container_width=True)
