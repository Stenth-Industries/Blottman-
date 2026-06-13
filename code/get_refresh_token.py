"""Generates a Google Ads refresh token.

Run: python get_refresh_token.py
Opens browser -> "Allow" -> token is printed to your terminal.
"""

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/adwords"]

flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
creds = flow.run_local_server(port=0, prompt="consent", access_type="offline")

print("\n\n=== YOUR REFRESH TOKEN ===")
print(creds.refresh_token)
print("==========================\n")
print("Paste this into .env as GOOGLE_ADS_REFRESH_TOKEN=")
