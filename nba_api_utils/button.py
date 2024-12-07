import streamlit as st

class ButtonHandler:
    @staticmethod
    def select_mode():
        return st.radio("表示モードを選択してください", ["プレイヤー単位", "試合単位"])
