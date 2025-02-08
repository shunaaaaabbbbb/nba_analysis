import streamlit as st
from utils.constants import STATS_LIST
import pandas as pd

def select_player(player_names, key: str = "default"):
    player_name = st.selectbox("選手を選択してください", player_names, index=player_names.index("LeBron James"), key = key)
    return player_name

def select_season(career_stats):
    available_seasons = sorted(career_stats['SEASON_ID'].unique(), reverse=True)
    season = st.selectbox("シーズンを選択してください", available_seasons)
    return season

def get_season_stats(career_stats, season):
    stats_df = career_stats
    selected_season_stats = stats_df[stats_df['SEASON_ID'] == season]
    if selected_season_stats.empty:
        st.error(f"{season} シーズンのデータが見つかりません。")
        return
    if len(selected_season_stats) > 1:
        selected_season_stats = selected_season_stats.tail(1)
    return selected_season_stats

def select_stat():
    stat_name = st.selectbox("比較するスタッツを選択してください:", STATS_LIST)
    stat_name = stat_name.split("（")[0]  # "PTS（得点）" → "PTS" に変換
    return stat_name
