import streamlit as st
import csv
import json
import io
from datetime import datetime

from app.services.read_emails import get_access_token, read_emails
from app.services.email_parsing import parse_registration_email


def normalize_record(record):
    return {
        "student_name": record.get("student_name", "") or record.get("name", "") or "",
        "email": record.get("email", "") or "",
        "phone": record.get("phone", "") or "",
     "course": record.get("course", "") or "",
        "class_date": record.get("class_date", "") or record.get("date", "") or "",
        "location": record.get("location", "") or "",
        "received_datetime": record.get("received_datetime", "") or "",
    }


def renderExport():
    st.title("Export")

    if "students" not in st.session_state:
        st.session_state["students"] = []

           if "seen_keys" not in st.session_state:
        st.session_state["seen_keys"] = set()

    if st.button("Auto Load Data", type="primary"):
        try:
            token = get_access_token(log=st.write)
            emails = read_emails(token)

            parsed_students = []
            st.session_state["seen_keys"] = set()

            for e in emails:
                body = e.get("body", {}).get("content", "")
                        record = parse_registration_email(body)

                if record and record.get("email"):
                        normalized = normalize_record(record)
                    normalized["received_datetime"] = e.get(
                        "receivedDateTime",
                        datetime.now().isoformat(timespec="seconds")
                    )

                    unique_key = (
                        normalized["email"],
              normalized["class_date"],
                        normalized["course"],
                    )

                          if unique_key not in st.session_state["seen_keys"]:
                        st.session_state["seen_keys"].add(unique_key)
                    parsed_students.append(normalized)

  st.session_state["students"] = parsed_students
                st.success(f"Loaded {len(parsed_students)} registration record(s).")

       except Exception as e:
            st.error(f"Auto load failed: {e}")

    students = st.session_state.get("students", [])

    if not students:
        st.warning("No parsed email data available to export.")
        return

    st.success(f"{len(students)} student record(s) ready for export.")
    st.dataframe(students, use_container_width=True)

       csv_output = io.StringIO()
    fieldnames = [
        "student_name",
        "email",
      "phone",
        "course",
       "class_date",
        "location",
        "received_datetime",
    ]
 writer = csv.DictWriter(csv_output, fieldnames=fieldnames)
    writer.writeheader()
     for row in students:
        writer.writerow(row)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    st.download_button(
        label="Download CSV",
        data=csv_output.getvalue(),
        file_name=f"students_export_{timestamp}.csv",
        mime="text/csv",
    )

         json_output = json.dumps(students, indent=2)
    st.download_button(
        label="Download JSON",
        data=json_output,
        file_name=f"students_export_{timestamp}.json",
        mime="application/json",
    )
