# email_parsing.py - CSC 131

import re
from html import unescape

# Helper Functions

def strip_html(html_text: str) -> str:
    """Remove HTML tags, unescape entities, keep text clean."""
    text = re.sub(r"<[^>]+>", "\n", html_text)       # Replace HTML tags with newline
    text = re.sub(r"\n+", "\n", text)                # Collapse multiple newlines
    text = unescape(text).strip()                    # Unescape HTML entities
    text = re.sub(r"=+", "", text)                   # Remove repeated '='
    return text

def normalize_email_body(email_body: str) -> str:
    """Normalize email body: strip HTML, collapse whitespace."""
    text = strip_html(email_body)
    text = re.sub(r"\s+", " ", text)                # Collapse multiple whitespace
    return text.strip()

def normalize_phone(phone: str) -> str:
    """Normalize phone numbers to XXX-XXX-XXXX format if possible."""
    digits = re.sub(r"[^\d]", "", phone or "")
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    elif len(digits) == 7:  # Optional: local numbers without area code
        return f"{digits[:3]}-{digits[3:]}"
    else:
        return digits  # return as-is if unexpected format

# Email Parsing Functions

def parse_registration_email(email_body: str) -> dict:
    """Extract registration info from email body."""
    email_body = normalize_email_body(email_body)

    # Remove admin-only sections if present
    admin_section = re.search(r"The info below is just sent to you as the admin(.+)", email_body, re.IGNORECASE)
    if admin_section:
        email_body = admin_section.group(1)

    # Extract fields
    name_match = re.search(r"Name[:=\-]?\s*([A-Za-z\s]+?)(?=\s*(Phone|Email|Course|Date|Location|$))", email_body, re.IGNORECASE)
    phone_match = re.search(r"Phone[:=\-]?\s*([\+\d\-\(\)\s]+)", email_body, re.IGNORECASE)
    email_match = re.search(r"Email[:=\-]?\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})", email_body, re.IGNORECASE)
    course_match = re.search(r"(?:Course|Class)[:=\-]?\s*([A-Za-z0-9\s]+)", email_body, re.IGNORECASE)
    date_match = re.search(r"Date[:=\-]?\s*(\d{4}/\d{2}/\d{2}|\d{2}/\d{2}/\d{4})", email_body)
    location_match = re.search(r"Location[:=\-]?\s*([A-Za-z0-9,.\s]+)", email_body, re.IGNORECASE)

    return {
        "email_type": "registration",
        "name": name_match.group(1).strip() if name_match else "",
        "phone": normalize_phone(phone_match.group(1)) if phone_match else "",
        "email": email_match.group(1).strip().lower() if email_match else "",
        "course": course_match.group(1).strip() if course_match else "",
        "date": date_match.group(1).strip() if date_match else "",
        "location": location_match.group(1).strip() if location_match else "",
        "aha_registered": "Y",
        "payment_status": "Pending",
        "rqi_uploaded": "N",
        "reminder_sent": "N"
    }

def parse_payment_email(email_body: str) -> dict:
    """Extract payment info from email body."""
    name_match = re.search(r"Name[:=\-]?\s*(.+?)(?:\n|$)", email_body, re.IGNORECASE)
    phone_match = re.search(r"Phone[:=\-]?\s*(.+?)(?:\n|$)", email_body, re.IGNORECASE)
    email_match = re.search(r"Email[:=\-]?\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})", email_body, re.IGNORECASE)
    transaction_match = re.search(r"Transaction ID[:=\-]?\s*(.+?)(?:\n|$)", email_body, re.IGNORECASE)

    return {
        "email_type": "payment",
        "name": name_match.group(1).strip() if name_match else "",
        "phone": normalize_phone(phone_match.group(1)) if phone_match else "",
        "email": email_match.group(1).strip().lower() if email_match else "",
        "transaction_id": transaction_match.group(1).strip() if transaction_match else "",
        "payment_status": "Paid"
    }

