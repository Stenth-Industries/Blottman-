"""Dedupe the empty 'Cell Phone Ticket' sitelink, publish rebuilt RSA (court/defence
angle) to ad group 186398312300, and pause the old non-compliant RSA #1 (774748697421).
Validates char limits locally before mutating."""
from dotenv import load_dotenv
import os, logging, sys
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
AD_GROUP = f"customers/{cid}/adGroups/186398312300"
OLD_RSA1 = f"customers/{cid}/adGroupAds/186398312300~774748697421"
DUP_SITELINK = f"customers/{cid}/campaignAssets/23039650759~322570766591~SITELINK"
FINAL_URL = "https://blottman.com/traffic-tickets"

HEADLINES = [
    ("Toronto Traffic Ticket Lawyer", True),
    ("Traffic Ticket Lawyer Ontario", True),
    ("Traffic Ticket Lawyer Help", True),
    ("You Don't Attend Court", False),
    ("Don't Just Pay the Fine", False),
    ("Challenge Your Ticket", False),
    ("500+ Car Ticket Cases Handled", False),
    ("Specialized in Traffic Law", False),
    ("Licensed Ontario Paralegals", False),
    ("Don't Miss Your Deadline", False),
    ("Get Help With Your Ticket", False),
    ("Free Case Review", False),
    ("Upfront, Honest Pricing", False),
    ("Book a Free Consult Now", False),
    ("Blottman Legal Services", False),
]
DESCRIPTIONS = [
    "Charged with a traffic ticket? Experienced Ontario paralegals can help fast.",
    "We attend court so you don't have to. Licensed, specialized traffic defence.",
    "Don't just plead guilty. Reduce or fight fines, demerit points, and penalties.",
    "Call now for a free case review and find out how to fight your ticket.",
]

# ---- local validation ----
errs = []
for t, _ in HEADLINES:
    if len(t) > 30: errs.append(f"headline over 30 ({len(t)}): {t}")
    if "!" in t: errs.append(f"headline has '!': {t}")
excl = sum(d.count("!") for d in DESCRIPTIONS)
for d in DESCRIPTIONS:
    if len(d) > 90: errs.append(f"description over 90 ({len(d)}): {d}")
if excl > 1: errs.append(f"too many '!' across ad: {excl}")
if len(HEADLINES) != 15: errs.append("not 15 headlines")
if len(DESCRIPTIONS) != 4: errs.append("not 4 descriptions")
if errs:
    print("VALIDATION FAILED:"); [print("  -", e) for e in errs]; sys.exit(1)
print("  [0] Local validation passed (15 H <=30, 4 D <=90, 0 banned '!').")

# ---- 1) Remove duplicate empty sitelink ----
ca_svc = client.get_service("CampaignAssetService")
op = client.get_type("CampaignAssetOperation")
op.remove = DUP_SITELINK
ca_svc.mutate_campaign_assets(customer_id=cid, operations=[op])
print("  [1] Removed duplicate empty 'Cell Phone Ticket' sitelink.")

# ---- 2) Create rebuilt RSA (ENABLED) ----
aga_svc = client.get_service("AdGroupAdService")
op = client.get_type("AdGroupAdOperation")
aga = op.create
aga.ad_group = AD_GROUP
aga.status = client.enums.AdGroupAdStatusEnum.ENABLED
ad = aga.ad
ad.final_urls.append(FINAL_URL)
rsa = ad.responsive_search_ad
rsa.path1 = "traffic-tickets"
rsa.path2 = "defence"
for text, pinned in HEADLINES:
    a = client.get_type("AdTextAsset")
    a.text = text
    if pinned:
        a.pinned_field = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1
    rsa.headlines.append(a)
for text in DESCRIPTIONS:
    a = client.get_type("AdTextAsset")
    a.text = text
    rsa.descriptions.append(a)
res = aga_svc.mutate_ad_group_ads(customer_id=cid, operations=[op])
print(f"  [2] Rebuilt RSA created (ENABLED): {res.results[0].resource_name}")

# ---- 3) Pause old non-compliant RSA #1 ----
op = client.get_type("AdGroupAdOperation")
op.update.resource_name = OLD_RSA1
op.update.status = client.enums.AdGroupAdStatusEnum.PAUSED
op.update_mask.paths.append("status")
aga_svc.mutate_ad_group_ads(customer_id=cid, operations=[op])
print("  [3] Paused old RSA #1 (774748697421 — had 98% Win Rate + DUI).")
print("\n  DONE — ad group now runs RSA #2 (record angle) + rebuilt RSA (court/defence angle).")
