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
    today = datetime.today()  # קבלת התאריך של היום הנוכחי

    # חישוב כמה ימים נשארו לשבת הקרובה (5 = שבת)
    days_until_this_shabbat = (5 - today.weekday()) % 7
    this_shabbat = today + timedelta(days=days_until_this_shabbat)  # קבלת תאריך השבת הקרובה

    next_shabbat = this_shabbat + timedelta(days=7)  # הוספת 7 ימים – לקבל את שבת הבאה, שאותה נרצה לתזמן

    start_date = next_shabbat.strftime("%Y-%m-%d")  # הפורמט הלועזי לתאריך השבת הבאה
    end_date = next_shabbat.strftime("%Y-%m-%d")    # משתמשים באותו תאריך גם להתחלה וגם לסיום – כדי לדייק בחיפוש הפרשה

    # קריאה ל־Hebcal כדי לקבל את פרשת השבוע עבור אותה שבת
    url = f"https://www.hebcal.com/hebcal/?v=1&cfg=json&maj=on&ss=on&mf=on&c=on&geo=il&m=50&s=on&start={start_date}&end={end_date}"
    response = requests.get(url)  # שליחת הבקשה
    data = response.json()  # המרת התשובה ל־JSON

    for item in data.get("items", []):  # מעבר על כל האירועים שהוחזרו
        if item.get("category") == "parashat":  # מציאת האירוע שהוא פרשת השבוע
            hebrew_date = convert_to_hebrew_date(next_shabbat)  # המרת התאריך לשבת לעברית
            return {
                "parasha_he": item["hebrew"],  # שם הפרשה בעברית
                "date_he": hebrew_date,        # התאריך העברי של השבת
                "date_en": next_shabbat.strftime("%Y-%m-%d")  # התאריך הלועזי
            }

    return None  # אם לא נמצאה פרשה, מחזיר None
