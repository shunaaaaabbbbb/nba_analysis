from nba_api.stats.static import players

class Player:
    """
    選手に関するクラス
    """
    def __init__(self, player_name: str):
        """初期設定

        Args:
            player_name (str): プレイヤーの名前
        """
        self.name = player_name
        self.id = self._get_player_id()

    def _get_player_id(self):
        """
        選手名からIDを取得
        """
        player_info = players.find_players_by_full_name(self.name)
        if player_info:
            return player_info[0]["id"]
        else:
            raise ValueError(f"Player {self.name} not found.")
