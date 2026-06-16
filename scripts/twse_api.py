import requests
from datetime import datetime, timezone, timedelta

TWSE_URL = "https://www.twse.com.tw/exchangeReport/STOCK_DAY"

ROC_OFFSET = 1911


def _ad_to_roc(ad_year: int) -> int:
    return ad_year - ROC_OFFSET


def _roc_to_ad(roc_year: int) -> int:
    return roc_year + ROC_OFFSET


def _roc_date_str(ad_date: datetime) -> str:
    return f"{_ad_to_roc(ad_date.year)}/{ad_date.month:02d}/{ad_date.day:02d}"


def get_closing_price(stock_no: str) -> dict:
    tz = timezone(timedelta(hours=8))
    today = datetime.now(tz)
    date_str = today.strftime("%Y%m%d")

    params = {"response": "json", "date": date_str, "stockNo": stock_no}

    resp = requests.get(TWSE_URL, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    if data["stat"] != "OK":
        raise Exception(f"TWSE API error: {data['stat']}")

    rows = data["data"]
    if not rows:
        raise Exception("無成交資料，可能今日未交易或盤後資料尚未產出")

    fields = data["fields"]
    target_date = _roc_date_str(today)

    # 找今日的資料列，若無則取最後一筆
    row = None
    for r in rows:
        if r[0] == target_date:
            row = r
            break
    if row is None:
        row = rows[-1]
        print(f"警告: 未找到今日({target_date})資料，取最後一筆({row[0]})")

    return {
        "date": row[0],
        "open": row[3],
        "high": row[4],
        "low": row[5],
        "close": row[6],
        "change": row[7],
        "volume": row[1],
        "fields": {f: v for f, v in zip(fields, row)},
    }
