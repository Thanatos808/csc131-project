import csv
import json
from typing import Dict, List
import streamlit as st

#import page render functions
from ui.Home import renderHome
from ui.Dashboard import renderDashboard
from ui.Intake import renderIntake
from ui.StudentDetail import renderStudentDetail
from ui.Export import renderExport
from ui.EmailAutomation import renderEmailAutomation

def main():
    #configure overall app settings
    st.set_page_config(page_title="CSC 131 Prototype", layout="wide")

    #map page names (sidebar label) to their render function
    pageOptions= {
        "Home": renderHome,
        "Dashboard": renderDashboard,
        "Intake": renderIntake,
        "Student Detail": renderStudentDetail,
        "Export": renderExport,
        "Email Automation": renderEmailAutomation,
    }

    #initialize current page in session state
    #session state allows pages to switch to each other
    if "currentPage" not in st.session_state:
        st.session_state["currentPage"] = "Home"

    #radio button lets user choose page manually
    with st.sidebar:
        st.title("Navigation")
        pageNames = list(pageOptions.keys()) #get list of page names
        currentIndex = pageNames.index(st.session_state["currentPage"]) #find index of current page

        selectedPage = st.radio(
            "Go to",
            pageNames,
            index=currentIndex
        )

        st.session_state["currentPage"] = selectedPage  #update session state with user changes

    pageOptions[selectedPage]()

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


def map_to_aha(fields: Dict, meta: Dict) -> Dict:
    return {
        "student_name": fields.get("student_name", "") or "",
        "email": fields.get("email", "") or "",
        "phone": fields.get("phone", "") or "",
        "course": fields.get("course", "") or "",
        "class_date": fields.get("class_date", "") or "",
        "location": fields.get("location", "") or "",
        "payment_status": meta.get("payment_status", "unknown") or "unknown",
        "received_datetime": meta.get("received_datetime", "") or "",
        "source_subject": meta.get("source_subject", "") or "",
        "source_internet_message_id": meta.get("internet_message_id", "") or "",
    }


def map_to_rqi(fields: Dict, meta: Dict) -> Dict:
    return {
        "student_name": fields.get("student_name", "") or "",
        "email": fields.get("email", "") or "",
        "course": fields.get("course", "") or "",
        "rqi_required": "yes",
        "status": "pending",
        "notes": "",
        "received_datetime": meta.get("received_datetime", "") or "",
        "source_internet_message_id": meta.get("internet_message_id", "") or "",
    }


def export_to_csv(rows: List[Dict], path: str, columns: List[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for r in rows:
            writer.writerow({c: r.get(c, "") for c in columns})


def export_to_json(rows: List[Dict], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)


def append_row_to_sheet(gc, sheet_id: str, tab_name: str, row_dict: Dict, columns: List[str]) -> None:
   
    sh = gc.open_by_key(sheet_id)
    ws = sh.worksheet(tab_name)

    values = [row_dict.get(col, "") for col in columns]
    ws.append_row(values, value_input_option="USER_ENTERED")
