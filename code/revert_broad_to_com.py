"""2026-06-24: 'Traffic ticket lawyer broad' (23039650759) ad group 186398312300 is
DISAPPROVED with ONE_WEBSITE_PER_AD_GROUP. Cause: the Jun-23 .ca migration TEST flipped
all 4 ads to blottman.ca, but every campaign sitelink + the lead form still point to
blottman.com (and blottman.ca / landing-v2 is a single page with no /hov-ticket/,
/traffic-violations/ etc. subpages). Ads(.ca) vs sitelinks(.com) = two websites in one
ad group -> whole ad group disapproved.

FIX: revert all 4 ads back to https://blottman.com/ (matches sitelinks, lead form, and
every other campaign in the account). Reversible. The full .ca migration is a deliberate
future project (needs the .ca site to host all subpages, then move ads+sitelinks+leadform
together). Run: python code/revert_broad_to_com.py"""
from dotenv import load_dotenv
import os, logging
from google.ads.googleads.client import GoogleAdsClient
logging.getLogger("google.ads.googleads").setLevel(logging.ERROR)
load_dotenv()
cfg={k:os.getenv(v) for k,v in {"developer_token":"GOOGLE_ADS_DEVELOPER_TOKEN","client_id":"GOOGLE_ADS_CLIENT_ID","client_secret":"GOOGLE_ADS_CLIENT_SECRET","refresh_token":"GOOGLE_ADS_REFRESH_TOKEN","login_customer_id":"GOOGLE_ADS_LOGIN_CUSTOMER_ID"}.items()}
cfg["use_proto_plus"]=True
client=GoogleAdsClient.load_from_dict(cfg)
cid=os.getenv("GOOGLE_ADS_CUSTOMER_ID")
HOME="https://blottman.com/"
ad_ids=["812451424746","812455198290","774748697421","812451172230"]  # 2 enabled + 2 paused

ad_svc=client.get_service("AdService")
ops=[]
for aid in ad_ids:
    op=client.get_type("AdOperation")
    ad=op.update
    ad.resource_name=f"customers/{cid}/ads/{aid}"
    ad.final_urls.append(HOME)
    op.update_mask.paths.append("final_urls")
    ops.append(op)
res=ad_svc.mutate_ads(customer_id=cid, operations=ops)
print(f"Repointed {len(res.results)} broad ads back to {HOME}:")
for aid in ad_ids:
    print(f"  ad {aid} -> {HOME}")
print("\nAll 4 ads + all sitelinks + lead form now share blottman.com.")
print("ONE_WEBSITE_PER_AD_GROUP should clear on re-review (hrs -> ~1 business day).")
print("Verify: python code/approval_status.py")
