import streamlit as st
from analysis_pages import nba_shotchart, player_comparison, show_stats

# ページ設定
st.set_page_config(
    page_title="NBA分析アプリ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# サイドバー
st.sidebar.title("分析機能")
screen = st.sidebar.radio(
    "画面を選択してください:",
    ["ショットチャート分析！", "プレイヤー比較！", "各選手のスタッツ！"]
)

# 各画面を呼び出し
if screen == "ショットチャート分析！":
    nba_shotchart.run()
elif screen == "プレイヤー比較！":
    player_comparison.run()
elif screen == "各選手のスタッツ！":
    show_stats.run()
