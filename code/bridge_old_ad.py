"""Temporarily re-enable old RSA #1 (774748697421) as a serving bridge while the two
new ads clear review. Re-run with 'pause' arg later to park it once they're approved."""
from dotenv import load_dotenv
import os, sys, logging
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
OLD = f"customers/{cid}/adGroupAds/186398312300~774748697421"
NEW = ["812451172230", "812451424746"]

ga = client.get_service("GoogleAdsService")
want_pause = len(sys.argv) > 1 and sys.argv[1] == "pause"

# Show review status of the two new ads
print("\n  New ads review status:")
all_approved = True
for r in ga.search(customer_id=cid, query=f"""
    SELECT ad_group_ad.ad.id, ad_group_ad.policy_summary.approval_status, ad_group_ad.status
    FROM ad_group_ad WHERE ad_group_ad.ad.id IN ({','.join(NEW)})"""):
    a = r.ad_group_ad
    st = a.policy_summary.approval_status.name
    if st != "APPROVED":
        all_approved = False
    print(f"    ad {a.ad.id}: {st} / {a.status.name}")

svc = client.get_service("AdGroupAdService")
op = client.get_type("AdGroupAdOperation")
op.update.resource_name = OLD
op.update_mask.paths.append("status")
if want_pause:
    op.update.status = client.enums.AdGroupAdStatusEnum.PAUSED
    svc.mutate_ad_group_ads(customer_id=cid, operations=[op])
    print("\n  Old ad PAUSED again (bridge removed).")
    if not all_approved:
        print("  WARNING: not all new ads are APPROVED yet — you may have re-opened a gap.")
else:
    op.update.status = client.enums.AdGroupAdStatusEnum.ENABLED
    svc.mutate_ad_group_ads(customer_id=cid, operations=[op])
    print("\n  Old ad RE-ENABLED as bridge. Re-run with 'pause' once both new ads show APPROVED.")
print()
