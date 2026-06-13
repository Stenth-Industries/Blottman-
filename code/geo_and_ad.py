"""Look up geo target constants for the converting cities + check the ad's approval.
Read-only. Prep for enabling 'Traffic ticket lawyer broad'."""
from dotenv import load_dotenv
import os, logging
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
ga = client.get_service("GoogleAdsService")
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
NAME = "Traffic ticket lawyer broad"

print("\n  GEO TARGET CONSTANTS (Ontario cities):")
for city in ("Toronto", "Brampton", "Mississauga", "Hamilton"):
    for r in ga.search(customer_id=cid, query=f"""
        SELECT geo_target_constant.id, geo_target_constant.canonical_name,
               geo_target_constant.target_type, geo_target_constant.status
        FROM geo_target_constant
        WHERE geo_target_constant.name = '{city}'
          AND geo_target_constant.country_code = 'CA'
          AND geo_target_constant.status = 'ENABLED'
    """):
        g = r.geo_target_constant
        if "Ontario" in g.canonical_name:
            print(f"    {g.id:>10}  {g.target_type:<12} {g.canonical_name}")

print("\n  AD APPROVAL in this campaign:")
for r in ga.search(customer_id=cid, query=f"""
    SELECT ad_group_ad.ad.id, ad_group_ad.ad.type,
           ad_group_ad.policy_summary.approval_status,
           ad_group_ad.policy_summary.review_status,
           ad_group_ad.status
    FROM ad_group_ad
    WHERE campaign.name = '{NAME}' AND ad_group_ad.status != 'REMOVED'
"""):
    a = r.ad_group_ad
    ps = a.policy_summary
    print(f"    ad {a.ad.id} ({a.ad.type_.name})  status={a.status.name}  "
          f"approval={ps.approval_status.name}  review={ps.review_status.name}")

print("\n  CALL/PHONE assets at campaign or account level:")
found = False
for r in ga.search(customer_id=cid, query=f"""
    SELECT asset.type, asset.call_asset.phone_number, campaign.name
    FROM campaign_asset
    WHERE campaign.name = '{NAME}' AND asset.type = 'CALL'
"""):
    found = True
    print(f"    campaign-level CALL: {r.asset.call_asset.phone_number}")
for r in ga.search(customer_id=cid, query="""
    SELECT asset.type, asset.call_asset.phone_number
    FROM customer_asset WHERE asset.type = 'CALL'
"""):
    found = True
    print(f"    account-level CALL: {r.asset.call_asset.phone_number}")
if not found:
    print("    (no call assets found — calls would rely on website click-to-call)")
print()
