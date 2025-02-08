import streamlit as st

from nba_api_utils.player import PlayerManager, Player
from utils.visualizations import show_donuts_chart, show_stats
from utils.ui_helpers import select_player, select_season, get_season_stats
from utils.helpers import get_color



def _calculate_stats(selected_season_stats):
    # 必要なデータを取得
    stats = {
        "POINTS PER GAME": selected_season_stats.iloc[0]['PTS'] / selected_season_stats.iloc[0]['GP'] if selected_season_stats.iloc[0]['GP'] > 0 else 0,
        "ASSIST PER GAME": selected_season_stats.iloc[0]['AST'] / selected_season_stats.iloc[0]['GP'] if selected_season_stats.iloc[0]['GP'] > 0 else 0,
        "REBOUND PER GAME": selected_season_stats.iloc[0]['REB'] / selected_season_stats.iloc[0]['GP'] if selected_season_stats.iloc[0]['GP'] > 0 else 0,
        "BLOCK PER GAME": selected_season_stats.iloc[0]['BLK'] / selected_season_stats.iloc[0]['GP'] if selected_season_stats.iloc[0]['GP'] > 0 else 0,
        "STEAL PER GAME": selected_season_stats.iloc[0]['STL'] / selected_season_stats.iloc[0]['GP'] if selected_season_stats.iloc[0]['GP'] > 0 else 0,
        "GAME PLAYED": selected_season_stats.iloc[0]['GP']
    }
    percentages = {
        "FG%": selected_season_stats.iloc[0]['FG_PCT'] * 100,
        "3P%": selected_season_stats.iloc[0]['FG3_PCT'] * 100,
        "FT%": selected_season_stats.iloc[0]['FT_PCT'] * 100
    }
    return stats, percentages

def _get_user_input():
    manager = PlayerManager()
    player_names = manager.player_names
    player_name = select_player(player_names)
    player = Player(player_name)
    career_stats = player.get_player_career_stats(player.id)
    season = select_season(career_stats)
    selected_season_stats = get_season_stats(career_stats, season)
    color = get_color(selected_season_stats)
    stats, percentages = _calculate_stats(selected_season_stats)
    return player_name, stats, color, percentages, season


def run():
    st.title("NBA 選手シーズンスタッツ表示")
    st.markdown("選手を選択して、シーズンスタッツを確認しましょう。")

    player_name, stats, color, percentages, season = _get_user_input()

    if st.button("スタッツを見る"):

        # 表示
        st.markdown(f"<h2 style='text-align: center;'>{player_name}'s Season Stats ({season} Season)</h2>", unsafe_allow_html=True)
        st.write("")

        cols = st.columns(3)
        for i, (label, value) in enumerate(stats.items()):
            with cols[i % 3]:
                show_stats(value, label, color)
                st.write("")

        cols = st.columns(3)
        for i, (label, value) in enumerate(percentages.items()):
            with cols[i]:
                show_donuts_chart(value, label, color)
