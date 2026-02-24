# parse_emails.py CSC 131 
import re
from html import unescape


# Email Parsing Functions


def strip_html(html_text: str) -> str:
    """Remove HTML tags and unescape HTML entities."""
    text = re.sub(r"<[^>]+>", "", html_text)
    return unescape(text)

def parse_registration_email(email_body: str) -> dict:
    """Extract registration info from email body."""
    name_match = re.search(r"Name[:=\-]?\s*(.+?)(?:\n|$)", email_body, re.IGNORECASE)
    phone_match = re.search(r"Phone[:=\-]?\s*(.+?)(?:\n|$)", email_body, re.IGNORECASE)
    email_match = re.search(r"Email[:=\-]?\s*(.+?)(?:\n|$)", email_body, re.IGNORECASE)
    course_match = re.search(r"(?:Course|Class)[:=\-]?\s*(.+?)(?:\n|$)", email_body, re.IGNORECASE)
    date_match = re.search(r"Date[:=\-]?\s*(.+?)(?:\n|$)", email_body, re.IGNORECASE)
    location_match = re.search(r"Location[:=\-]?\s*(.+?)(?:\n|$)", email_body, re.IGNORECASE)

    return {
        "name": name_match.group(1).strip() if name_match else "",
        "phone": phone_match.group(1).strip() if phone_match else "",
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
    email_match = re.search(r"Email[:=\-]?\s*(.+?)(?:\n|$)", email_body, re.IGNORECASE)
    transaction_match = re.search(r"Transaction ID[:=\-]?\s*(.+?)(?:\n|$)", email_body, re.IGNORECASE)

    return {
        "name": name_match.group(1).strip() if name_match else "",
        "phone": phone_match.group(1).strip() if phone_match else "",
        "email": email_match.group(1).strip().lower() if email_match else "",
        "transaction_id": transaction_match.group(1).strip() if transaction_match else "",
        "payment_status": "Paid"
    }


# Main Data Extraction Function

def process_emails(messages, source_type="AHA"):
    """
    Process a list of email messages (from Microsoft Graph) and extract registration/payment records.
    Returns a list of registration dictionaries.
    """
    required_fields = ["name","phone","email","course","date","location"]
    emails_seen = set()
    all_records = []

    for msg in messages:
        email_body = msg.get("bodyPreview", "")
        email_body = strip_html(email_body)

        #  Registration parsing 
        reg_record = parse_registration_email(email_body)
        email_lower = reg_record.get("email")

        # Skip missing or duplicate registration
        if not email_lower or email_lower in emails_seen:
            continue
        if not all(reg_record.get(f) for f in required_fields):
            print(f"Warning: Missing required field for {email_lower}, skipping")
            continue

        # Apply RQI defaults if needed
        if source_type.upper() == "RQI":
            reg_record.update({"aha_registered": "N", "payment_status": "Paid", "rqi_uploaded": "Y"})

        all_records.append(reg_record)
        emails_seen.add(email_lower)
        print("Registration record extracted:")
        print(reg_record)
        print("-" * 50)

        # Payment parsing 
        pay_record = parse_payment_email(email_body)
        pay_email_lower = pay_record.get("email")
        if pay_email_lower in emails_seen and pay_record.get("transaction_id"):
            print("Payment record matched to registration:")
            print(pay_record)
            print("-" * 50)

    return all_records

# Optional Demo Run
if __name__ == "__main__":
    # Example test emails
    messages = [
        {"bodyPreview": "<p>Name: John Doe</p><p>Phone: 555-111-2222</p><p>Email: john@example.com</p><p>Course: BLS</p><p>Date: 2026-02-19</p><p>Location: GA Exchange</p>"},
        {"bodyPreview": "<p>Name: John Doe</p><p>Phone: 555-111-2222</p><p>Email: john@example.com</p><p>Transaction ID: 67676</p>"}
    ]
    process_emails(messages)