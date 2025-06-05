import os
from glob import glob
from datetime import datetime
from config.config import VIDEO_DIR, THUMBNAIL_EXT, VIDEO_EXT


def collect_files():
    pairs = []
    for video_file in glob(os.path.join(VIDEO_DIR, f"*{VIDEO_EXT}")):  # מעבר על כל קבצי הווידאו בתיקייה
        base = os.path.splitext(os.path.basename(video_file))[0]  # קבלת שם הקובץ ללא הסיומת
        try:
            index = int(base)  # ניסיון להמיר את שם הקובץ למספר (1–9)
        except ValueError:
            continue  # אם לא הצליח, דלג
        thumb_path = os.path.join(VIDEO_DIR, f"{base}{THUMBNAIL_EXT}")  # בניית הנתיב לתמונת הטאמבנייל
        if os.path.exists(thumb_path):  # רק אם התמונה קיימת
            pairs.append((index, video_file, thumb_path))  # הוסף לרשימה
    return sorted(pairs, key=lambda x: x[0])  # מיון לפי מספר העלייה


def load_description_template(parasha, hebrew_date, english_date):
    with open("default_description.txt", encoding="utf-8") as f:
        template = f.read()
    return (
        template.replace("{parasha}", parasha)
                .replace("{hebrew_date}", hebrew_date)
                .replace("{english_date}", english_date)
    )


def log_error(message, exception):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_message = f"[{timestamp}] {message}\n{str(exception)}\n\n"
    print(error_message)  # הדפסה לקונסול
    with open("upload_errors.log", "a", encoding="utf-8") as f:
        f.write(error_message)
