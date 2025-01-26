import streamlit as st
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats, playerdashboardbyyearoveryear
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
        # Player Dashboardを取得
        dashboard = playerdashboardbyyearoveryear.PlayerDashboardByYearOverYear(player_id=player['id'])
        data = dashboard.get_data_frames()[1]  # 高度なスタッツ（Advanced Stats）データフレーム

        stats_df = career_stats.get_data_frames()[0]
        st.write(data)
        st.write(stats_df)
        # データフレームを整形
        stat_df = stats_df.rename(columns={
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
        #display_columns = ['シーズン', '得点', 'アシスト', 'リバウンド', 'スティール', 'ブロック', '試合数', 'FG%', '3P%', 'FT%']
        #stats_df = stats_df[display_columns]

        # 指定されたシーズンのデータを取得
        selected_season = stats_df[stats_df['SEASON_ID'] == season]

        if selected_season.empty:
            st.error(f"{season} シーズンのデータが見つかりません。")
            return

        # スタッツを取得
        fg_pct = selected_season.iloc[0]['FG_PCT'] * 100
        fg3_pct = selected_season.iloc[0]['FG3_PCT'] * 100
        ft_pct = selected_season.iloc[0]['FT_PCT'] * 100
        fgm = selected_season.iloc[0]['FGM']
        fg3m = selected_season.iloc[0]['FG3M']
        ftm = selected_season.iloc[0]['FTM']

        # 3つのカラムを作成
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])  # 比率を1:1:1:2に設定

        # ドーナツグラフ1: FG%
        with col1:
            st.metric(label="Field Goal Made",value=fgm, delta="+2.0%")

            fig_fg = go.Figure(data=[go.Pie(
                labels=['成功', '失敗'],
                values=[fg_pct, 100 - fg_pct],
                hole=0.6,
                marker=dict(colors=['rgba(30, 144, 255, 0.7)', 'rgba(220, 220, 220, 0.5)']),
                textinfo = "none",
                rotation = 360 * fg_pct * 0.01 if fg_pct < 50 else 0
            )])
            fig_fg.update_layout(
                showlegend=False,
                template="plotly_dark",
                annotations=
                [
                dict(
                    text=f"{fg_pct:.1f}%", x=0.5, y=0.5,
                    font=dict(size=40, color="black", family="Arial Black"), showarrow=False
                ),
                # 縁取りの黒テキスト（少し大きいサイズ）
                dict(
                    text="FG%", x=0.06, y=0.94,  # 左上の位置
                    font=dict(size=40, color="black", family="Arial Black"), showarrow=False
                ),
                # 本来のテキスト（上に重ねる）
                dict(
                    text="FG%", x=0.05, y=0.95,  # 左上の位置
                    font=dict(size=40, color="rgba(30, 144, 255,1)", family="Arial Black"), showarrow=False
                ),
                ],
                width=400,  # グラフの幅を指定
                height=400,  # グラフの高さを指定
            )
            st.plotly_chart(fig_fg, use_container_width=True)

        # ドーナツグラフ2: 3P%
        with col2:
            st.metric(label="Three Point Made",value=fg3m, delta="+2.0%")
            
            fig_3p = go.Figure(data=[go.Pie(
                labels=['成功', '失敗'],
                values=[fg3_pct, 100 - fg3_pct],
                hole=0.6,
                marker=dict(colors=['rgba(30, 144, 255, 0.7)','rgba(220, 220, 220, 0.5)']),
                textinfo = "none",
                rotation = 360 * fg3_pct * 0.01 if fg3_pct < 50 else 0
            )])
            fig_3p.update_layout(
                showlegend=False,
                template="plotly_dark",
                annotations=
                [
                dict(
                    text=f"{fg3_pct:.1f}%", x=0.5, y=0.5,
                    font=dict(size=40, color="black", family="Arial Black"), showarrow=False
                ),
                # 縁取りの黒テキスト（少し大きいサイズ）
                dict(
                    text="3P%", x=0.06, y=0.94,  # 左上の位置
                    font=dict(size=40, color="black", family="Arial Black"), showarrow=False
                ),
                # 本来のテキスト（上に重ねる）
                dict(
                    text="3P%", x=0.05, y=0.95,  # 左上の位置
                    font=dict(size=40, color="rgba(30, 144, 255,1)", family="Arial Black"), showarrow=False
                ),
                ],
                width=400,  # グラフの幅を指定
                height=400,  # グラフの高さを指定
            )
            st.plotly_chart(fig_3p, use_container_width=True)

        # ドーナツグラフ3: FT%
        with col3:
            st.metric(label="Free Throw Made",value=ftm, delta="+2.0%")
            
            fig_ft = go.Figure(data=[go.Pie(
                labels=['成功', '失敗'],
                values=[ft_pct, 100 - ft_pct],
                hole=0.6,
                marker=dict(colors=['rgba(30, 144, 255, 0.7)', 'rgba(220, 220, 220, 0.5)']),
                textinfo = "none",
                rotation = 360 * ft_pct * 0.01 if ft_pct < 50 else 0
            )])
            fig_ft.update_layout(
                showlegend=False,
                template="plotly_dark",
                annotations=
                [
                dict(
                    text=f"{ft_pct:.1f}%", x=0.5, y=0.5,
                    font=dict(size=40, color="black", family="Arial Black"), showarrow=False
                ),
                # 縁取りの黒テキスト（少し大きいサイズ）
                dict(
                    text="FT%", x=0.06, y=0.94,  # 左上の位置
                    font=dict(size=40, color="black", family="Arial Black"), showarrow=False
                ),
                # 本来のテキスト（上に重ねる）
                dict(
                    text="FT%", x=0.05, y=0.95,  # 左上の位置
                    font=dict(size=40, color="rgba(30, 144, 255,1)", family="Arial Black"), showarrow=False
                ),
                ],
                width=400,  # グラフの幅を指定
                height=400,  # グラフの高さを指定
            )
            st.plotly_chart(fig_ft, use_container_width=True)

        # データ全体をテーブルで表示
        st.subheader("詳細なスタッツデータ")
        st.dataframe(stats_df, use_container_width=True)
