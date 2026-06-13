"""Close the competitor/junk search-term leaks on 'Traffic ticket lawyer broad'.
These leaked because the shared list had them EXACT-only (variants with extra words
slipped through) or not at all. Add as campaign-level PHRASE negatives so any query
containing the brand phrase is blocked. Parking is already broad-covered — not touched."""
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
CAMPAIGN = f"customers/{cid}/campaigns/23039650759"

# Phrase negatives — competitor brands + the junk "ex copper" variant
PHRASE_NEGS = [
    "amar traffic tickets",   # competitor, was exact-only -> +city variants leaked
    "benito zappia",          # competitor paralegal, absent entirely
    "x copper",               # competitor X-Copper, only city-specific exacts existed
    "ex copper",              # misspelling variant ("ex copper near me")
    "xcopper",                # one-word brand variant
]

svc = client.get_service("CampaignCriterionService")
ops = []
for text in PHRASE_NEGS:
    op = client.get_type("CampaignCriterionOperation")
    cc = op.create
    cc.campaign = CAMPAIGN
    cc.negative = True
    cc.keyword.text = text
    cc.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
    ops.append(op)

res = svc.mutate_campaign_criteria(customer_id=cid, operations=ops)
print(f"  Added {len(res.results)} campaign-level PHRASE negatives:")
for text, r in zip(PHRASE_NEGS, res.results):
    print(f"    [PHR] {text}  -> {r.resource_name}")
print("\n  DONE. Parking left as-is (already broad-covered at campaign level).")
