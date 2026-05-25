import streamlit as st
from datetime import datetime
from typing import List, Dict
import gspread
from google.oauth2.service_account import Credentials

COLUMNS = [
    "student_name",
    "email",
    "phone",
  "course",
    "class_date",
    "location",
    "received_datetime",
]
def get_gspread_client():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_file("service_account.json", scopes=scopes)
    return gspread.authorize(creds)

def append_student_to_sheet(student: dict, sheet_id: str, tab_name: str):
    gc = get_gspread_client()
   sh = gc.open_by_key(sheet_id)
    ws = sh.worksheet(tab_name)
    existing = ws.get_all_values()
    if not existing:
      ws.append_row(COLUMNS, value_input_option="USER_ENTERED")

    row = [student.get(col, "") for col in COLUMNS]
    ws.append_row(row, value_input_option="USER_ENTERED")


         def send_to_intake(student: Dict, sheet_id: str, tab_name: str = "Sheet1"):
    
    if not sheet_id:
        raise ValueError("No Sheet ID provided to send_to_intake.")

    append_student_to_sheet(student, sheet_id, tab_name)
    if "students" not in st.session_state: # make sure it exists
        st.session_state["students"] = []
    if "students" in st.session_state:
       
        for s in st.session_state["students"]:
            if s.get("email") == student.get("email"):
                s["completed"] = True
                break
    else:
        # adds new students
        new_entry = student.copy()
        new_entry["completed"] = True
            st.session_state["students"].append(new_entry)

def renderIntake():
    st.title("Intake")
    if "students" not in st.session_state:
        st.session_state["students"] = []
    if "sheet_id" not in st.session_state:
        st.session_state["sheet_id"] = ""
    if "tab_name" not in st.session_state:
        st.session_state["tab_name"] = "Sheet1"

    st.subheader("Google Sheets Connection")
    st.session_state["sheet_id"] = st.text_input(
        "Google Sheet ID (from the URL)",
        value=st.session_state["sheet_id"],
        placeholder="Example: 1AbCDeFgHiJkLmNoPq...",
    )
    st.session_state["tab_name"] = st.text_input(
        "Tab name",
        value=st.session_state["tab_name"],
    )

    st.divider()

    with st.form("intake_form"):
        student_name = st.text_input("Student Name")
            email = st.text_input("Email")
        phone = st.text_input("Phone")
    course = st.text_input("Course")
        class_date = st.text_input("Class Date")
        location = st.text_input("Location")

        submitted = st.form_submit_button("Add Student")

    if submitted:
        new_student = {
            "student_name": student_name.strip(),
          "email": email.strip(),
            "phone": phone.strip(),
            "course": course.strip(),
         "class_date": class_date.strip(),
            "location": location.strip(),
            "received_datetime": datetime.now().isoformat(timespec="seconds"),
        }

        st.session_state["students"].append(new_student)

      sheet_id = st.session_state["sheet_id"].strip()
        tab_name = st.session_state["tab_name"].strip()

        if sheet_id:
            try:
                append_student_to_sheet(new_student, sheet_id, tab_name)
                st.success("Student added AND uploaded to Google Sheets ")
            except Exception as e:
                st.warning("Student added locally, but Google Sheets upload failed.")
          st.error(f"Sheets error: {e}")
        else:
            st.success("Student added locally  (add Sheet ID to auto-upload)")

    if st.session_state["students"]:
        st.subheader("Students collected so far")
        st.dataframe(st.session_state["students"], use_container_width=True)
