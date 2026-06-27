"""Go-live flip for the consolidated Search campaign (23971101309). Safe + idempotent.
Checks every RSA's approval/review. Decision:
  - any DISAPPROVED        -> ABORT, report which (do NOT flip).
  - any still UNDER_REVIEW  -> NOT READY, report (run again later).
  - all APPROVED/_LIMITED   -> ENABLE new campaign + PAUSE the 4 old Search campaigns.
Run: python code/go_live_search.py        (auto-decides; --check = report only, never mutate)
"""
from dotenv import load_dotenv
import os, sys, logging
from google.ads.googleads.client import GoogleAdsClient
logging.getLogger("google.ads.googleads").setLevel(logging.CRITICAL)
load_dotenv()
cfg={k:os.getenv(v) for k,v in {"developer_token":"GOOGLE_ADS_DEVELOPER_TOKEN","client_id":"GOOGLE_ADS_CLIENT_ID","client_secret":"GOOGLE_ADS_CLIENT_SECRET","refresh_token":"GOOGLE_ADS_REFRESH_TOKEN","login_customer_id":"GOOGLE_ADS_LOGIN_CUSTOMER_ID"}.items()}
cfg["use_proto_plus"]=True
client=GoogleAdsClient.load_from_dict(cfg); ga=client.get_service("GoogleAdsService")
cid=os.getenv("GOOGLE_ADS_CUSTOMER_ID")
NEW=23971101309
OLD=[23002273381, 23039650759, 22780000236, 22780001277]  # TTL, broad, LowerVal-New, HigherVal-New
CHECK_ONLY = "--check" in sys.argv

ready, pending, disapproved = [], [], []
for r in ga.search(customer_id=cid, query=f"""SELECT ad_group.name,
    ad_group_ad.policy_summary.approval_status, ad_group_ad.policy_summary.review_status
    FROM ad_group_ad WHERE campaign.id={NEW}"""):
    ap=r.ad_group_ad.policy_summary.approval_status.name
    rv=r.ad_group_ad.policy_summary.review_status.name
    nm=r.ad_group.name
    if ap=="DISAPPROVED": disapproved.append((nm,ap,rv))
    elif ap in ("APPROVED","APPROVED_LIMITED") and rv=="REVIEWED": ready.append(nm)
    else: pending.append((nm,ap,rv))

print(f"ads: {len(ready)} ready | {len(pending)} pending | {len(disapproved)} disapproved")
for nm,ap,rv in disapproved: print(f"  DISAPPROVED: {nm} ({ap}/{rv})")
for nm,ap,rv in pending: print(f"  pending: {nm} ({ap}/{rv})")

if disapproved:
    print("\nABORT - disapprovals present. Fix before going live. No changes made."); sys.exit(2)
if pending:
    print("\nNOT READY - still under review. Run again later. No changes made."); sys.exit(3)
if not ready:
    print("\nNo ads found - aborting."); sys.exit(4)
if CHECK_ONLY:
    print("\nALL APPROVED. (--check mode: no changes made.)"); sys.exit(0)

# FLIP: enable new, pause old 4
cs=client.get_service("CampaignService")
def set_status(camp_id, status):
    op=client.get_type("CampaignOperation")
    op.update.resource_name=f"customers/{cid}/campaigns/{camp_id}"
    op.update.status=getattr(client.enums.CampaignStatusEnum, status)
    op.update_mask.paths.append("status")
    cs.mutate_campaigns(customer_id=cid, operations=[op])

set_status(NEW, "ENABLED"); print(f"\nENABLED new campaign {NEW}")
for o in OLD:
    set_status(o, "PAUSED"); print(f"PAUSED old campaign {o}")
print("\nLIVE. New consolidated Search is serving; 4 old Search campaigns paused. Total stays $100/day.")
