import csv
import json
import io
from typing import Dict, List

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from services.email_pipeline import run_email_pipeline


AHA_COLUMNS: List[str] = [
    "student_name",
    "email",
    "phone",
    "course",
    "class_date",
    "location",
    "payment_status",
    "received_datetime",
    "source_subject",
    "source_internet_message_id",
]

RQI_COLUMNS: List[str] = [
    "student_name",
    "email",
    "course",
    "rqi_required",
    "status",
    "notes",
    "received_datetime",
    "source_internet_message_id",
]

RAW_COLUMNS: List[str] = [
    "student_name",
    "email",
    "phone",
    "course",
    "class_date",
    "location",
    "received_datetime",
    "payment_status",
    "source_subject",
    "source_internet_message_id",
    "status",
    "notes",
    "rqi_required",
]


def get_gspread_client():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_file(
        "service_account.json", scopes=scopes
    )
    return gspread.authorize(creds)


def export_rows_to_google_sheet(rows: List[Dict], columns: List[str], sheet_id: str, tab_name: str):
    gc = get_gspread_client()
    sh = gc.open_by_key(sheet_id)

    try:
        ws = sh.worksheet(tab_name)
        ws.clear()
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(title=tab_name, rows=1000, cols=len(columns))

    output_rows = [columns]
    for row in rows:
        output_rows.append([row.get(col, "") for col in columns])

    ws.update("A1", output_rows)


def map_to_aha(student: Dict) -> Dict:
    return {
        "student_name": student.get("student_name", "") or "",
        "email": student.get("email", "") or "",
        "phone": student.get("phone", "") or "",
        "course": student.get("course", "") or "",
        "class_date": student.get("class_date", "") or "",
        "location": student.get("location", "") or "",
        "payment_status": student.get("payment_status", "unknown") or "unknown",
        "received_datetime": student.get("received_datetime", "") or "",
        "source_subject": student.get("source_subject", "") or "",
        "source_internet_message_id": student.get("source_internet_message_id", "") or "",
    }


def map_to_rqi(student: Dict) -> Dict:
    return {
        "student_name": student.get("student_name", "") or "",
        "email": student.get("email", "") or "",
        "course": student.get("course", "") or "",
        "rqi_required": student.get("rqi_required", "yes") or "yes",
        "status": student.get("status", "pending") or "pending",
        "notes": student.get("notes", "") or "",
        "received_datetime": student.get("received_datetime", "") or "",
        "source_internet_message_id": student.get("source_internet_message_id", "") or "",
    }


def map_to_raw(student: Dict) -> Dict:
    return {
        "student_name": student.get("student_name", "") or "",
        "email": student.get("email", "") or "",
        "phone": student.get("phone", "") or "",
        "course": student.get("course", "") or "",
        "class_date": student.get("class_date", "") or "",
        "location": student.get("location", "") or "",
        "received_datetime": student.get("received_datetime", "") or "",
        "payment_status": student.get("payment_status", "unknown") or "unknown",
        "source_subject": student.get("source_subject", "") or "",
        "source_internet_message_id": student.get("source_internet_message_id", "") or "",
        "status": student.get("status", "pending") or "pending",
        "notes": student.get("notes", "") or "",
        "rqi_required": student.get("rqi_required", "yes") or "yes",
    }


def normalize_record(record: Dict) -> Dict:
    return {
        "student_name": record.get("student_name", "") or record.get("name", "") or "",
        "email": record.get("email", "") or "",
        "phone": record.get("phone", "") or "",
        "course": record.get("course", "") or "",
        "class_date": record.get("class_date", "") or record.get("date", "") or "",
        "location": record.get("location", "") or "",
        "payment_status": record.get("payment_status", "unknown") or "unknown",
        "received_datetime": record.get("received_datetime", "") or "",
        "source_subject": record.get("source_subject", "") or "",
        "source_internet_message_id": record.get("source_internet_message_id", "") or "",
        "status": record.get("status", "pending") or "pending",
        "notes": record.get("notes", "") or "",
        "rqi_required": record.get("rqi_required", "yes") or "yes",
    }


def renderExport():
    st.title("Export")

    if st.button("Auto Load Data", type="primary"):
        try:
            results, records = run_email_pipeline()
            parsed_students = []

            for record in records:
                if record.get("email_type") == "registration":
                    parsed_students.append(normalize_record(record))

            st.session_state["parsed_students"] = parsed_students
            st.success(f"Loaded {len(parsed_students)} registration record(s).")
            st.rerun()
        except Exception as e:
            st.error(f"Auto load failed: {e}")

    if "parsed_students" not in st.session_state or not st.session_state["parsed_students"]:
        st.warning("No parsed email data available to export.")
        return

    students = st.session_state["parsed_students"]
    st.success(f"{len(students)} parsed student records ready for export.")

    export_type = st.selectbox(
        "Choose export format",
        ["Raw Student Export", "AHA Export", "RQI Export"]
    )

    if export_type == "Raw Student Export":
        rows = [map_to_raw(student) for student in students]
        columns = RAW_COLUMNS
        default_tab = "Raw Export"
    elif export_type == "AHA Export":
        rows = [map_to_aha(student) for student in students]
        columns = AHA_COLUMNS
        default_tab = "AHA Export"
    else:
        rows = [map_to_rqi(student) for student in students]
        columns = RQI_COLUMNS
        default_tab = "RQI Export"

    st.subheader("Preview")
    st.dataframe(rows, use_container_width=True)

    csv_output = io.StringIO()
    writer = csv.DictWriter(csv_output, fieldnames=columns)
    writer.writeheader()

    for row in rows:
        writer.writerow({col: row.get(col, "") for col in columns})

    st.download_button(
        label="Download CSV",
        data=csv_output.getvalue(),
        file_name="students_export.csv",
        mime="text/csv",
    )

    json_output = json.dumps(rows, indent=2, ensure_ascii=False)

    st.download_button(
        label="Download JSON",
        data=json_output,
        file_name="students_export.json",
        mime="application/json",
    )

    st.divider()
    st.subheader("Export to Google Sheets")

    if "export_sheet_id" not in st.session_state:
        st.session_state["export_sheet_id"] = ""

    if "export_tab_name" not in st.session_state:
        st.session_state["export_tab_name"] = default_tab

    st.session_state["export_sheet_id"] = st.text_input(
        "Google Sheet ID",
        value=st.session_state["export_sheet_id"],
        placeholder="Example: 1AbCDeFgHiJkLmNoPq..."
    )

    st.session_state["export_tab_name"] = st.text_input(
        "Tab name for export",
        value=st.session_state["export_tab_name"]
    )

    if st.button("Export to Google Sheets", type="primary"):
        sheet_id = st.session_state["export_sheet_id"].strip()
        tab_name = st.session_state["export_tab_name"].strip()

        if not sheet_id:
            st.error("Please enter a Google Sheet ID.")
            return

        try:
            export_rows_to_google_sheet(rows, columns, sheet_id, tab_name)
            st.success(f"{export_type} successfully exported to Google Sheets tab '{tab_name}'.")
        except Exception as e:
            st.error(f"Google Sheets export failed: {e}")
