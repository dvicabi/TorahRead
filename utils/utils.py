import os
from glob import glob
from datetime import datetime
from config.config import VIDEO_DIR, THUMBNAIL_EXT, VIDEO_EXT
from pathlib import Path


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
from pathlib import Path

def generate_social_text(parasha, hebrew_date, english_date,
                         playlist_url, mphtir_url, parasha_url,
                         whatsapp_url="https://chat.whatsapp.com/LKPdjJgSdxZ4Hu8M4R1pvj",
                         channel_sub_url="https://www.youtube.com/@YourChannel?sub_confirmation=1"):

    # ← מיפוי כל המשתנים שצריך להחליף
    replacements = {
        "{parasha}": parasha,
        "{playlist_url}": playlist_url,
        "{mphtir_url}": mphtir_url,
        "{parasha_url}": parasha_url,
        "{hebrew_date}": hebrew_date,
        "{english_date}": english_date,
        "{whatsapp_url}": whatsapp_url,
        "{channel_sub_url}": channel_sub_url,
        "{parasha_hash}": parasha.replace(' ', '')
    }

    # ← קריאה לתבנית קיימת בקובץ text_torah_file.txt
    file_path = Path("text_torah_file.txt")

    if not file_path.exists():
        print("❌ הקובץ text_torah_file.txt לא קיים.")
        return

    content = file_path.read_text(encoding="utf-8")

    for key, value in replacements.items():
        content = content.replace(key, value)

    # ← כתיבה חזרה של הקובץ המעודכן
    file_path.write_text(content, encoding="utf-8")
    print("✅ עודכן הקובץ text_torah_file.txt")

    # ← שמירה של אותו טקסט גם לקובץ ההפצה לוואטסאפ ופייסבוק
    Path("text_file_send_facebook_whatsapp.txt").write_text(content, encoding="utf-8")

    # ← העתקה ללוח אם יש pyperclip
    try:
        import pyperclip
        pyperclip.copy(content)
    except ImportError:
        print("ℹ️ להפעלת העתקה ללוח: pip install pyperclip")

    print("📄 נוצר גם text_file_send_facebook_whatsapp.txt והועתק ללוח.")



