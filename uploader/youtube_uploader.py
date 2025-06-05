from googleapiclient.http import MediaFileUpload
from scheduler.scheduler import convert_to_utc
from utils.utils import log_error
from datetime import datetime


def upload_video(youtube, file_path, title, description, scheduled_time, playlist_id, thumbnail_path):
    try:
        media = MediaFileUpload(file_path, chunksize=-1, resumable=True)

        # ✔️ ניקוי תגיות
        raw_tags = [
            "בראשית", "נח", "לך לך", "וירא", "חיי שרה", "תולדות", "ויצא", "וישלח", "וישב", "מקץ",
            "ויגש", "ויחי", "שמות", "וארא", "בא", "בשלח", "יתרו", "משפטים", "תרומה", "תצוה",
            "כי תשא", "ויקהל", "פקודי", "ויקרא", "צו", "שמיני", "תזריע", "מצורע", "אחרי מות",
            "קדושים", "אמור", "בהר", "בחוקותי", "במדבר", "נשא", "בהעלותך", "שלח", "קורח",
            "חוקת", "בלק", "פנחס", "מטות", "מסעי", "דברים", "ואתחנן", "עקב", "ראה", "שופטים",
            "כי תצא", "כי תבוא", "נצבים", "וילך", "האזינו", "וזאת הברכה",
            "דביר", "קבסה", "עליה לתורה", "קריאה בתורה", "חומש", "פרשה", "שבת", "נוסח מרוקאי",
            "sephardic torah reading", "Torah Reading", "Torah reading in Hebrew",
            "parashat hashavua", "weekly torah reading", "aliyah", "hebrew torah chanting",
            "torah chanting", "torah blessings", "hebrew bible", "moroccan jewish",
            "aliyot", "torah portion", "israel synagogue", "parasha video"
        ]

        tags = [
            tag.strip()
            for tag in raw_tags
            if isinstance(tag, str) and tag.strip() != "" and len(tag.strip()) <= 100
        ][:30]  # YouTube מגביל ל־30 תגיות

        # ✔️ בקשת העלאה
        request = youtube.videos().insert(
            part="snippet,status,contentDetails,recordingDetails",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                    "categoryId": "10",
                    "tags": tags,
                    "defaultLanguage": "he",
                    "defaultAudioLanguage": "he"
                },
                "status": {
                    "privacyStatus": "private",
                    "publishAt": convert_to_utc(scheduled_time).isoformat().replace("+00:00", "Z"),
                    "selfDeclaredMadeForKids": False,
                    "license": "creativeCommon",
                    "embeddable": True
                },
                "contentDetails": {
                    "licensedContent": False
                },
                "recordingDetails": {
                    "locationDescription": "Petah Tikva, Israel",
                    "recordingDate": convert_to_utc(scheduled_time).isoformat().replace("+00:00", "Z")
                }
            },
            media_body=media
        )

        response = request.execute()
        video_id = response["id"]

    except Exception as e:
        log_error(f"שגיאה בהעלאת הסרטון: {title}", e)
        return

    # ✔️ טאמבנייל
    try:
        youtube.thumbnails().set(
            videoId=video_id,
            media_body=thumbnail_path
        ).execute()
    except Exception as e:
        log_error(f"שגיאה בהעלאת תמונת טאמבנייל לסרטון {title}", e)

    # ✔️ שיוך לפלייליסט
    try:
        youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        ).execute()
    except Exception as e:
        log_error(f"שגיאה בשיוך הסרטון {title} לפלייליסט", e)

    # ✔️ הדפסה ולוג הצלחה
    print(f"✅ הועלה בהצלחה: {title} בתאריך {scheduled_time}")

    with open("upload_success.log", "a", encoding="utf-8") as log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{timestamp}] הועלה בהצלחה: {title} ({video_id})\n")




def create_playlist(youtube, title, description):
    response = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {"title": title, "description": description},  # פרטי הפלייליסט
            "status": {"privacyStatus": "public"}  # חשיפה לציבור
        }
    ).execute()
    return response["id"]  # החזר את מזהה הפלייליסט
