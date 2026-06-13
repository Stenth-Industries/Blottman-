"""Today's leads in detail: conversion actions by campaign + call details (call_view)."""
import os, logging
from dotenv import load_dotenv
from google.ads.googleads.client import GoogleAdsClient

logging.getLogger("google.ads.googleads").setLevel(logging.WARNING)
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
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
ga = client.get_service("GoogleAdsService")

import sys
PERIOD = sys.argv[1].upper() if len(sys.argv) > 1 else "TODAY"

print(f"\n  === {PERIOD}: conversions by campaign x action (all_conversions) ===")
q1 = f"""
    SELECT campaign.name, segments.conversion_action_name,
           metrics.all_conversions
    FROM campaign
    WHERE segments.date DURING {PERIOD}
      AND metrics.all_conversions > 0
"""
rows = list(ga.search(customer_id=cid, query=q1))
if not rows:
    print("  (none yet)")
for r in rows:
    print(f"  {r.campaign.name[:35]:35} | {r.segments.conversion_action_name[:30]:30} | {r.metrics.all_conversions:.1f}")

print("\n  === CALL DETAILS (call_view, most recent first) ===")
q2 = """
    SELECT call_view.start_call_date_time, call_view.call_duration_seconds,
           call_view.caller_country_code, call_view.caller_area_code,
           call_view.call_status, call_view.type, campaign.name
    FROM call_view
"""
try:
    rows = list(ga.search(customer_id=cid, query=q2))
    rows.sort(key=lambda r: r.call_view.start_call_date_time, reverse=True)
    if not rows:
        print("  (no call records)")
    for r in rows[:25]:
        cv = r.call_view
        print(f"  {cv.start_call_date_time} | {cv.call_duration_seconds:>4}s | "
              f"+{cv.caller_country_code} {cv.caller_area_code} | {cv.call_status.name:9} | "
              f"{cv.type_.name:14} | {r.campaign.name[:28]}")
    if len(rows) > 25:
        print(f"  ... ({len(rows)} total records)")
except Exception as e:
    print(f"  call_view error: {e}")
