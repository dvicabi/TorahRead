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
    with open("templates/default_description.txt", encoding="utf-8") as f:
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


# utils.py  (הוסף בסוף הקובץ)
def generate_social_text(parasha, hebrew_date, english_date,
                         playlist_url, mphtir_url, parasha_url,
                         whatsapp_url="https://chat.whatsapp.com/LKPdjJgSdxZ4Hu8M4R1pvj",
                         channel_sub_url="https://www.youtube.com/@YourChannel?sub_confirmation=1"):
    from pathlib import Path
    with open("templates/social_share_template.txt", encoding="utf-8") as f:
        template = f.read()

    text = (template
            .replace("{parasha}", parasha)
            .replace("{playlist_url}", playlist_url)
            .replace("{mphtir_url}", mphtir_url)
            .replace("{parasha_url}", parasha_url)
            .replace("{hebrew_date}", hebrew_date)
            .replace("{english_date}", english_date)
            .replace("{whatsapp_url}", whatsapp_url)
            .replace("{channel_sub_url}", channel_sub_url)
            .replace("{parasha_hash}", parasha.replace(' ', '')))

    Path("text_file_send_facebook_whatsapp.txt").write_text(text, encoding="utf-8")
    Path("text_torah_file.txt").write_text(text, encoding="utf-8")  # ← עדכון גם של הקובץ המקורי

    try:
        import pyperclip
        pyperclip.copy(text)
    except ImportError:
        print("ℹ️ להתקן העתקה אוטומטית ללוח, הפעל: pip install pyperclip")

    print("📄 נוצר text_file_send_facebook_whatsapp.txt והועתק ללוח.")


