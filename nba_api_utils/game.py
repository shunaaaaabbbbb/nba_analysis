from nba_api.stats.endpoints import leaguegamelog, boxscoretraditionalv2

class Game:
    """
    試合に関するクラス
    """
    def __init__(self, season: str, date: str):
        """初期設定

        Args:
            season (str): シーズン(ex. 2024-25)
            date (str): 日付
        """
        self.season = season
        self.date = date
        self.game_log = self._fetch_game_log()

    def _fetch_game_log(self):
        """
        指定されたシーズンと日付の試合ログを取得
        """
        gamelog = leaguegamelog.LeagueGameLog(season=self.season, player_or_team_abbreviation="T")
        games = gamelog.get_data_frames()[0]
        return games[games["GAME_DATE"] == self.date]

    def get_teams(self, game_id: int):
        """
        試合IDから参加チームを取得
        """
        boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
        game_stats = boxscore.get_data_frames()[0]
        return game_stats["TEAM_ABBREVIATION"].unique()
