from datetime import timedelta
from pytz import timezone, utc


def get_scheduled_time(index, sunday):
    if index <= 7:
        return sunday.replace(hour=8 + (index - 1))  # עבור עליות 1–7, כל שעה משעה 8 בבוקר
    elif index == 8:
        return (sunday + timedelta(days=1)).replace(hour=9)  # עלייה 8 – יום שני ב־9:00
    elif index == 9:
        return (sunday + timedelta(days=1)).replace(hour=12)  # עלייה 9 – יום שני ב־12:00
    else:
        return None  # אין זמן תזמון מוגדר לשאר הערכים


def convert_to_utc(dt_local):
    israel = timezone("Asia/Jerusalem")
    local_dt = israel.localize(dt_local)  # קובע שהשעה היא שעון ישראל
    utc_dt = local_dt.astimezone(utc)  # ממיר ל־UTC
    return utc_dt


def parasha_title(english_date, hebrew_date, index, parasha):
    aliquot = [
        "עלייה ראשונה",
        "עלייה שנייה",
        "עלייה שלישית",
        "עלייה רביעית",
        "עלייה חמישית",
        "עלייה שישית",
        "עלייה שביעית"
    ]

    if index <= 7:
        aliyah_name = aliquot[index - 1]
        title = f"{parasha} {aliyah_name} בנוסח יהדות מרוקו - {hebrew_date} ({english_date})"
    elif index == 8:
        title = f"מפטיר הפטרה {parasha} בנוסח יהדות מרוקו - {hebrew_date} ({english_date})"
    else:
        title = f"{parasha} בנוסח יהדות מרוקו - {hebrew_date} ({english_date})"
    return title
