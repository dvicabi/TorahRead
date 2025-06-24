import requests
from datetime import datetime, timedelta

def convert_to_hebrew_date(gregorian_date):
    """המרת תאריך לועזי לעברי באמצעות Hebcal"""
    url = "https://www.hebcal.com/converter?cfg=json&gy={}&gm={}&gd={}&g2h=1".format(
        gregorian_date.year, gregorian_date.month, gregorian_date.day
    )
    response = requests.get(url)
    data = response.json()
    return data.get("hebrew")  # לדוגמה: "י"ז בתמוז תשפ"ד"

def get_hebrew_year(hebrew_date_str):
    """מחזיר רק את השנה מתוך מחרוזת תאריך עברי כמו: י"ז בתמוז תשפ"ד"""
    return hebrew_date_str.split()[-1]  # המילה האחרונה היא השנה

def get_next_shabbat_info():
    today = datetime.today()  # קבלת התאריך של היום הנוכחי

    # חישוב כמה ימים נשארו לשבת הקרובה (5 = שבת)
    days_until_this_shabbat = (5 - today.weekday()) % 7
    this_shabbat = today + timedelta(days=days_until_this_shabbat)  # קבלת תאריך השבת הקרובה

    next_shabbat = this_shabbat + timedelta(days=7)  # הוספת 7 ימים – לקבל את שבת הבאה, שאותה נרצה לתזמן

    # יצירת פורמטים שונים מהתאריך הלועזי
    date_en_full = next_shabbat.strftime("%Y-%m-%d")   # תאריך מלא כמו 2025-08-09
    date_en_year = next_shabbat.strftime("%Y")         # רק השנה, לדוגמה: 2025

    # קריאה ל־Hebcal כדי לקבל את פרשת השבוע עבור אותה שבת
    url = f"https://www.hebcal.com/hebcal/?v=1&cfg=json&maj=on&ss=on&mf=on&c=on&geo=il&m=50&s=on&start={date_en_full}&end={date_en_full}"
    response = requests.get(url)
    data = response.json()

    for item in data.get("items", []):
        if item.get("category") == "parashat":
            full_hebrew_date = convert_to_hebrew_date(next_shabbat)  # תאריך עברי מלא כמו י"ז בתמוז תשפ"ד
            hebrew_year = get_hebrew_year(full_hebrew_date)  # חילוץ השנה בלבד

            # נטרול המילה "פרשת " רק אם קיימת
            name = item["hebrew"]
            parasha_name = name[5:] if name.startswith("פרשת ") else name

            return {
                "parasha_he": parasha_name,  # שם הפרשה בלבד
                "hebrew_year": hebrew_year,  # שנה עברית (תשפ"ד)
                "date_en": date_en_full,  # תאריך לועזי מלא (2025-08-09)
                "gregorian_year": date_en_year  # שנה לועזית בלבד (2025)
            }

    return None  # אם לא נמצאה פרשה

# קריאה לדוגמה
print(get_next_shabbat_info())