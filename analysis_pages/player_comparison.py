import streamlit as st

def run():
    st.title("プレイヤー比較")

    # プレイヤー選択
    player1 = st.text_input("プレイヤー1を入力:")
    player2 = st.text_input("プレイヤー2を入力:")

    if player1 and player2:
        st.write(f"プレイヤー1: {player1}")
        st.write(f"プレイヤー2: {player2}")
        # ここに比較ロジックを追加
    col1, col2 = st.columns([1,1])
    with col1:
        st.write(11)
    with col2:
        st.write(121)