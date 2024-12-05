import streamlit as st
from nba_api.stats.endpoints import boxscoretraditionalv2
from nba_api.stats.endpoints import leaguegamelog
from nba_api.stats.static import players


def get_game_log(season, date):
    """
    指定されたシーズンと日付の試合ログを取得し、該当する試合を返す。

    Parameters:
        season (str): NBAシーズン (例: "2023-24")
        date (str): 試合日付 (例: "2024-11-20")

    Returns:
        DataFrame: 該当する試合のログ
    """
    gamelog = leaguegamelog.LeagueGameLog(season=season, player_or_team_abbreviation="T")
    games = gamelog.get_data_frames()[0]
    return games[games["GAME_DATE"] == date]


def get_player_name(game_id, team):
    """
    選手名を入力してNBAのプレイヤーIDを返す関数。

    Parameters:
        player_name (str): 検索したい選手の名前（フルネームまたは部分一致）

    Returns:
        int: プレイヤーID (該当なしの場合はNone)
    """
    boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
    game_stats = boxscore.get_data_frames()[0]
    player_name = game_stats[game_stats["TEAM_ABBREVIATION"] == team]["PLAYER_NAME"]
    return player_name

def get_player_id(player_name):
    """
    選手名を入力してNBAのプレイヤーIDを返す関数。

    Parameters:
        player_name (str): 検索したい選手の名前（フルネームまたは部分一致）

    Returns:
        int: プレイヤーID (該当なしの場合はNone)
    """
    # プレイヤーを検索
    player_info = players.find_players_by_full_name(player_name)
    if player_info:
        return player_info[0]["id"]
    else:
        return None

def get_two_teams(game_id):
    boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
    game_stats = boxscore.get_data_frames()[0]
    two_team = game_stats["TEAM_ABBREVIATION"].unique()
    return two_team
    

def select_player_by_game():
    """
    Streamlit UIでシーズン、日付、試合、チーム、選手を選択し、
    選択された選手のIDを返す。

    Returns:
        dict: 選択された情報 (シーズン、日付、試合ID、チーム名、選手名、選手ID)
    """
    # Step 1: シーズンの選択
    season = st.text_input("Enter Season (e.g., 2023-24):", "")
    if not season:
        st.stop()

    # Step 2: 日付の選択
    date = st.text_input("Enter Game Date (YYYY-MM-DD):", "")
    if not date:
        st.stop()

    # Step 3: 試合ログの取得
    try:
        games_on_date = get_game_log(season, date)
        if games_on_date.empty:
            st.warning("No games found for the given date.")
            st.stop()
    except Exception as e:
        st.error(f"Error fetching games: {e}")
        st.stop()

    # Step 4: 試合の選択
    game_options = {row["MATCHUP"]: row["GAME_ID"] for _, row in games_on_date.iterrows()}
    selected_game = st.selectbox("Select a game:", list(game_options.keys()))
    if not selected_game:
        st.stop()

    game_id = game_options[selected_game]

    # Step 5: チームの選択
    teams = get_two_teams(game_id)
    selected_team = st.selectbox("Select a team:", teams)
    if not selected_team:
        st.stop()

    # Step 6: 選手の選択
    # 選手一覧はここでは仮定的に用意。APIを使うなら試合IDに基づく選手データを取得する処理を追加
    players_on_team = get_player_name(game_id, selected_team)
    selected_player = st.selectbox("Select a player:", players_on_team)
    if not selected_player:
        st.stop()

    # プレイヤーIDの取得
    player_id = get_player_id(selected_player)
    if not player_id:
        st.error("Player ID not found.")
        st.stop()
    
    return game_id, player_id, season