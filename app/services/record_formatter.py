def format_for_intake(record):
    """Format parsed record to expected intake structure."""
    return {
        "student_name": record.get("name"),
        "email": record.get("email"),
        "phone": record.get("phone"),
        "course": record.get("course"),
        "class_date": record.get("date"),
        "location": record.get("location"),
    }