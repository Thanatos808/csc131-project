from app.services.email_parsing import parse_registration_email, parse_payment_email

# Test registration email parsing
def test_registration_email():
    # Sample registration email body
    email = """Name: John Doe
    Phone: 555-111-2222
    Email: john@email.com
    Course: BLS
    Location: GA Exchange
    Date: 2026-02-19"""

    # Parse the registration email
    record = parse_registration_email(email)

    # Check that all required fields were extracted
    assert record["name"] == "John Doe"
    assert record["phone"] == "555-111-2222"
    assert record["email"] == "john@email.com"
    assert record["course"] == "BLS"
    assert record["date"] == "2026-02-19"
    assert record["payment_status"] == "Pending"

    print("Registration email test passed!")

# Test payment email parsing
def test_payment_email():
    # Sample payment confirmation email body
    email = """Name: Jane Smith
    Phone: 555-222-3333
    Email: jane@email.com
    Transaction ID: 12345"""

    # Parse the payment email
    record = parse_payment_email(email)

    # Check that all required fields were extracted
    assert record["name"] == "Jane Smith"
    assert record["phone"] == "555-222-3333"
    assert record["email"] == "jane@email.com"
    assert record["payment_status"] == "Paid"

    print("Payment email test passed!")

# Run tests
if __name__ == "__main__":
    test_registration_email()
    test_payment_email()