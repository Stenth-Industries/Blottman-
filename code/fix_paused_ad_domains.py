"""Fix Google's 'One website per ad group' disapproval on the broad campaign's
ad group 186398312300 (Traffic ticket lawyer broad / 23039650759).

Context: the blottman.ca migration test (Jun 23) repointed only the 2 ENABLED
RSAs to blottman.ca and left 2 PAUSED ads on blottman.com. Google's
'One website per ad group' rule counts active AND paused ads, so the .ca/.com
mix disapproved the whole ad group (incl. the live ads -> 'This ad can't run').

Fix: repoint the 2 PAUSED ads to blottman.ca so all 4 ads share one TLD. They
stay PAUSED; this only clears the domain conflict. Reversible (just set the URL
back). No keyword-level final URLs exist in this ad group.

Reusable: when migrating other campaigns to blottman.ca, sweep their PAUSED ads
too or you'll hit the same disapproval. Edit CAMPAIGN_ID / PAUSED_ADS / NEW_URL.

Run: python code/fix_paused_ad_domains.py
"""
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
svc = client.get_service("AdService")

NEW_URL = "https://blottman.ca/"
PAUSED_ADS = ["774748697421", "812451172230"]  # the 2 paused .com ads in ag 186398312300

ops = []
for ad_id in PAUSED_ADS:
    op = client.get_type("AdOperation")
    ad = op.update
    ad.resource_name = svc.ad_path(cid, ad_id)
    del ad.final_urls[:]
    ad.final_urls.append(NEW_URL)
    op.update_mask.paths.append("final_urls")
    ops.append(op)

resp = svc.mutate_ads(customer_id=cid, operations=ops)
for r in resp.results:
    print("  repointed paused:", r.resource_name, "->", NEW_URL)
print("\n  Done. All ads in the ad group now share one TLD (blottman.ca) -> "
      "'one website per ad group' conflict cleared. Disapproval re-checks in hrs-~1 business day.")
