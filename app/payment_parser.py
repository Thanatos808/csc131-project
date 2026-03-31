
import re

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

PAID_KEYWORDS = [

    #list of words that will determine payment

    "paid",
    "receipt",
    "transaction approved",
    "successful payment",
    "payment confirmation",
    "thank you for your payment",
    "payment received"
    "purchase details",
    "payment date",
    "payment source",
    "payment description",
    "success"

]

NOT_PAID_KEYWORDS = [

    #list of words that will determine no payment 

    "cancelled",
    "canceled",
    "payment failed",
    "payment unsuccessful",
    "payment declined",
    "declined",
    "failed",
    "pending payment",
    "action required"


]
def parse_payment_email(raw_text):
    #checks if there is any text at all
    if raw_text is None or raw_text.strip() == "":
        return {
            "full_name": None,
            "email": None,
            "payment_status": "Unknown",
            "transaction_id": None,
            "amount": None, 
            "raw_detected": False
        }
    
    text = raw_text.strip()
    lower_text = text.lower()

    
    #finds the email
    email = None
    email_match = EMAIL_RE.search(text)
    if email_match:
        email = email_match.group(0)

    #looks for words to confirm no payment 
    payment_status = "Unknown"
    for keyword in NOT_PAID_KEYWORDS:
        if keyword in lower_text:
            payment_status = "Not Paid"
            break

    #looks for words to confirm payment
    if payment_status == "Unknown":
        for keyword in PAID_KEYWORDS:
            if keyword in lower_text:
                payment_status = "Paid"
                break

    #finds an transaction ID
    transaction_id = None

    patterns = [

        #list of typical patterns for transaction IDs

        r"Transaction\s*ID[:\s]+([A-Za-z0-9\-]+)",
        r"Order\s*(?:ID|#)[:\s]+([A-Za-z0-9\-]+)",
        r"Receipt\s*(?:ID|#)[:\s]+([A-Za-z0-9\-]+)",
        r"Confirmation\s*(?:ID|#)[:\s]+([A-Za-z0-9\-]+)",  
        r"Payment\s*(?:ID|#)[:\s]+([A-Za-z0-9\-]+)"

    ]

    for pattern in patterns:
        m = re.search(pattern, text, flags=re.IGNORECASE)
        if m:
            transaction_id = m.group(1).strip()
            break

    full_name = None

    name_patterns = [

        #list of typical naming formats

        r"Name[:\s]+([A-Za-z ,.'\-]+)",
        r"Student\s*Name[:\s]+([A-Za-z ,.'\-]+)",
        r"Customer[:\s]+([A-Za-z ,.'\-]+)",
        r"Billed\s*To[:\s]+([A-Za-z ,.'\-]+)"

    ]

    for pattern in name_patterns:
        m = re.search(pattern, text, flags=re.IGNORECASE)
        if m:
            full_name = m.group(1).strip()
            break

    amount = None

    amount_patterns = [

        #list of typical patterns to print how much something costs

        r"Amount\s*(?:Paid)?[:\s]+\$?([0-9]+(?:\.[0-9]{2})?)",
        r"Total[:\s]+\$?([0-9]+(?:\.[0-9]{2})?)",
        r"Payment\s*Amount[:\s]+\$?([0-9]+(?:\.[0-9]{2})?)"

    ]

    for pattern in amount_patterns:
        m = re.search(pattern, text, flags=re.IGNORECASE)
        if m:
            amount = m.group(1).strip()
            break

    raw_detected = False
    if ("payment" in lower_text) or (transaction_id is not None) or (payment_status != "Unknown"):
        raw_detected = True

    return{

        "full_name": full_name,
        "email": email,
        "payment_status": payment_status,
        "transaction_id": transaction_id,
        "amount": amount,
        "raw_detected": raw_detected
    }






