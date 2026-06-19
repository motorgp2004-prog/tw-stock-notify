import os
import sys
from datetime import datetime, timezone, timedelta
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from send_mail import send_email
from twse_api import get_closing_price

STOCK_NO = "6838"
STOCK_NAME = "台新藥"

TARGET_START = 13
TARGET_END = 14


def is_target_time():
    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz)
    if now.weekday() >= 5:
        print(f"週末({now.strftime('%A')})，跳過")
        return False
    # 只允許在 13:30 ~ 13:44 之間執行（每天最多一封）
    if now.hour == 13 and 30 <= now.minute <= 44:
        return True
    print(f"非目標時間({now.hour}:{now.minute:02d})，跳過")
    return False


def main():
    if not is_target_time():
        return

    try:
        info = get_closing_price(STOCK_NO)
    except Exception as e:
        print(f"抓取股價失敗: {e}")
        send_email(
            subject=f"[錯誤] {STOCK_NAME}({STOCK_NO}) 收盤行情取得失敗",
            body=f"無法取得 {STOCK_NAME}({STOCK_NO}) 收盤行情\n錯誤訊息: {e}",
        )
        sys.exit(1)

    line = "=" * 40
    body = f"""
{line}
  {STOCK_NAME}({STOCK_NO}) 收盤行情
  日期: {info['date']}
{line}

  開盤價: {info['open']}
  最高價: {info['high']}
  最低價: {info['low']}
  收盤價: {info['close']}
  漲跌  : {info['change']}
  成交量: {info['volume']} 股
{line}
"""

    subject = f"{info['date']} {STOCK_NAME}({STOCK_NO}) 收盤價: {info['close']}"

    print(body)
    send_email(subject=subject, body=body)


if __name__ == "__main__":
    main()
