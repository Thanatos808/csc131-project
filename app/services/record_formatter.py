def format_for_intake(record):
    """Format parsed record to expected intake structure."""
    return {
        "student_name": record.get("name") or "",
        "email": record.get("email") or "",
        "phone": record.get("phone") or "",
        "course": record.get("course") or "",
        "class_date": record.get("date") or "",
        "location": record.get("location") or "",
    }