"""Call-quality breakdown by campaign: area code + duration, last 7 days.
GTA area codes = 416/647/437/905/289/365. Out-of-area = everything else
(519/226 = SW Ontario near Sarnia/Windsor). Run: python code/call_quality.py
"""
from dotenv import load_dotenv
import os, logging
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

GTA = {"416", "647", "437", "905", "289", "365"}

import datetime
cutoff = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()
rows = list(ga.search(customer_id=cid, query="""
    SELECT call_view.start_call_date_time, call_view.call_duration_seconds,
           call_view.caller_area_code, call_view.call_status, campaign.name
    FROM call_view
"""))
rows = [r for r in rows if r.call_view.start_call_date_time[:10] >= cutoff]
rows.sort(key=lambda r: r.call_view.start_call_date_time, reverse=True)

print("\n  === CALLS, LAST 7 DAYS (area code + duration by campaign) ===")
print(f"  GTA area codes = {sorted(GTA)}; anything else = out-of-area\n")
by_camp = {}
for r in rows:
    cv = r.call_view
    name = r.campaign.name
    ac = cv.caller_area_code or "?"
    region = "GTA" if ac in GTA else "OUT" if ac != "?" else "?"
    by_camp.setdefault(name, []).append((cv.start_call_date_time, cv.call_duration_seconds, ac, region, cv.call_status.name))

for name in sorted(by_camp):
    calls = by_camp[name]
    gta = sum(1 for c in calls if c[3] == "GTA")
    out = sum(1 for c in calls if c[3] == "OUT")
    unk = sum(1 for c in calls if c[3] == "?")
    longcalls = sum(1 for c in calls if c[1] >= 30)
    print(f"  {name}  — {len(calls)} calls | GTA {gta} / OUT {out} / ?{unk} | {longcalls} were >=30s")
    for dt, dur, ac, region, status in calls:
        print(f"      {dt} | {dur:>4}s | area {ac:>3} [{region:3}] | {status}")
    print()
