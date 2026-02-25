import csv
import json
from typing import Dict, List

import streamlit as st


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
    ws.append_row(values, value_input_option="USER_ENTERED")  # fixed Python comment


def renderExport():
    """
    Streamlit page function expected by app/main.py:
      from app.ui.Export import renderExport
    """

    st.title("Export")

    st.write("Choose an export format below.")


    st.subheader("Export options")

    export_type = st.radio("Export type", ["CSV", "JSON"], horizontal=True)

    st.info(
        "This page is wired up so the app runs without import errors.\n\n"
        "To actually export data, we need to know where your student rows live "
        "(for example: st.session_state['students'] or a database)."
    )


    demo_rows = [
        {
            "student_name": "Demo Student",
            "email": "demo@example.com",
            "phone": "555-555-5555",
            "course": "CSC 131",
            "class_date": "2026-02-24",
            "location": "Online",
            "payment_status": "unknown",
            "received_datetime": "",
            "source_subject": "",
            "source_internet_message_id": "",
        }
    ]

    if st.button("Download Demo Export"):
        if export_type == "CSV":
            import io
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=AHA_COLUMNS)
            writer.writeheader()
            for r in demo_rows:
                writer.writerow({c: r.get(c, "") for c in AHA_COLUMNS})

            st.download_button(
                label="Click to download CSV",
                data=output.getvalue(),
                file_name="export.csv",
                mime="text/csv",
            )
        else:
            st.download_button(
                label="Click to download JSON",
                data=json.dumps(demo_rows, indent=2),
                file_name="export.json",
                mime="application/json",
            )
