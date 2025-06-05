import requests
from datetime import datetime, timedelta

def convert_to_hebrew_date(gregorian_date):
    """המרת תאריך לועזי לעברי באמצעות Hebcal"""
    url = "https://www.hebcal.com/converter?cfg=json&gy={}&gm={}&gd={}&g2h=1".format(
        gregorian_date.year, gregorian_date.month, gregorian_date.day
    )
    response = requests.get(url)
    data = response.json()
    return data.get("hebrew")

def get_next_shabbat_info():
    today = datetime.today()
    sunday = today + timedelta(days=(6 - today.weekday()) % 7 + 1)  # יום ראשון הבא
    shabbat = sunday + timedelta(days=6)  # שבת שאחריו

    start_date = sunday.strftime("%Y-%m-%d")
    end_date = shabbat.strftime("%Y-%m-%d")

    # בקשת פרשת השבוע מתוך Hebcal API
    url = f"https://www.hebcal.com/hebcal/?v=1&cfg=json&maj=on&ss=on&mf=on&c=on&geo=il&m=50&s=on&start={start_date}&end={end_date}"
    response = requests.get(url)
    data = response.json()

    for item in data.get("items", []):
        if item.get("category") == "parashat":
            hebrew_date = convert_to_hebrew_date(shabbat)
            return {
                "parasha_he": item["hebrew"],
                "date_he": hebrew_date,
                "date_en": shabbat.strftime("%Y-%m-%d")
            }

    return None
