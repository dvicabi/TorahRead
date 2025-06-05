import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import SCOPES

def get_youtube_service():
    creds = None  # הגדרת משתנה הרשאות
    if os.path.exists("token.pickle"):  # אם קיים טוקן קיים במחשב
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)  # טען את הטוקן
    if not creds or not creds.valid:  # אם אין טוקן או שהוא לא תקף
        if creds and creds.expired and creds.refresh_token:  # אם פג תוקף אבל יש אפשרות לרענן
            creds.refresh(Request())  # רענון הטוקן
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)  # יצירת תהליך התחברות חדש
            creds = flow.run_local_server(port=0)  # פתיחת דפדפן להתחברות
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)  # שמירת ההרשאות לקובץ
    return build("youtube", "v3", credentials=creds)  # יצירת אובייקט API של יוטיוב
