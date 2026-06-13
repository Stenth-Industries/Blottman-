"""Daily call-conversion watch — Blottman Law.

Run each morning:  python stenth_watch.py

Shows every call-related conversion action firing by day for the last 14 days,
so you can confirm the new STENTH $500 action starts flowing after the
June 9 switch. If STENTH is still flat ~5-7 days after Jun 9, it's misconfigured
(not just lagging) and needs a closer look.
"""

from dotenv import load_dotenv
import os
import logging
from collections import defaultdict
from google.ads.googleads.client import GoogleAdsClient

# Silence the Google Ads client's per-request INFO logging
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
ga = client.get_service("GoogleAdsService")
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")

# Which conversion actions are call-related (everything else is hidden to reduce noise)
CALL_KEYWORDS = ("call", "stenth", "phone")

rows = list(ga.search(customer_id=cid, query="""
    SELECT segments.date, segments.conversion_action_name,
           metrics.all_conversions, metrics.all_conversions_value
    FROM customer
    WHERE segments.date DURING LAST_14_DAYS
    ORDER BY segments.date
"""))

# day -> action -> [count, value]
data = defaultdict(lambda: defaultdict(lambda: [0.0, 0.0]))
actions = set()
for r in rows:
    name = r.segments.conversion_action_name
    if not any(k in name.lower() for k in CALL_KEYWORDS):
        continue
    data[str(r.segments.date)][name][0] += r.metrics.all_conversions
    data[str(r.segments.date)][name][1] += r.metrics.all_conversions_value
    actions.add(name)

if not actions:
    print("No call-related conversions in the last 14 days.")
    raise SystemExit

actions = sorted(actions)
print("\n  Call-conversion activity - last 14 days\n")
header = "  {:<12}".format("Date") + "".join(f"{a[:22]:>24}" for a in actions)
print(header)
print("  " + "-" * (len(header) - 2))

totals = defaultdict(lambda: [0.0, 0.0])
for day in sorted(data):
    cells = ""
    for a in actions:
        c, v = data[day][a]
        totals[a][0] += c
        totals[a][1] += v
        cells += f"{(str(int(c)) if c else '.'):>24}"
    print(f"  {day:<12}" + cells)

print("  " + "-" * (len(header) - 2))
tcells = "".join(f"{int(totals[a][0]):>24}" for a in actions)
print("  {:<12}".format("14d total") + tcells)

# Verdict on STENTH
stenth = next((a for a in actions if "stenth" in a.lower()), None)
print()
if stenth:
    n = int(totals[stenth][0])
    if n == 0:
        print(f"  STENTH: still 0 over 14 days. If it's been >5 days since the Jun 9 switch,")
        print(f"          this is likely MISCONFIGURED, not lagging — investigate.")
    else:
        print(f"  STENTH: {n} call(s) recorded — it's FLOWING. Migration working.")
else:
    print("  STENTH action not present in call data yet (no calls attributed since switch).")
print()
