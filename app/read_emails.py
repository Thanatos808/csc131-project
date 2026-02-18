import msal
import requests
import json

# Credentials
CLIENT_ID = "19c09051-a817-4669-ab5f-55d43b192816"
TENANT = "common"  # allows personal Microsoft accounts
AUTHORITY = f"https://login.microsoftonline.com/common"

SCOPES = ['https://graph.microsoft.com/Mail.Read', 'https://graph.microsoft.com/User.Read']  # Permission to read emails

GRAPH_ENDPOINT = "https://graph.microsoft.com/v1.0/me/messages" # graph api


def get_access_token():
    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority=AUTHORITY
    )

    flow = app.initiate_device_flow(scopes = SCOPES)  # oauth device flow

    print(flow["message"])  # Shows login instructions

    result = app.acquire_token_by_device_flow(flow)

    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception("Authentication failed")


def read_emails(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "$select": "subject,from,receivedDateTime,bodyPreview",
        "$top": 10
    }

    response = requests.get(GRAPH_ENDPOINT, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"Graph API Error: {response.status_code}\n{response.text}")

    emails = response.json().get("value", [])

    print("\nEMAIL RESULTS\n")

    for i, email in enumerate(emails, start=1):
        subject = email.get("subject", "No Subject")
        sender = email.get("from", {}).get("emailAddress", {}).get("address", "Unknown")
        received = email.get("receivedDateTime", "Unknown")
        preview = email.get("bodyPreview", "")

        print(f"Email #{i}")
        print(f"From: {sender}")
        print(f"Subject: {subject}")
        print(f"Received: {received}")
        print(f"Preview: {preview}")
        print("-" * 50)


if __name__ == "__main__":
    token = get_access_token()
    read_emails(token)
