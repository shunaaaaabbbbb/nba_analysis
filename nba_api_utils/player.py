from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import pandas as pd

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

    def get_player_career_stats(self, player_id: int, stat_name: str) -> pd.DataFrame:
        """プレイヤーのキャリアスタッツを返す

        Args:
            player_id (int): プレイヤーID
            stat_name (str): 取得したいスタッツ名

        Returns:
            pd.DataFrame: プレイヤーのキャリアスタッツ
        """
        # プレイヤーのキャリアスタッツを取得
        career = playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()[0]
        career = career[['SEASON_ID', 'TEAM_ABBREVIATION', stat_name]]
       
        # 同じSEASON_IDが複数ある場合、TEAM_ABBREVIATIONが"TOT"のデータを優先
        career = career.sort_values(by=['SEASON_ID', 'TEAM_ABBREVIATION'], ascending=[True, False])
        career = career.drop_duplicates(subset=['SEASON_ID'], keep='first')

        # SEASON_IDを数値型に変換
        career['SEASON_ID'] = career['SEASON_ID'].str[:4].astype(int)
        career = career.sort_values('SEASON_ID').reset_index(drop=True)

        # シーズンのギャップを埋める
        full_seasons = pd.DataFrame({'SEASON_ID': range(career['SEASON_ID'].min(), career['SEASON_ID'].max() + 1)})
        career = pd.merge(full_seasons, career, on='SEASON_ID', how='left')

        # IS_PLAYEDカラムを作成
        career['IS_PLAYED'] = career[stat_name].notna()

        # NaNを0で埋める
        career = career.fillna(0)

        return career