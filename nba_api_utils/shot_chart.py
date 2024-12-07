from nba_api.stats.endpoints import shotchartdetail

class ShotChart:
    def __init__(self, season):
        self.season = season

    def get_game_shot_data(self, game_id, player_id):
        """
        特定の試合のショットチャートデータを取得。

        Args:
            game_id (str): 試合ID

        Returns:
            DataFrame: ショットチャートデータ
        """
        response = shotchartdetail.ShotChartDetail(
            team_id=0,
            player_id=player_id,
            season_nullable=self.season,
            game_id_nullable=game_id,
            context_measure_simple='FGA'
        )
        data = response.get_data_frames()[0]
        if data.empty:

            raise ValueError(f"No shot data found")
        return data


    def get_team_game_shot_data(self, game_id, team_id):
        """
        特定の試合で特定のチームのショットチャートデータを取得。

        Args:
            game_id (str): 試合ID
            team_id (str): チームID

        Returns:
            DataFrame: チームのショットチャートデータ
        """
        response = shotchartdetail.ShotChartDetail(
            team_id=team_id,
            player_id=0,  # プレイヤーIDを0にすることでチーム全体のデータを取得
            season_nullable=self.season,
            game_id_nullable=game_id,
            context_measure_simple='FGA'
        )
        data = response.get_data_frames()[0]
        if data.empty:
            raise ValueError(f"No shot data found for game {game_id} and team {team_id}")
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
            raise ValueError("No games found for the given date.")
        return data