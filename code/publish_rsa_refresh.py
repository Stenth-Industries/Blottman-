"""Lift the Average court-angle RSA to Excellent in ad group 186398312300.
Order (to respect the 3-enabled-RSA ceiling):
  [1] Pause old non-compliant ad 774748697421 (98% Win Rate + DUI, homepage).
  [2] Pause the Average ad being replaced, 812451172230 (court/defence).
  [3] Create the refreshed court/defence RSA (ENABLED) — 15 H (3 pinned slot 1) + 4 D.
End state enabled RSAs: 812451424746 (record angle) + new refresh (court angle)."""
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
OLD_98WIN = f"customers/{cid}/adGroupAds/186398312300~774748697421"
OLD_AVG   = f"customers/{cid}/adGroupAds/186398312300~812451172230"
FINAL_URL = "https://blottman.com/traffic-tickets"

HEADLINES = [
    ("Toronto Traffic Ticket Lawyer", True),
    ("Traffic Ticket Lawyer Ontario", True),
    ("Fight Your Traffic Ticket", True),
    ("You Don't Attend Court", False),
    ("Don't Just Plead Guilty", False),
    ("Challenge Your Ticket", False),
    ("500+ Ticket Cases Handled", False),
    ("Licensed Ontario Paralegals", False),
    ("LSO-Regulated Paralegals", False),
    ("Act Before Your Court Date", False),
    ("Don't Miss Your Deadline", False),
    ("Upfront, Honest Pricing", False),
    ("No Hidden Legal Fees", False),
    ("Book a Free Case Review", False),
    ("Get Traffic Ticket Help", False),
]
DESCRIPTIONS = [
    "Charged with a traffic ticket in Ontario? Experienced paralegals can help fast.",
    "Licensed Ontario paralegals. Upfront, honest pricing with no hidden fees.",
    "Your paralegal attends court so you don't have to. Don't just plead guilty.",
    "Book a free case review today and find out how to fight your traffic ticket.",
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
if sum(1 for _, p in HEADLINES if p) != 3: errs.append("expected exactly 3 pinned headlines")
if errs:
    print("VALIDATION FAILED:"); [print("  -", e) for e in errs]; sys.exit(1)
print("  [0] Local validation passed (15 H <=30, 4 D <=90, 0 banned '!', 3 pinned slot 1).")

aga = client.get_service("AdGroupAdService")

# ---- 1) Pause old 98% Win Rate + DUI ad ----
op = client.get_type("AdGroupAdOperation")
op.update.resource_name = OLD_98WIN
op.update.status = client.enums.AdGroupAdStatusEnum.PAUSED
op.update_mask.paths.append("status")
aga.mutate_ad_group_ads(customer_id=cid, operations=[op])
print("  [1] Paused 774748697421 (98% Win Rate + DUI, homepage).")

# ---- 2) Pause the Average ad being replaced ----
op = client.get_type("AdGroupAdOperation")
op.update.resource_name = OLD_AVG
op.update.status = client.enums.AdGroupAdStatusEnum.PAUSED
op.update_mask.paths.append("status")
aga.mutate_ad_group_ads(customer_id=cid, operations=[op])
print("  [2] Paused 812451172230 (the Average court-angle ad being replaced).")

# ---- 3) Create refreshed RSA (ENABLED) ----
op = client.get_type("AdGroupAdOperation")
a = op.create
a.ad_group = AD_GROUP
a.status = client.enums.AdGroupAdStatusEnum.ENABLED
ad = a.ad
ad.final_urls.append(FINAL_URL)
rsa = ad.responsive_search_ad
rsa.path1 = "traffic-tickets"
rsa.path2 = "defence"
for text, pinned in HEADLINES:
    h = client.get_type("AdTextAsset")
    h.text = text
    if pinned:
        h.pinned_field = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1
    rsa.headlines.append(h)
for text in DESCRIPTIONS:
    d = client.get_type("AdTextAsset")
    d.text = text
    rsa.descriptions.append(d)
res = aga.mutate_ad_group_ads(customer_id=cid, operations=[op])
print(f"  [3] Created refreshed RSA (ENABLED): {res.results[0].resource_name}")
print("\n  DONE — enabled RSAs now: 812451424746 (record) + new refresh (court/defence).")
