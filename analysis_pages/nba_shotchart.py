import streamlit as st
from nba_api_utils.input_data import select_player_by_game, select_game
from utils.visualizations import plot_shot_chart
from nba_api_utils.shot_chart import ShotChart


def _select_mode():
    """
    ボタンを使用してモードを選択する。
    """
    mode = st.radio("表示モードを選択してください", ["プレイヤーのショットチャート", "チームのショットチャート"])
    return mode


def _run_player_analysis(output_col):
    """
    プレイヤー単位のショットチャート分析。
    """
    game_id, player_id, season, player_name, game, date = select_player_by_game()

    if not game_id:
        return

    shot_chart = ShotChart(season)
    shot_chart_data = shot_chart.get_game_shot_data(game_id, player_id)

    # タブのリストを定義（タブ名とフィルター条件のペア）
    tabs_config = [
        ("全クォーター", None),  # フィルターなし（全データ）
        ("1Q", shot_chart_data['PERIOD'] == 1),
        ("2Q", shot_chart_data['PERIOD'] == 2),
        ("3Q", shot_chart_data['PERIOD'] == 3),
        ("4Q", shot_chart_data['PERIOD'] == 4),
        ("前半", shot_chart_data['PERIOD'].isin([1, 2])),
        ("後半", shot_chart_data['PERIOD'].isin([3, 4])),
        ("延長", shot_chart_data['PERIOD'] >= 5)
    ]

    with output_col:
        # タブを作成
        tabs = st.tabs([config[0] for config in tabs_config])

        # 各タブの内容を生成
        for tab, (tab_name, mask) in zip(tabs, tabs_config):
            with tab:
                # データのフィルタリング（マスクを使用して元のデータフレーム構造を維持）
                filtered_data = shot_chart_data if mask is None else shot_chart_data[mask]

                # ショットチャートの描画
                if not filtered_data.empty:
                    plot_shot_chart(
                        title="player",
                        shot_chart_data=filtered_data,
                        date=date,
                        game=game,
                        player_name=player_name,
                    )
                else:
                    st.warning(f"{tab_name}のショットデータはありません。")

def _run_game_analysis(output_col):
    """
    プレイヤー単位のショットチャート分析。
    """
    game_id, team_id, season, team_name, game, date = select_game()

    if game_id:
        shot_chart = ShotChart(season)
        shot_chart_data = shot_chart.get_team_game_shot_data(game_id, team_id)

    # タブのリストを定義（タブ名とフィルター条件のペア）
    tabs_config = [
        ("全クォーター", None),  # フィルターなし（全データ）
        ("1Q", shot_chart_data['PERIOD'] == 1),
        ("2Q", shot_chart_data['PERIOD'] == 2),
        ("3Q", shot_chart_data['PERIOD'] == 3),
        ("4Q", shot_chart_data['PERIOD'] == 4),
        ("前半", shot_chart_data['PERIOD'].isin([1, 2])),
        ("後半", shot_chart_data['PERIOD'].isin([3, 4])),
        ("延長", shot_chart_data['PERIOD'] >= 5)
    ]

    with output_col:
        # タブを作成
        tabs = st.tabs([config[0] for config in tabs_config])

        # 各タブの内容を生成
        for tab, (tab_name, mask) in zip(tabs, tabs_config):
            with tab:
                # データのフィルタリング（マスクを使用して元のデータフレーム構造を維持）
                filtered_data = shot_chart_data if mask is None else shot_chart_data[mask]

                # ショットチャートの描画
                if not filtered_data.empty:
                    plot_shot_chart(
                        title="game",
                        shot_chart_data=filtered_data,
                        date=date,
                        game=game,
                        team_name=team_name
                    )
                else:
                    st.warning(f"{tab_name}のショットデータはありません。")


def run():
    """
    アプリケーションのエントリーポイント。
    """
    st.title("NBAのショットチャートを作ってみよう！")
    # 左右のカラムを作成（1:1の比率）
    left_col, right_col = st.columns([1, 1])
    with left_col:
        mode = _select_mode()
        if mode == "プレイヤーのショットチャート":
            _run_player_analysis(right_col)
        elif mode == "チームのショットチャート":
            _run_game_analysis(right_col)
        else:
            st.error("モードが選択されていません。")