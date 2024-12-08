from pandas import DataFrame
from nba_api.stats.endpoints import shotchartdetail


class ShotChart:
    def __init__(self, season: str):
        """
        初期化: シーズンを指定してインスタンスを作成

        Args:
            season (str): 対象のシーズン（例: "2023-24"）
        """
        self.season: str = season

    def _fetch_shot_chart_data(self, team_id: int, player_id: int, game_id: str = None, context_measure: str = 'FGA') -> DataFrame:
        """
        内部メソッド: ショットチャートデータを取得。
        """
        response = shotchartdetail.ShotChartDetail(
            team_id=team_id,
            player_id=player_id,
            season_nullable=self.season,
            game_id_nullable=game_id,
            context_measure_simple=context_measure
        )
        data = response.get_data_frames()[0]
        if data.empty:
            raise ValueError(f"No shot data found")
        return data

    def get_game_shot_data(self, game_id: str, player_id: int) -> DataFrame:
        """特定の試合のプレイヤーショットチャートを取得"""
        return self._fetch_shot_chart_data(team_id=0, player_id=player_id, game_id=game_id)

    def get_team_game_shot_data(self, game_id: str, team_id: int) -> DataFrame:
        """特定の試合のチームショットチャートを取得"""
        return self._fetch_shot_chart_data(team_id=team_id, player_id=0, game_id=game_id)
