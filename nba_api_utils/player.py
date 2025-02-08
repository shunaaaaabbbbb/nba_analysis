from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import pandas as pd


class PlayerManager():
    """全NBA選手を管理するクラス"""
    def __init__(self):
        self.player_names = self._load_players()

    def _load_players(self):
        player_list = players.get_players()
        player_names = sorted([p["full_name"] for p in player_list])
        return player_names

class Player:
    """
    選手に関するクラス
    """
    def __init__(self, player_name: str):
        """初期設定

        Args:
            player_name (str): プレイヤーの名前
        """
        self.name = player_name  # プレイヤー名
        self.id = self._get_player_id()  # プレイヤーid

    def _get_player_id(self) -> pd.DataFrame:
        """選手名からIDを取得

        Raises:
            ValueError: プレイヤーidが見つからないエラー

        Returns:
            pd.DataFrame: プレイヤーのデータフレーム
        """
        player_info = players.find_players_by_full_name(self.name)
        if player_info:
            return player_info[0]["id"]
        else:
            raise ValueError(f"Player {self.name} not found.")


    def get_player_career_stats(self, player_id: int) -> pd.DataFrame:
        """プレイヤーのキャリアスタッツを返す

        Args:
            player_id (int): プレイヤーID
            stat_name (str): 取得したいスタッツ名

        Returns:
            pd.DataFrame: プレイヤーのキャリアスタッツ
        """
        # プレイヤーのキャリアスタッツを取得
        career = playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()[0]

        # 同じSEASON_IDが複数ある場合、TEAM_ABBREVIATIONが"TOT"のデータを優先
        career = career.sort_values(by=['SEASON_ID', 'TEAM_ABBREVIATION'], ascending=[True, False])
        career = career.drop_duplicates(subset=['SEASON_ID'], keep='first')

        # SEASON_IDを数値型に変換
        career['SEASON_ID_int'] = career['SEASON_ID'].str[:4].astype(int).copy()
        career = career.sort_values('SEASON_ID_int').reset_index(drop=True)

        # シーズンのギャップを埋める
        full_seasons = pd.DataFrame({'SEASON_ID_int': range(career['SEASON_ID_int'].min(), career['SEASON_ID_int'].max() + 1)})
        career = pd.merge(full_seasons, career, on='SEASON_ID_int', how='left')

        # `SEASON_ID_int` を `YYYY-YY` 形式の `SEASON_ID` に変換
        career['SEASON_ID'] = career['SEASON_ID_int'].apply(lambda x: f"{x}-{str(x+1)[-2:]}")

        # IS_PLAYEDカラムを作成
        career['IS_PLAYED'] = career["PLAYER_ID"].notna()

        # NaNを0で埋める
        career = career.fillna(0)

        return career