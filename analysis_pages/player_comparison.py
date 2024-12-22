import streamlit as st

from utils.visualizations import plot_cumulative_points_comparison

def run():
    st.title("2人の選手の累積スタッツを比較してみよう！")
    st.write("2人の選手と比較したいスタッツを入力したら、両選手のシーズンごとの累積スタッツを表す棒グラフが表示されます。")
    st.header("")
    col1,col2 = st.columns([1,3])
    with col1:
        player_name1 = st.text_input("1人目の選手名を入力してください。",
                                    "LeBron James")
        player_name2 = st.text_input("2人目の選手名を入力してください。",
                                    "Kareem Abdul-Jabbar")

        stats_list = ["PTS（得点）",
                      "AST（アシスト）",
                      "REB（リバウンド）",
                      "BLK（ブロック）",
                      "OREB（オフェンスリバウンド）",
                      "DREB（ディフェンスリバウンド）",
                      "STL（スティール）",
                      "TOV（ターンオーバー）",
                      "PF（ファール）",
                      "FGM（フィールドゴール成功数）",
                      "FGA（フィールドゴール試投数）",
                      "FG3M（3ポイント成功数）",
                      "FG3A（3ポイント試投数）",
                      "FTM（フリースロー成功数）",
                      "FTA（フリースロー試投数）"
                      ]

        stat_name = st.selectbox("比較するスタッツを選択してください:",
                                 stats_list)
        stat_name = stat_name.split("（")[0]

    with col2:
        if player_name1 and player_name2:
            plot_cumulative_points_comparison(player_name1,
                                              player_name2,
                                              stat_name
                                              )
