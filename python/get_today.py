"""システム日付（日本時間）を取得する"""

from datetime import datetime, timedelta, timezone

def get_today():
    # デフォルトのタイムゾーンのまま取得する
    now = datetime.now()
    print(f"Now is {now}")
    today = now.strftime('%Y%m%d')
    print(f"Today is {today}")

    # 日付だけならより簡単に
    today = datetime.today()
    print(f"Today is {datetime.strftime(today, '%Y%m%d')}")
    yesterday = today - timedelta(days=1)
    print(f"Yesterday is {datetime.strftime(yesterday, '%Y%m%d')}")

    # 日本時間で取得する（デフォルトのタイムゾーンがUTCの場合）
    jst = timezone(timedelta(hours=+9), 'JST')
    jst_now = datetime.now(jst)
    print(f"Now(JST) is {jst_now}")
    jst_today = jst_now.strftime('%Y%m%d')
    print(f"Today(JST) is {jst_today}")


if __name__ == "__main__":
    get_today()
