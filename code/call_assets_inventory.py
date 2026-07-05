"""Read-only: list all CALL assets, their phone numbers, existing ad schedules,
and which ENABLED campaigns/account they serve on. Pre-step for adding the
answerable-hours schedule (call_asset_schedule.py)."""
from dotenv import load_dotenv
import os, logging
from google.ads.googleads.client import GoogleAdsClient
logging.getLogger("google.ads.googleads").setLevel(logging.WARNING)
load_dotenv()
cfg = {
    "developer_token": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
    "client_id": os.getenv("GOOGLE_ADS_CLIENT_ID"),
    "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
    "refresh_token": os.getenv("GOOGLE_ADS_REFRESH_TOKEN"),
    "login_customer_id": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),
    "use_proto_plus": True,
}
client = GoogleAdsClient.load_from_dict(cfg)
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
ga = client.get_service("GoogleAdsService")

def fmt_sched(a):
    if not a.call_asset.ad_schedule_targets:
        return "NO SCHEDULE (shows 24/7)"
    return "; ".join(
        f"{s.day_of_week.name} {s.start_hour}:00-{s.end_hour}:00"
        for s in a.call_asset.ad_schedule_targets
    )

print("=== ALL CALL ASSETS ===")
assets = {}
for r in ga.search(customer_id=cid, query="""
    SELECT asset.resource_name, asset.id, asset.call_asset.phone_number,
           asset.call_asset.country_code, asset.call_asset.ad_schedule_targets
    FROM asset WHERE asset.type = 'CALL'
"""):
    assets[r.asset.id] = r.asset
    print(f"  asset {r.asset.id} | {r.asset.call_asset.phone_number} | {fmt_sched(r.asset)}")

print("\n=== CAMPAIGN LINKS (enabled links on non-removed campaigns) ===")
for r in ga.search(customer_id=cid, query="""
    SELECT campaign.name, campaign.status, campaign_asset.asset,
           campaign_asset.status, campaign_asset.field_type
    FROM campaign_asset
    WHERE campaign_asset.field_type = 'CALL' AND campaign_asset.status = 'ENABLED'
      AND campaign.status IN ('ENABLED','PAUSED')
"""):
    aid = r.campaign_asset.asset.split("/")[-1]
    print(f"  {r.campaign.status.name:8} {r.campaign.name[:45]:45} -> asset {aid}")

print("\n=== ACCOUNT-LEVEL LINKS ===")
try:
    for r in ga.search(customer_id=cid, query="""
        SELECT customer_asset.asset, customer_asset.status
        FROM customer_asset
        WHERE customer_asset.field_type = 'CALL' AND customer_asset.status = 'ENABLED'
    """):
        aid = r.customer_asset.asset.split("/")[-1]
        print(f"  account-level -> asset {aid}")
except Exception as e:
    print(f"  (customer_asset query failed: {e})")
