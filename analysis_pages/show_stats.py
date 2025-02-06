import streamlit as st
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

from utils.visualizations import show_donuts_chart, show_stats
from utils.constants import TEAM_COLORS


def run():
    st.title("NBA 選手シーズンスタッツ表示")
    st.markdown("選手を選択して、シーズンスタッツを確認しましょう。")

    player_list = players.get_players()
    player_names = sorted([p["full_name"] for p in player_list])
    player_dict = {p["full_name"]: p["id"] for p in player_list}

    player_name = st.selectbox("選手を選択してください", player_names, index=player_names.index("LeBron James"))
    player_id = player_dict[player_name]
    career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
    available_seasons = sorted(career_stats.get_data_frames()[0]['SEASON_ID'].unique(), reverse=True)
    season = st.selectbox("シーズンを選択してください", available_seasons)

    if st.button("スタッツを見る"):
        stats_df = career_stats.get_data_frames()[0]
        selected_season = stats_df[stats_df['SEASON_ID'] == season]
        if selected_season.empty:
            st.error(f"{season} シーズンのデータが見つかりません。")
            return
        if len(selected_season) > 1:
            selected_season = selected_season.tail(1)

        team_abbr = selected_season.iloc[0]['TEAM_ABBREVIATION']
        color = TEAM_COLORS.get(team_abbr, "gray") if team_abbr in TEAM_COLORS else "black"

        fg_pct = selected_season.iloc[0]['FG_PCT'] * 100
        fg3_pct = selected_season.iloc[0]['FG3_PCT'] * 100
        ft_pct = selected_season.iloc[0]['FT_PCT'] * 100
        pts = selected_season.iloc[0]['PTS'] / selected_season.iloc[0]['GP']
        ast = selected_season.iloc[0]['AST'] / selected_season.iloc[0]['GP']
        reb = selected_season.iloc[0]['REB'] / selected_season.iloc[0]['GP']
        blk = selected_season.iloc[0]['BLK'] / selected_season.iloc[0]['GP']
        stl = selected_season.iloc[0]['STL'] / selected_season.iloc[0]['GP']
        gp = selected_season.iloc[0]['GP']


        st.markdown(
            f'<h2 style="text-align: center;">{player_name}\'s Season Stats ({season} Season)</h2>',
            unsafe_allow_html=True
        )
        st.write("")
        col11, col12, col13 = st.columns([1, 1, 1])
        st.write("")
        col21, col22, col23 = st.columns([1, 1, 1])
        col5, col6, col7 = st.columns([1, 1, 1])

        with col11:
            show_stats(pts, "POINTS PER GAME", color)
        with col12:
            show_stats(ast, "ASSIST PER GAME", color)
        with col13:
            show_stats(reb, "REBOUND PER GAME", color)
        with col21:
            show_stats(blk, "BLOCK PER GAME", color)
        with col22:
            show_stats(stl, "STEAL PER GAME", color)
        with col23:
            show_stats(gp, "GAME PLAYED", color)
        with col5:
            show_donuts_chart(fg_pct, "FG%", color)
        with col6:
            show_donuts_chart(fg3_pct, "3P%", color)
        with col7:
            show_donuts_chart(ft_pct, "FT%", color)
