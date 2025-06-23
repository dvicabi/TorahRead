from auth.auth import get_youtube_service
from hebcal.hebcal import get_next_shabbat_info
from scheduler.scheduler import get_scheduled_time, parasha_title
from uploader.youtube_uploader import upload_video, create_playlist
from utils.utils import collect_files, load_description_template, generate_social_text
from datetime import datetime, timedelta

def main():
    print("🚀 Running main script...")
    youtube = get_youtube_service()  # התחברות לחשבון יוטיוב
    shabbat_info = get_next_shabbat_info()  # קבלת מידע על שבת הקרובה

    if not shabbat_info:
        print("לא נמצאה פרשה לשבוע הבא.")
        return  # יציאה אם אין פרשה

    parasha = shabbat_info["parasha_he"]  # שם הפרשה בעברית
    hebrew_date = shabbat_info["date_he"]  # תאריך עברי
    english_date = shabbat_info["date_en"]  # תאריך לועזי
    # 📌 אנחנו רוצים שהתזמון יהיה עבור יום ראשון הקרוב ולא עבור תאריך השבת (english_date)
    # 📅 לכן נחשב את יום ראשון הקרוב מהיום הנוכחי
    days_until_sunday = (6 - datetime.today().weekday()) % 7  # יום ראשון הבא
    sunday = datetime.today() + timedelta(days=days_until_sunday)
    sunday = sunday.replace(hour=8, minute=0, second=0, microsecond=0)  # קביעת שעת בסיס

    print(f"📅 מתוזמן עבור פרשת {parasha} בשבת {english_date} ({hebrew_date})")

    playlist_title = f"{parasha} – בנוסח מרוקאי {hebrew_date} ({english_date})"  # שם הפלייליסט
    playlist_description = f"קריאה בתורה {parasha}, שבוע {hebrew_date}, {english_date}."  # תיאור הפלייליסט
    playlist_id = create_playlist(youtube, playlist_title, playlist_description)  # יצירת פלייליסט ביוטיוב

    files = collect_files()  # איסוף כל הקבצים לתזמון
    print("📁 קבצים שנמצאו:", files)

    links = {}

    for index, video_path, thumb_path in files:
        scheduled = get_scheduled_time(index, sunday)  # קביעת שעת התזמון
        if not scheduled:
            continue

        title = parasha_title(english_date, hebrew_date, index, parasha)
        description = load_description_template(parasha, hebrew_date, english_date)
        video_id = upload_video(youtube, video_path, title, description, scheduled, playlist_id, thumb_path)  # העלאה בפועל

        links[index] = f"https://youtu.be/{video_id}"

    playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"
    mphtir_url = links.get(8, "")
    parasha_url = links.get(9, "")

    generate_social_text(parasha, hebrew_date, english_date, playlist_url, mphtir_url, parasha_url)


if __name__ == "__main__":
    main()

