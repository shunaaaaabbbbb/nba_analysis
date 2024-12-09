import datetime

def get_season_list():
    """
    現在の年を基準に、最新シーズンから古い順にNBAのシーズンリストを取得する。
    Returns:
        list: シーズンのリスト（例: ["2024-25", "2023-24", ...]）
    """
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month

    # NBAのシーズンは10月から開始。現在の月でシーズンの開始年を判断
    if current_month >= 10:  # 現在の月が10月以降の場合、シーズン開始年は現在の年
        start_year = current_year
    else:  # 現在の月が9月以前の場合、シーズン開始年は前年
        start_year = current_year - 1

    # NBAは1946-47シーズンからスタート
    first_season_year = 2004
    seasons = [f"{year}-{str(year + 1)[-2:]}" for year in range(first_season_year, start_year + 1)]

    return seasons[::-1]  # 新しい順に並べる

