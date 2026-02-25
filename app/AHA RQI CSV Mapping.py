import os
import re
import sqlite3
from datetime import datetime, timezone

import requests
import msal #install msal 
from bs4 import BeautifulSoup #pip install beautifulsoup4
 
import gspread #install gspread google-auth
from google.oauth2.service_account import Credentials

#CONFIGURATION
CLIENT_ID = os.environ.get("MS_CLIENT_ID") #Azure Client ID
TENANT_ID = os.environ.get("MS_TENANT_ID", "common")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["Mail.Read"] # Adjust scopes as needed

#Google Sheets Configuration
GOOGLE_CREDS_JSON = os.environ.get("GOOGLE_CREDS_JSON", "service_account.json") #Google Service Account JSON
SHEET_ID = os.environ.get("GOOGLE_SHEET_TAB", "Sheet1")

#Dedupe Path
DB_PATH = os.environ.get("DB_PATH", "seen_emails.sqlite3")

#Email Filtering Keywords
REG_SUBJECT_KEYWORDS = ["AHA", "registration", "enrollment", "class registration"]

#Helper Function
def init_db():
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS seen (
            internet_message_id TEXT PRIMARY KEY,
            received_datetime TEXT
        )
    """)
    con.commit()
    return con

# Authentication and Graph API Client
def already_seen(con, internet_message_id: str) -> bool:
    cur = con.execute("SELECT 1 FROm seen WHERE internet_message_id = ?", (internet_message_id,))
    return cur.fetchone() is not None

#Mark email as seen
def mark_seen(con, internet_message_id: str, received: str):
    con.execute("INSERT INTO seen (internet_message_id, received_datetime) VALUES (?, ?)", (internet_message_id, received))
    con.commit()

#Removing extra whitespace and standardizing line breaks
def normalize(text: str) -> str:
    text = re.sub(r"\r\n", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

#Extracting information 
def find_first(patterns, text):
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE | re.MULTILINE)
        if m:
            return m.group(1).strip()
    return None

EMAIL_RE_FALLBACK = re.compile(
    r"\b([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,})\b", re.IGNORECASE)

#This function to extract fields from the email body
def extract_fields(email_text: str) -> dict:
    """
    Tune these regexes to the real Outlook email template.
    Start broad, then tighten once you have samples.
    """
    t = normalize(email_text)

    name = find_first(
        [
            r"Student Name:\s*(.+)",
            r"Name:\s*(.+)",
            r"Participant:\s*(.+)",
        ],
        t,
    )

    email_addr = find_first(
        [
            r"Email:\s*([^\s]+)",
            r"Student Email:\s*([^\s]+)",
        ],
        t,
    ) or (EMAIL_RE_FALLBACK.search(t).group(1) if EMAIL_RE_FALLBACK.search(t) else None)

    course = find_first(
        [
            r"Course:\s*(.+)",
            r"Class:\s*(.+)",
        ],
        t,
    )

    location = find_first(
        [
            r"Location:\s*(.+)",
            r"Site:\s*(.+)",
            r"Campus:\s*(.+)",
        ],
        t,
    )

    return {
        "student_name": name,
        "email": email_addr,
        "course": course,
        "location": location,
    }

#Microsoft Graph API
def get_graph_token() -> str:
    if not CLIENT_ID:
        raise RuntimeError("MS_CLIENT_ID env var is not set.")

    app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    accounts = app.get_accounts()
    result = app.acquire_token_silent(SCOPES, account=accounts[0] if accounts else None)

    if not result:
        flow = app.initiate_device_flow(scopes=SCOPES)
        if "user_code" not in flow:
            raise RuntimeError(f"Device flow failed: {flow}")
        print(flow["message"])
        result = app.acquire_token_by_device_flow(flow)

    if "access_token" not in result:
        raise RuntimeError(f"Token error: {result.get('error')} - {result.get('error_description')}")
    return result["access_token"]

def graph_list_messages(token: str, top: int = 20):
    url = "https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages"
    params = {
        "$top": top,
        "$select": "subject,from,receivedDateTime,body,internetMessageId",
        "$orderby": "receivedDateTime DESC",
    }
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers, params=params, timeout=30)
    r.raise_for_status()
    return r.json().get("value", [])


def looks_like_registration(subject: str) -> bool:
    s = (subject or "").lower()
    return any(k.lower() in s for k in REG_SUBJECT_KEYWORDS)

#Google Sheets
def sheets_client():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_file(GOOGLE_CREDS_JSON, scopes=scopes)
    return gspread.authorize(creds)


def append_row_to_sheet(gc, row: dict):
    sh = gc.open_by_key(SHEET_ID)
    ws = sh.worksheet(WORKSHEET_NAME)

    # Map to columns
    values = [
        row.get("student_name", ""),
        row.get("email", ""),
        row.get("course", ""),
        row.get("location", ""),
        row.get("received_datetime", ""),
        row.get("source_subject", ""),
    ]
    ws.append_row(values, value_input_option="USER_ENTERED")

# Main pipeline

def main():
    if not CLIENT_ID:
        raise SystemExit("Set MS_CLIENT_ID env var.")
    if not SHEET_ID:
        raise SystemExit("Set GOOGLE_SHEET_ID env var.")

    con = init_db()
    token = get_graph_token()
    gc = sheets_client()

    messages = graph_list_messages(token, top=25)

    for m in messages:
        internet_id = m.get("internetMessageId")
        if not internet_id:
            continue
        if already_seen(con, internet_id):
            continue

        subject = m.get("subject", "")
        if not looks_like_registration(subject):
            # If you want ALL emails processed, remove this
            continue

        received = m.get("receivedDateTime", "")
        body = (m.get("body") or {}).get("content", "")
        body_type = (m.get("body") or {}).get("contentType", "text")

        text = html_to_text(body, body_type)
        fields = extract_fields(text)

        # Basic validation
        if not fields["student_name"] or not fields["email"]:
            # Log for manual review
            print("Skipping (missing name/email):", subject)
            mark_seen(con, internet_id, received)
            continue

        out_row = {
            **fields,
            "received_datetime": received,
            "source_subject": subject,
        }

        append_row_to_sheet(gc, out_row)
        mark_seen(con, internet_id, received)
        print("Wrote:", out_row["student_name"], out_row["email"])


if __name__ == "__main__":
    main()