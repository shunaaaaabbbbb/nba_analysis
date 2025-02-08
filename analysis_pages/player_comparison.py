import streamlit as st

from nba_api_utils.player import PlayerManager, Player
from utils.ui_helpers import select_player, select_stat
from utils.visualizations import plot_cumulative_comparison


def _get_user_input():
    manager = PlayerManager()
    player_names = manager.player_names
    player_name1 = select_player(player_names, key = "player1")
    player_name2 = select_player(player_names, key = "player2")
    player1 = Player(player_name1)
    player2 = Player(player_name2)
    stat_name = select_stat()
    return player1, player2, stat_name

def run():
    st.title("2人の選手の累積スタッツを比較してみよう！")
    st.write("2人の選手と比較したいスタッツを入力したら、両選手のシーズンごとの累積スタッツを表す棒グラフが表示されます。")
    st.header("")
    col1,col2 = st.columns([1,3])
    with col1:
        player1, player2, stat_name = _get_user_input()
        is_button = st.button("スタッツを見る")

    with col2:
        if is_button:
            plot_cumulative_comparison(
                player1, player2,stat_name
                )
