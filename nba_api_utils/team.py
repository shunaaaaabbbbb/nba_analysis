from nba_api.stats.static import teams

class Team:
    """
    チームに関するクラス
    """
    def __init__(self, team_name: str):
        """初期設定

        Args:
            team_name (str): チーム名
        """
        self.name = team_name
        self.id = self._get_team_id()

    def _get_team_id(self):
        """
        チーム名からIDを取得
        """
        team_info = [team for team in teams.get_teams() if team['abbreviation'] == self.name]
        if team_info:
            return team_info[0]["id"]
        else:
            return None