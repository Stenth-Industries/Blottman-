"""Who-changed-what over a recent window — isolates Akash's changes.
Kushagra = info@stenth.com; anything else (non-system) is likely Akash."""

from dotenv import load_dotenv
import os
from google.ads.googleads.client import GoogleAdsClient

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

KUSHAGRA = "info@stenth.com"

# change_event max lookback is 30 days; use an explicit 2-day window.
rows = list(ga.search(customer_id=cid, query="""
    SELECT
        change_event.change_date_time,
        change_event.change_resource_type,
        change_event.changed_fields,
        change_event.resource_name,
        change_event.user_email,
        change_event.client_type,
        change_event.campaign,
        change_event.ad_group
    FROM change_event
    WHERE change_event.change_date_time DURING LAST_14_DAYS
    ORDER BY change_event.change_date_time DESC
    LIMIT 9000
"""))

# group by user
by_user = {}
for r in rows:
    e = r.change_event
    u = e.user_email if e.user_email else f"[{e.client_type.name}]"
    by_user.setdefault(u, []).append(e)

print(f"\nTotal change events (last 14d): {len(rows)}")
print("By user:")
for u, evs in sorted(by_user.items(), key=lambda x: -len(x[1])):
    tag = "  <-- KUSHAGRA" if u == KUSHAGRA else ("  <-- likely AKASH" if "@" in u else "")
    print(f"  {len(evs):>4}  {u}{tag}")

# detail for non-Kushagra human users
print("\n" + "=" * 100)
print("  NON-KUSHAGRA HUMAN CHANGES (Akash et al.)")
print("=" * 100)
for u, evs in by_user.items():
    if u == KUSHAGRA or "@" not in u:
        continue
    print(f"\n### {u}  ({len(evs)} changes)")
    print(f"  {'Time':<20} {'Resource Type':<26} {'Campaign':<14} {'Fields'}")
    print(f"  {'-'*96}")
    for e in evs:
        t = str(e.change_date_time)[:19].replace("T", " ")
        rtype = e.change_resource_type.name
        camp = e.campaign.split("/")[-1] if e.campaign else "—"
        fields = ", ".join(e.changed_fields.paths) if e.changed_fields and e.changed_fields.paths else "—"
        print(f"  {t:<20} {rtype:<26} {camp:<14} {fields}")

print("\nDone.\n")
