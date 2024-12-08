import streamlit as st

class ButtonHandler:
    def __init__(self):
        self.mode = None

    def select_mode(self):
        """モードを選択するためのUIを表示し、選択結果を保存"""
        self.mode = st.radio("表示モードを選択してください", ["プレイヤーのショットチャート", "チームのショットチャート"])
        return self.mode

