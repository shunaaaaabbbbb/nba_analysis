from nba_api.stats.endpoints import shotchartdetail
import streamlit as st
class ShotChart:
    def __init__(self, player_id, season):
        self.player_id = player_id
        self.season = season

    def get_game_shot_data(self, game_id):
        """
        特定の試合のショットチャートデータを取得。

        Args:
            game_id (str): 試合ID

        Returns:
            DataFrame: ショットチャートデータ
        """
        response = shotchartdetail.ShotChartDetail(
            team_id=0,
            player_id=self.player_id,
            season_nullable=self.season,
            game_id_nullable=game_id,
            context_measure_simple='FGA'
        )
        data = response.get_data_frames()[0]
        if data.empty:

            raise ValueError(f"No shot data found")
        return data


    def get_season_shot_data(self):
        """
        特定のシーズンの全試合のショットチャートデータを取得。

        Returns:
            DataFrame: シーズン全体のショットチャートデータ
        """
        response = shotchartdetail.ShotChartDetail(
            team_id=0,
            player_id=self.player_id,
            season_nullable=self.season,
            context_measure_simple='FGA'
        )
        data = response.get_data_frames()[0]
        if data.empty:
            raise ValueError(f"No shot data found for season {self.season}")
        return data