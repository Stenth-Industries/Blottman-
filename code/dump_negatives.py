"""Dump existing negative keywords for 'Traffic ticket lawyer broad':
campaign-level negatives + contents of every attached negative shared set.
So we add only the gaps (parking + competitor/junk leaks)."""
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
ga = client.get_service("GoogleAdsService")
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
NAME = "Traffic ticket lawyer broad"

print("\n=== CAMPAIGN-LEVEL negative keywords ===")
any_c = False
for r in ga.search(customer_id=cid, query=f"""
    SELECT campaign_criterion.keyword.text, campaign_criterion.keyword.match_type
    FROM campaign_criterion
    WHERE campaign.name='{NAME}' AND campaign_criterion.type='KEYWORD'
      AND campaign_criterion.negative=TRUE"""):
    any_c = True
    k = r.campaign_criterion.keyword
    print(f"   [{k.match_type.name[:3]}] {k.text}")
if not any_c: print("   (none)")

print("\n=== ATTACHED negative SHARED SETS + their contents ===")
sets = []
for r in ga.search(customer_id=cid, query=f"""
    SELECT shared_set.id, shared_set.name, shared_set.resource_name
    FROM campaign_shared_set WHERE campaign.name='{NAME}'"""):
    sets.append((r.shared_set.id, r.shared_set.name, r.shared_set.resource_name))
for sid, sname, sres in sets:
    print(f"\n   --- {sname} (id {sid}) ---")
    n = 0
    for r in ga.search(customer_id=cid, query=f"""
        SELECT shared_criterion.keyword.text, shared_criterion.keyword.match_type
        FROM shared_criterion WHERE shared_set.id={sid}"""):
        k = r.shared_criterion.keyword
        if k.text:
            n += 1
            print(f"      [{k.match_type.name[:3]}] {k.text}")
    print(f"      ({n} keyword negatives)")
print()