def parse_atlas_notification_email(email_body: str) -> dict:
    """
    Parse Atlas enrollment notification emails and mark them as Atlas notifications.
    """
    email_body = normalize_email_body(email_body)

    # Extract instructor name after "Dear"
    instructor_match = re.search(r"Dear\s+([A-Za-z\s]+)", email_body)

    # Extract course name and date
    course_match = re.search(r"requests for (.+?) on", email_body, re.IGNORECASE)
    date_match = re.search(r"on (\d{2}/\d{2}/\d{4})", email_body)

    return {
        "email_type": "atlas_notification", # Used to distinguish from normal registration/payment emails
        "instructor_name": instructor_match.group(1).strip() if instructor_match else "",
        "course": course_match.group(1).strip() if course_match else "",
        "date": date_match.group(1).strip() if date_match else ""
    }

def parse_notification_email_flexible(email_body: str) -> dict:
    """Extract course and date from unstructured notification emails."""
    email_body = normalize_email_body(email_body)
    course_match = re.search(r"enrollment requests for (.+?) on", email_body, re.IGNORECASE)
    date_match = re.search(r"on (\d{2}/\d{2}/\d{4})", email_body)

    return {
        "course": course_match.group(1).strip() if course_match else "",
        "date": date_match.group(1).strip() if date_match else ""
    }
# Main Processing Function

def process_emails(messages, source_type="AHA"):
    """Process list of emails and extract registration/payment records."""
    required_fields = ["name", "phone", "email", "course", "date", "location"]
    emails_seen = set()
    all_records = []

    # System emails to ignore
    system_emails = {"atlas.support@heart.org"}

    for msg in messages:
        email_body = normalize_email_body(msg.get("body", {}).get("content") or msg.get("bodyPreview", ""))

        # Atlas notifications
        if "incoming class enrollment requests" in email_body.lower():
            # Use the dedicated Atlas parser
            atlas_record = parse_atlas_notification_email(email_body)
            all_records.append(atlas_record)  # Keep as separate record
            continue  # Skip the normal registration/payment parsing for this email
        
        # Parse registration info
        reg_record = parse_registration_email(email_body)
        email_lower = reg_record.get("email")

        # Skip duplicates
        if email_lower in emails_seen:
            continue

        # Merge notification info if present
        notif = parse_notification_email_flexible(email_body)
        if notif.get("course") and notif.get("date"):
            reg_record.update({
                "course": notif.get("course"),
                "date": notif.get("date")
            })
            if email_lower in system_emails or not reg_record.get("name"):
                reg_record["partial_record"] = True

        # Skip emails with no usable info
        if not reg_record.get("name") and not reg_record.get("email") and not reg_record.get("course"):
            print(f"Skipping email with no usable student info: {email_lower or 'unknown'}")
            continue

        # Apply RQI defaults if needed
        if source_type.upper() == "RQI":
            reg_record.update({"aha_registered": "N", "payment_status": "Paid", "rqi_uploaded": "Y"})

        # Append registration
        all_records.append(reg_record)
        if email_lower:
            emails_seen.add(email_lower)

        # Parse payment info and merge if email exists
        pay_record = parse_payment_email(email_body)
        pay_email_lower = pay_record.get("email")
        if pay_email_lower in emails_seen and pay_record.get("transaction_id"):
            for r in all_records:
                if r.get("email") == pay_email_lower:
                    r.update(pay_record)

    return all_records
# Demo / Test Run
if __name__ == "__main__":
    test_messages = [
        {"bodyPreview": "<p>Name: John Doe</p><p>Phone: 555-111-2222</p><p>Email: john@example.com</p><p>Course: BLS</p><p>Date: 2026/02/19</p><p>Location: Sacramento, CA</p>"},
        {"bodyPreview": "<p>Name: John Doe</p><p>Phone: 555-111-2222</p><p>Email: john@example.com</p><p>Transaction ID: 67676</p>"},
        {"bodyPreview": "<p>Dear Test,</p><p>You have one or more incoming class enrollment requests for BLS Provider Course on 05/04/2026.</p><p>Sincerely,</p><p>AHA Atlas Support</p>"}
    ]

    records = process_emails(test_messages)

    print("\nAll extracted records:\n")
    for i, r in enumerate(records, 1):
        print(f"Record #{i} (Full)" if not r.get("partial_record") else f"Record #{i} (Partial/System)")
        for key, value in r.items():
            print(f"{key}: {value}")
        print("-" * 40)