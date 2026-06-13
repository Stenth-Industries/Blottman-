"""Add catch-all BROAD negatives to 'Master Negatives - Blottman (Stenth)' (12109076551):
  [BRO] parking    -> blocks ANY query containing 'parking' (the gap: only multi-word
                      parking negs existed; standalone is strictly broader coverage)
  [BRO] immigration -> PMAX #2 was serving on 'immigration lawyers' (off-target, not covered)
Directly addresses Les's Jun-14 complaint (parking + irrelevant calls). Skips if present.
NOTE: negatives suppress Search + PMAX search themes, but NOT PMAX insight-category /
Final-URL-Expansion leak -> that requires the UI 'Final URL Expansion OFF' toggle."""
from dotenv import load_dotenv
import os, logging
from google.ads.googleads.client import GoogleAdsClient
logging.getLogger("google.ads.googleads").setLevel(logging.WARNING)
load_dotenv()
cfg = {k: os.getenv(v) for k, v in {
    "developer_token":"GOOGLE_ADS_DEVELOPER_TOKEN","client_id":"GOOGLE_ADS_CLIENT_ID",
    "client_secret":"GOOGLE_ADS_CLIENT_SECRET","refresh_token":"GOOGLE_ADS_REFRESH_TOKEN",
    "login_customer_id":"GOOGLE_ADS_LOGIN_CUSTOMER_ID"}.items()}
cfg["use_proto_plus"] = True
client = GoogleAdsClient.load_from_dict(cfg)
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
ga = client.get_service("GoogleAdsService")

SHARED_SET = f"customers/{cid}/sharedSets/12109076551"
NEW = ["parking", "immigration"]  # all BROAD

rows = ga.search(customer_id=cid, query=f"""
    SELECT shared_criterion.keyword.text, shared_criterion.keyword.match_type
    FROM shared_criterion
    WHERE shared_criterion.shared_set='{SHARED_SET}' AND shared_criterion.type='KEYWORD'""")
existing = {r.shared_criterion.keyword.text.lower() for r in rows}
to_add = [t for t in NEW if t.lower() not in existing]
for t in NEW:
    if t.lower() in existing: print(f"  skip (already present): {t}")

if to_add:
    svc = client.get_service("SharedCriterionService")
    ops = []
    for text in to_add:
        op = client.get_type("SharedCriterionOperation")
        op.create.shared_set = SHARED_SET
        op.create.keyword.text = text
        op.create.keyword.match_type = client.enums.KeywordMatchTypeEnum.BROAD
        ops.append(op)
    res = svc.mutate_shared_criteria(customer_id=cid, operations=ops)
    print(f"\n  Added {len(res.results)} BROAD negatives to Master Negatives:")
    for text in to_add: print(f"    [BRO] {text}")
else:
    print("  Nothing to add.")
