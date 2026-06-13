"""Inspect paused SEARCH campaigns — structure + keywords + any lifetime stats.
Helps pick ONE tight high-intent campaign to flip on as an emergency lead tap."""
from dotenv import load_dotenv
import os, logging
from collections import defaultdict
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

# Keywords per paused search campaign
data = defaultdict(list)
for r in ga.search(customer_id=cid, query="""
    SELECT campaign.name, ad_group.name, ad_group_criterion.keyword.text,
           ad_group_criterion.keyword.match_type, ad_group_criterion.status
    FROM keyword_view
    WHERE campaign.advertising_channel_type = 'SEARCH'
      AND campaign.status = 'PAUSED'
      AND ad_group_criterion.negative = FALSE
"""):
    k = r.ad_group_criterion.keyword
    data[r.campaign.name].append(f"[{k.match_type.name[:3]}] {k.text}")

for camp in sorted(data):
    kws = data[camp]
    print(f"\n  === {camp}  ({len(kws)} keywords) ===")
    for kw in kws[:18]:
        print(f"      {kw}")
    if len(kws) > 18:
        print(f"      ... +{len(kws)-18} more")
print()
