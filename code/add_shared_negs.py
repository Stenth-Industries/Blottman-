"""Add competitor + DIY-intent PHRASE negatives to the shared list
'Master Negatives - Blottman (Stenth)' (12109076551) so Search AND PMAX benefit.
Skips terms already in the list; verifies campaign attachments after."""
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

SHARED_SET_ID = "12109076551"  # Master Negatives - Blottman (Stenth)
SHARED_SET = f"customers/{cid}/sharedSets/{SHARED_SET_ID}"

NEW_NEGS = [
    # competitor names seen in Jun-11 search terms (people seeking a specific firm)
    "kaelah mizzi",
    "nextlaw",
    "ontario legal ltd",
    "ott legal",
    "nikbakht law",
    "brian mcleod",
    # DIY/self-serve intent (court's own free processes / not hiring anyone)
    "early resolution",
    "paying",
    "pay ticket",
    "lost my ticket",
]

# 1) what's already in the list?
rows = ga.search(customer_id=cid, query=f"""
    SELECT shared_criterion.keyword.text, shared_criterion.keyword.match_type
    FROM shared_criterion
    WHERE shared_criterion.shared_set = '{SHARED_SET}'
      AND shared_criterion.type = 'KEYWORD'
""")
existing = {r.shared_criterion.keyword.text.lower() for r in rows}
print(f"  Shared list has {len(existing)} keyword negatives already.")

to_add = [t for t in NEW_NEGS if t.lower() not in existing]
skipped = [t for t in NEW_NEGS if t.lower() in existing]
for t in skipped:
    print(f"    skip (already present): {t}")

# 2) add the new ones as PHRASE
if to_add:
    svc = client.get_service("SharedCriterionService")
    ops = []
    for text in to_add:
        op = client.get_type("SharedCriterionOperation")
        sc = op.create
        sc.shared_set = SHARED_SET
        sc.keyword.text = text
        sc.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
        ops.append(op)
    res = svc.mutate_shared_criteria(customer_id=cid, operations=ops)
    print(f"\n  Added {len(res.results)} PHRASE negatives to Master Negatives:")
    for text, r in zip(to_add, res.results):
        print(f"    [PHR] {text}")
else:
    print("  Nothing to add.")

# 3) which campaigns is the list attached to?
rows = ga.search(customer_id=cid, query=f"""
    SELECT campaign.name, campaign.status, campaign.advertising_channel_type
    FROM campaign_shared_set
    WHERE campaign_shared_set.shared_set = '{SHARED_SET}'
      AND campaign_shared_set.status = 'ENABLED'
""")
print("\n  List is attached to (enabled links):")
for r in rows:
    print(f"    {r.campaign.status.name:8} {r.campaign.advertising_channel_type.name:16} {r.campaign.name}")
