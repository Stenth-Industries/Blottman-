"""Call breakdown: short / missed / not-connected counts.
Buckets every call by call_status (RECEIVED vs MISSED) and duration (<30s short,
>=30s qualifying). Reports all-time + last 30d + last 7d. Run: python code/call_breakdown.py
"""
from dotenv import load_dotenv
import os, logging, datetime
from google.ads.googleads.client import GoogleAdsClient

logging.getLogger("google.ads.googleads").setLevel(logging.CRITICAL)
load_dotenv()
config = {
    "developer_token": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
    "client_id": os.getenv("GOOGLE_ADS_CLIENT_ID"),
    "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
    "refresh_token": os.getenv("GOOGLE_ADS_REFRESH_TOKEN"),
    "login_customer_id": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),
    "use_proto_plus": True,
}
client = GoogleAdsClient.load_from_dict(config)
ga = client.get_service("GoogleAdsService")
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")

rows = list(ga.search(customer_id=cid, query="""
    SELECT call_view.start_call_date_time, call_view.call_duration_seconds,
           call_view.call_status
    FROM call_view
"""))

today = datetime.date.today()
cut30 = (today - datetime.timedelta(days=30)).isoformat()
cut7 = (today - datetime.timedelta(days=7)).isoformat()

def report(label, data):
    total = len(data)
    missed = sum(1 for r in data if r.call_view.call_status.name == "MISSED")
    received = sum(1 for r in data if r.call_view.call_status.name == "RECEIVED")
    short = sum(1 for r in data if r.call_view.call_duration_seconds < 30)
    qualifying = sum(1 for r in data if r.call_view.call_duration_seconds >= 30)
    # "not connected" practical bucket = missed OR connected-but-short (<30s = hang-up/voicemail)
    not_productive = sum(1 for r in data
                         if r.call_view.call_status.name == "MISSED"
                         or r.call_view.call_duration_seconds < 30)
    print(f"\n  === {label} ===")
    print(f"  Total calls:              {total}")
    print(f"  MISSED (never connected): {missed}")
    print(f"  RECEIVED (connected):     {received}")
    print(f"  Short  (<30s):            {short}")
    print(f"  Qualifying (>=30s):       {qualifying}")
    print(f"  Short OR missed (lost):   {not_productive}")

report("ALL TIME", rows)
report("LAST 30 DAYS", [r for r in rows if r.call_view.start_call_date_time[:10] >= cut30])
report("LAST 7 DAYS", [r for r in rows if r.call_view.start_call_date_time[:10] >= cut7])
