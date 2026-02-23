import csv
import re
from typing import List, Dict


# Parse registration email
def parse_registration_email(email_body: str) -> Dict[str, str]:
    """
    Extracts name, phone, email, course, and date from a registration email (location if needed as well).
    Returns a dictionary with default tracking values.
    """
    # Use regex to capture each field, ignoring case and trimming whitespace
    name_match = re.search(r"Name[:=\-]?\s*(.+?)(?:\n|$)", email_body, re.IGNORECASE)
    phone_match = re.search(r"Phone[:=\-]?\s*(.+?)(?:\n|$)", email_body, re.IGNORECASE)
    email_match = re.search(r"Email[:=\-]?\s*(.+?)(?:\n|$)", email_body, re.IGNORECASE)
    course_match = re.search(r"(?:Course|Class)[:=\-]?\s*(.+?)(?:\n|$)", email_body, re.IGNORECASE)
    date_match = re.search(r"Date[:=\-]?\s*(.+?)(?:\n|$)", email_body, re.IGNORECASE)
    location_match = re.search(r"Location[:=\-]?\s*(.+?)(?:\n|$)", email_body, re.IGNORECASE)

    # Return dictionary with parsed data and default tracking feilds 
    return {
        "name": name_match.group(1).strip() if name_match else "",
        "phone": phone_match.group(1).strip() if phone_match else "",
        "email": email_match.group(1).strip().lower() if email_match else "", # lowecase to prevent duplicataes 
        "course": course_match.group(1).strip() if course_match else "",
        "date": date_match.group(1).strip() if date_match else "",
        "location": location_match.group(1).strip() if location_match else "",
        "aha_registered": "Y",        # assumes registration occured -- extra fields 
        "payment_status": "Pending",  # payment not confirmed yet
        "rqi_uploaded": "N",          # not uploaded yet
        "reminder_sent": "N"          # no reminder sent yet
    }

# Parse payment email

def parse_payment_email(email_body: str) -> Dict[str, str]:
    """
    Extracts name, phone, email, and transaction ID from a payment confirmation email.
    Updates payment_status to 'Paid'.
    """
    # regex searches for each field 
    name_match = re.search(r"Name[:=\-]?\s*(.+?)(?:\n|$)", email_body, re.IGNORECASE)
    phone_match = re.search(r"Phone[:=\-]?\s*(.+?)(?:\n|$)", email_body, re.IGNORECASE)
    email_match = re.search(r"Email[:=\-]?\s*(.+?)(?:\n|$)", email_body, re.IGNORECASE)
    transaction_match = re.search(r"Transaction ID[:=\-]?\s*(.+?)(?:\n|$)", email_body, re.IGNORECASE)

    # Returns parsed values and paid stats 
    return {
        "name": name_match.group(1).strip() if name_match else "",
        "phone": phone_match.group(1).strip() if phone_match else "",
        "email": email_match.group(1).strip().lower() if email_match else "",
        "transaction_id": transaction_match.group(1).strip() if transaction_match else "",
        "payment_status": "Paid"
    }

# test - Process CSV for demo purposes
def process_csv(file_path: str, source_type: str) -> List[Dict[str, str]]:
    """
    Reads a CSV file and extracts registration records using the parsing functions.
    Handles duplicate emails and missing required fields.
    """
    required_fields = ["name", "phone", "email", "course", "date", "location"]
    data = []
    emails_seen = set()  # to prevent duplicate entries

    # Open and read csv
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Normalize keys (lowercase) and strip whitespace
            row = {k.strip().lower(): v.strip() for k, v in row.items()}

            # remove extra labels from phone/email columns if present 
            phone_value = re.sub(r"(Phone:|Email:)", "", row.get('phone','')).strip()
            email_value = re.sub(r"(Email:)", "", row.get('email','')).strip()
            email_lower = email_value.lower()

            # Skip empty or duplicate emails
            if not email_lower:
                print("Warning: Empty email, skipping record")
                continue
            if email_lower in emails_seen:
                print(f"Duplicate email skipped: {email_value}")
                continue

            # a simulated email body for parser 
            if source_type.upper() == "AHA":
                email_body = f"""
            Name: {row.get('first name','')} {row.get('last name','')}
            Phone: {phone_value}
            Email: {email_value}
            Course: {row.get('course','')}
            Date: {row.get('date','')}
            Location: {row.get('location', '')}
            """
            else:  # RQI CSV
                email_body = f"""
            Name: {row.get('firstname','')} {row.get('lastname','')}
            Phone: {phone_value}
            Email: {email_value}
            Course: {row.get('jobname','')}
            Date: {row.get('activedate','')}

            """
                
            # Parse email with the proper structure 
            record = parse_registration_email(email_body)

            # Set RQI defaults - marks as paid and uploaded 
            if source_type.upper() == "RQI":
                record.update({"aha_registered": "N", "payment_status": "Paid", "rqi_uploaded": "Y"})

            # Skip if missing required fields
            if not all(record.get(f) for f in required_fields):
                print(f"Warning: Missing required field for {record.get('email','unknown')}, skipping")
                continue

            # Add record and mark email as seen
            data.append(record)
            emails_seen.add(email_lower)

    return data
 # --Demo function for testing 
def demo_email_parsing():
    """
    demo purposes only - email parsing for registration and payment emails, 
    takes what is needed and handle duplicates 
    """
    emails_seen = set()

    # Sample registration email this came from the sheets 
    reg_email = """Name: John Doe
    Phone: 555-111-2222
    Email: john@example.com
    Course: BLS
    Location: GA Exchange
    Date: 2026-02-19"""
    
    reg_record = parse_registration_email(reg_email)
    email_lower = reg_record["email"]

    if not all(reg_record[f] for f in ["name","phone","email","course","date"]): #checks for missing required fields 
        print("Registration email missing fields, skipping")
    elif email_lower in emails_seen:    # checks for duplictes 
        print(f"Duplicate registration skipped: {email_lower}")
    else:
        emails_seen.add(email_lower)
        print("Registration record extracted:")
        print(reg_record)

    # Sample payment email
    pay_email = """Name: John Doe
    Phone: 555-111-2222
    Email: john@example.com
    Transaction ID: 67676"""
    pay_record = parse_payment_email(pay_email)
    email_lower = pay_record["email"]
    # only process if email matches registration 
    if email_lower in emails_seen:
        print("\nPayment record extracted and matched to registration:")
        print(pay_record)
    else:
        print("\nPayment email without matching registration, skipping")

    # Run demo 

if __name__ == "__main__":
    demo_email_parsing()