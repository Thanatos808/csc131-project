import re
# same logic but just for parse emails 
# parse registration email

def parse_registration_email(email_body):
   
    # Use regex to find each field, stop at newline
    name_match = re.search(r"Name[:=\-]?\s*(.+?)(?:\n|$)", email_body, re.IGNORECASE)
    phone_match = re.search(r"Phone[:=\-]?\s*(.+?)(?:\n|$)", email_body, re.IGNORECASE)
    email_match = re.search(r"Email[:=\-]?\s*(.+?)(?:\n|$)", email_body, re.IGNORECASE)
    course_match = re.search(r"(?:Course|Class)[:=\-]?\s*(.+?)(?:\n|$)", email_body, re.IGNORECASE)
    date_match = re.search(r"Date[:=\-]?\s*(.+?)(?:\n|$)", email_body, re.IGNORECASE)

    return {
        "name": name_match.group(1).strip() if name_match else "",
        "phone": phone_match.group(1).strip() if phone_match else "",
        "email": email_match.group(1).strip().lower() if email_match else "",
        "course": course_match.group(1).strip() if course_match else "",
        "date": date_match.group(1).strip() if date_match else "",
        "aha_registered": "Y",
        "payment_status": "Pending",
        "rqi_uploaded": "N",
        "reminder_sent": "N"
    }

def parse_payment_email(email_body):
   
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