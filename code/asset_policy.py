"""One-off: asset-group + asset-level policy approval status — Blottman Law.
Pinpoints which asset(s) are LIMITED/DISAPPROVED and the policy topic."""
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

# Asset group primary status
print("\n  Asset groups: status + reasons\n")
for r in ga.search(customer_id=cid, query="""
    SELECT asset_group.name, asset_group.primary_status,
           asset_group.primary_status_reasons, campaign.name
    FROM asset_group
    WHERE asset_group.status = 'ENABLED'
"""):
    ag = r.asset_group
    reasons = ", ".join(x.name for x in ag.primary_status_reasons) or "-"
    print(f"  [{r.campaign.name[:24]}] {ag.name[:24]:<25} "
          f"primary={ag.primary_status.name}  reasons={reasons}")

# Asset-level approval within asset groups
print("\n  Assets NOT fully approved (limited/disapproved)\n")
print(f"  {'Field':<16}{'Approval':<14}{'Review':<12}Text/Topic")
print("  " + "-"*72)
any_bad = False
for r in ga.search(customer_id=cid, query="""
    SELECT asset_group_asset.field_type, asset_group_asset.policy_summary.approval_status,
           asset_group_asset.policy_summary.review_status,
           asset_group_asset.policy_summary.policy_topic_entries,
           asset.type, asset.text_asset.text, asset.name
    FROM asset_group_asset
    WHERE asset_group_asset.status = 'ENABLED'
"""):
    ps = r.asset_group_asset.policy_summary
    appr = ps.approval_status.name
    if appr in ("APPROVED", "UNKNOWN", "UNSPECIFIED"):
        continue
    any_bad = True
    topics = ", ".join(t.topic for t in ps.policy_topic_entries) or "-"
    txt = r.asset.text_asset.text or r.asset.name or r.asset.type_.name
    print(f"  {r.asset_group_asset.field_type.name[:15]:<16}{appr:<14}"
          f"{ps.review_status.name[:11]:<12}{txt[:28]} | {topics}")
if not any_bad:
    print("  (no individually disapproved assets — limitation may be at group/account policy level)")
print()
