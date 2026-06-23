"""Staged test: repoint the 2 ENABLED RSAs in 'Traffic ticket lawyer broad'
(23039650759) from blottman.com to blottman.ca. Only these two ads; paused ads
left as-is. Final-URL change = ad re-review (hrs to ~1 business day), no
bid-strategy learning reset."""
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
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
NEW_URL = "https://blottman.ca/"
ENABLED_ADS = ["812451424746", "812455198290"]

svc = client.get_service("AdService")
ops = []
for ad_id in ENABLED_ADS:
    op = client.get_type("AdOperation")
    ad = op.update
    ad.resource_name = svc.ad_path(cid, ad_id)
    ad.final_urls.append(NEW_URL)
    op.update_mask.paths.append("final_urls")
    ops.append(op)

resp = svc.mutate_ads(customer_id=cid, operations=ops)
for r in resp.results:
    print("  repointed:", r.resource_name, "->", NEW_URL)
print("\n  Done. Both enabled broad RSAs now point to blottman.ca (re-review pending).")
