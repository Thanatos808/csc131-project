from app.read_emails import get_access_token, read_emails
from app.email_parsing import process_emails
import requests
from app.atlas_automation import run as atlas_run
from playwright.sync_api import Playwright, sync_playwright

def main(): 

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
    main()