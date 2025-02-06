import streamlit as st
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats, playerdashboardbyyearoveryear
import plotly.graph_objects as go

def show_donuts_chart(stat, name):
    # ドーナツグラフ3: FT%
    fig = go.Figure(data=[go.Pie(
        labels=['成功', '失敗'],
        values=[stat, 100 - stat],
        hole=0.6,
        marker=dict(colors=['rgba(30, 144, 255, 0.7)', 'rgba(220, 220, 220, 0.5)']),
        textinfo = "none",
        rotation = 360 * stat * 0.01 if stat < 50 else 0
    )])
    fig.update_layout(
        showlegend=False,
        template="plotly_dark",
        annotations=
        [
        dict(
            text=f"{stat:.1f}%", x=0.5, y=0.5,
            font=dict(size=40, color="black", family="Arial Black"), showarrow=False
        ),
        # 縁取りの黒テキスト（少し大きいサイズ）
        dict(
            text=name, x=0.055, y=0.945,  # 左上の位置
            font=dict(size=40, color="black", family="Arial Black"), showarrow=False
        ),
        # 本来のテキスト（上に重ねる）
        dict(
            text=name, x=0.05, y=0.95,  # 左上の位置
            font=dict(size=40, color="rgba(30, 144, 255,1)", family="Arial Black"), showarrow=False
        ),
        ],
        width=500,  # グラフの幅を指定
        height=500,  # グラフの高さを指定
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
    """
    <style>
    .box {
        border: 4px solid #1E90FF;
        padding: 15px;
        border-radius: 30px; /* ここを変えれば一括変更可能 */
        background-color: #f9f9f9;
        text-align: center;
    }
    .box h1 {
        font-size: 50px;
        margin: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
def show_stats(stat, name):
    if name == "GAME PLAYED":
        st.markdown(
                f'<div class="box"><h1>{name}</h1><h1>{stat:.0f}</h1></div>',
                unsafe_allow_html=True
                    )
    else:
        st.markdown(
                f'<div class="box"><h1>{name}</h1><h1>{stat:.1f}</h1></div>',
                unsafe_allow_html=True
                    )


def run():
    # ページタイトル
    st.title("NBA 選手シーズンスタッツ表示")
    st.markdown("選手を選択して、シーズンスタッツを確認しましょう。")

    # 選手名とシーズンの入力
    with st.form("プレイヤーとシーズンを選ぶ"):
        player_name = st.text_input("選手名を入力してください（例: LeBron James）", "LeBron James")
        season = st.text_input("シーズンを入力してください（例: 2024-25）", "2024-25")
        submitted = st.form_submit_button("スタッツを見る")

    if submitted:
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

        # 指定されたシーズンのデータを取得
        selected_season = stats_df[stats_df['SEASON_ID'] == season]
        if selected_season.empty:
            st.error(f"{season} シーズンのデータが見つかりません。")
            return
        if len(selected_season) > 1:
            selected_season = selected_season.tail(1)

        # スタッツを取得
        fg_pct = selected_season.iloc[0]['FG_PCT'] * 100
        fg3_pct = selected_season.iloc[0]['FG3_PCT'] * 100
        ft_pct = selected_season.iloc[0]['FT_PCT'] * 100
        pts = selected_season.iloc[0]['PTS'] / selected_season.iloc[0]['GP']
        ast = selected_season.iloc[0]['AST'] / selected_season.iloc[0]['GP']
        reb = selected_season.iloc[0]['REB'] / selected_season.iloc[0]['GP']
        blk = selected_season.iloc[0]['BLK'] / selected_season.iloc[0]['GP']
        stl = selected_season.iloc[0]['STL'] / selected_season.iloc[0]['GP']
        gp = selected_season.iloc[0]['GP']

        st.write("")
        col11, col12, col13 = st.columns([1, 1, 1])
        st.write("")
        col21, col22, col23 = st.columns([1, 1, 1])  # 4つの等分カラム

        # ドーナツチャート用カラム（col5～col7）
        col5, col6, col7 = st.columns([1, 1, 1])  # 3等分カラム

        with col11:
            show_stats(pts, "POINTS PER GAME")

        with col12:
            show_stats(ast, "ASSIST PER GAME")

        with col13:
            show_stats(reb, "REBOUND PER GAME")

        with col21:
            show_stats(blk, "BLOCK PER GAME")

        with col22:
            show_stats(stl, "STEAL PER GAME")

        with col23:
            show_stats(gp, "GAME PLAYED")

        with col5:
            show_donuts_chart(fg_pct, "FG%")

        with col6:
            show_donuts_chart(fg3_pct, "3P%")

        with col7:
            show_donuts_chart(ft_pct, "FT%")

        # データフレーム表示
        st.write(stats_df)
        st.write(data)
