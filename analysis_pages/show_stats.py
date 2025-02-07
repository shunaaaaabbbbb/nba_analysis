import streamlit as st
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

from utils.visualizations import show_donuts_chart, show_stats
from utils.constants import TEAM_COLORS




def _get_players_list():
    player_list = players.get_players()
    player_names = sorted([p["full_name"] for p in player_list])
    player_dict = {p["full_name"]: p["id"] for p in player_list}
    return player_names, player_dict

def _select_player(player_names, player_dict):
    player_name = st.selectbox("選手を選択してください", player_names, index=player_names.index("LeBron James"))
    player_id = player_dict[player_name]
    return player_id, player_name

def _get_career_stats(player_id):
    career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
    return career_stats

def _select_season(career_stats):
    available_seasons = sorted(career_stats.get_data_frames()[0]['SEASON_ID'].unique(), reverse=True)
    season = st.selectbox("シーズンを選択してください", available_seasons)
    return season

def _get_season_stats(career_stats, season):
    stats_df = career_stats.get_data_frames()[0]
    selected_season_stats = stats_df[stats_df['SEASON_ID'] == season]
    if selected_season_stats.empty:
        st.error(f"{season} シーズンのデータが見つかりません。")
        return
    if len(selected_season_stats) > 1:
        selected_season_stats = selected_season_stats.tail(1)
    return selected_season_stats

def _get_color(selected_season_stats):
    team_abbr = selected_season_stats.iloc[0]['TEAM_ABBREVIATION']
    color = TEAM_COLORS.get(team_abbr, "gray") if team_abbr in TEAM_COLORS else "black"
    return color

def _calculate_stats(selected_season_stats):
    # 必要なデータを取得
    stats = {
        "POINTS PER GAME": selected_season_stats.iloc[0]['PTS'] / selected_season_stats.iloc[0]['GP'],
        "ASSIST PER GAME": selected_season_stats.iloc[0]['AST'] / selected_season_stats.iloc[0]['GP'],
        "REBOUND PER GAME": selected_season_stats.iloc[0]['REB'] / selected_season_stats.iloc[0]['GP'],
        "BLOCK PER GAME": selected_season_stats.iloc[0]['BLK'] / selected_season_stats.iloc[0]['GP'],
        "STEAL PER GAME": selected_season_stats.iloc[0]['STL'] / selected_season_stats.iloc[0]['GP'],
        "GAME PLAYED": selected_season_stats.iloc[0]['GP']
    }
    percentages = {
        "FG%": selected_season_stats.iloc[0]['FG_PCT'] * 100,
        "3P%": selected_season_stats.iloc[0]['FG3_PCT'] * 100,
        "FT%": selected_season_stats.iloc[0]['FT_PCT'] * 100
    }
    return stats, percentages

def _get_user_input():
    player_names, player_dict = _get_players_list()
    player_id, player_name = _select_player(player_names, player_dict)
    career_stats = _get_career_stats(player_id)
    season = _select_season(career_stats)
    selected_season_stats = _get_season_stats(career_stats, season)
    color = _get_color(selected_season_stats)
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
