import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from send_mail import send_email
from twse_api import get_closing_price

STOCK_NO = "6838"
STOCK_NAME = "台新藥"


def main():
    try:
        info = get_closing_price(STOCK_NO)
    except Exception as e:
        print(f"抓取股價失敗: {e}")
        send_email(
            subject=f"[錯誤] {STOCK_NAME}({STOCK_NO}) 收盤行情取得失敗",
            body=f"無法取得 {STOCK_NAME}({STOCK_NO}) 收盤行情\n錯誤訊息: {e}",
        )
        sys.exit(1)

    body = f"""
{'='*40}
  {STOCK_NAME}({STOCK_NO}) 收盤行情
  日期: {info['date']}
{'='*40}

  開盤價: {info['open']}
  最高價: {info['high']}
  最低價: {info['low']}
  收盤價: {info['close']}
  漲跌  : {info['change']}
  成交量: {info['volume']} 股
{'='*40}
"""

    subject = f"{info['date']} {STOCK_NAME}({STOCK_NO}) 收盤價: {info['close']}"

    print(body)
    send_email(subject=subject, body=body)


if __name__ == "__main__":
    main()
