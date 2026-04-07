from app.services.read_emails import get_access_token, read_emails
from app.services.email_parsing import process_emails
import requests
from app.services.atlas_automation import run as atlas_run
from playwright.sync_api import Playwright, sync_playwright

def run_email_pipeline(): 

    # Step 1: Get access token + fetch emails
    token = get_access_token()
    emails = read_emails(token)

    # Step 2: Filter and prepare messages
    messages = []
    for e in emails:
        content = e.get("body", {}).get("content", "")
        content_lower = content.lower()
        # Only include emails likely containing registrations
        if "course" in content_lower or "enrollment" in content_lower:
            messages.append({"body": e.get("body", {})})

    print(f"Processing {len(messages)} filtered emails...\n")
    records = process_emails(messages)

    # Step 3: Run Atlas automation to register students
    print("\nRunning Atlas automation...\n")
    atlas_emails = [r for r in records if r.get("email_type") == "atlas_notification"] # Atlas notifications ONLY
    results = []
    with sync_playwright() as playwright:
        for email in atlas_emails:
            instructor_name = email.get("instructor_name")
            date_str = email.get("date")
            print(f"Registering student for instructor {instructor_name} on {date_str}...")
            try:
                result = atlas_run(playwright, instructor_name, date_str)
                results.append(result)
            except Exception as e: # Catch errors to allow processing other emails
                print(f"Error registering: {e}")
    print("\n=== Registration Results ===\n")
    for r in results:
        print(r)
    return results, records
    # Print extracted records

    # print("\nAll extracted records:\n")
    # for i, r in enumerate(records, 1):
    #     # Mark system/partial records
    #     record_type = "Partial/System" if r.get("partial_record") else "Full"
    #     print(f"Record #{i} ({record_type})")
    #     for key, value in r.items():
    #         print(f"{key}: {value}")
    #     print("-" * 40)

if __name__ == "__main__":
    run_email_pipeline()