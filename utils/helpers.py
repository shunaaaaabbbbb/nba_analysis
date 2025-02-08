import pandas as pd
from nba_api_utils.player import Player
from utils.constants import TEAM_COLORS

def get_color(selected_season_stats):
    team_abbr = selected_season_stats.iloc[0]['TEAM_ABBREVIATION']
    color = TEAM_COLORS.get(team_abbr, "gray") if team_abbr in TEAM_COLORS else "black"
    return color



def get_player_stats(player: Player) -> pd.DataFrame:
    """選手のキャリアスタッツを取得"""
    stats = player.get_player_career_stats(player.id)
    return stats

def prepare_cumlative_stats(stats: pd.DataFrame, stat_name: str) -> pd.DataFrame:
    """累積スタッツを計算し、キャリア年数を追加"""
    stats[f'CUMULATIVE_{stat_name}'] = stats[stat_name].cumsum()
    stats['CAREER_YEAR'] = range(1, len(stats) + 1)
    return stats

def fill_missing_career_years(stats1: pd.DataFrame, stats2: pd.DataFrame, stat_name: str):
    """短い方のキャリアをゼロ埋めする"""
    max_career_length = max(len(stats1), len(stats2))

    for stats in [stats1, stats2]:
        if len(stats) < max_career_length:
            filler = max_career_length - len(stats)
            additional_rows = pd.DataFrame({
                'CAREER_YEAR': range(len(stats) + 1, max_career_length + 1),
                f'CUMULATIVE_{stat_name}': [0] * filler
            })
            stats = pd.concat([stats, additional_rows], ignore_index=True)

    return stats1, stats2