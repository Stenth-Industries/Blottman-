"""Publish RSA #2 + 6 campaign-level sitelinks for 'Traffic ticket lawyer broad'.
Adds a 2nd ENABLED RSA to ad group 186398312300 and links sitelinks to campaign 23039650759.
Run once. Prints resource names of everything created."""
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

AD_GROUP = f"customers/{cid}/adGroups/186398312300"
CAMPAIGN = f"customers/{cid}/campaigns/23039650759"
FINAL_URL = "https://blottman.com/traffic-tickets"

HEADLINES = [
    ("Traffic Ticket Lawyer Toronto", True),
    ("Ontario Traffic Ticket Lawyer", True),
    ("Traffic Ticket Lawyer Near You", True),
    ("Defend Your Driving Record", False),
    ("Fight Demerit Points", False),
    ("Protect Your Insurance Rate", False),
    ("500+ Car Ticket Cases Handled", False),
    ("Licensed Traffic Paralegals", False),
    ("Serving Drivers Across the GTA", False),
    ("Act Before Your Court Date", False),
    ("Talk to a Paralegal Today", False),
    ("Free, No-Obligation Review", False),
    ("Upfront, Fair Pricing", False),
    ("Book Your Free Consult", False),
    ("Trust Blottman Law", False),
]
DESCRIPTIONS = [
    "Fight your traffic ticket with experienced Ontario paralegals. Free case review.",
    "Licensed, LSO-regulated paralegals. Upfront, fair pricing with no hidden fees.",
    "Keep demerit points off your record and protect your insurance rate. Local team.",
    "Book your free, no-obligation case review today. Don't just pay the fine.",
]
SITELINKS = [
    ("Careless Driving", "Fight careless driving charges", "Protect your licence & record",
     "https://blottman.com/careless-driving-lawyer-paralegal"),
    ("Speeding Tickets", "Challenge your speeding ticket", "Avoid demerit points & fines",
     "https://blottman.com/speeding-ticket-lawyer"),
    ("Stunt Driving", "Defend stunt driving charges", "Licence suspension help",
     "https://blottman.com/stunt-driving-ticket-lawyer"),
    ("Cell Phone Ticket", "Distracted driving defence", "Fight the charge in Ontario",
     "https://blottman.com/cellphone-ticket-lawyer-and-paralegal-ontario"),
    ("Suspended Licence", "Drive under suspension help", "Experienced GTA paralegals",
     "https://blottman.com/driving-under-suspension-ticket-lawyer-toronto"),
    ("Free Consultation", "Free, no-obligation review", "Talk to a paralegal today",
     "https://blottman.com/free-consultation"),
]

# ---- 1) Create RSA #2 (ENABLED) ----
aga_svc = client.get_service("AdGroupAdService")
op = client.get_type("AdGroupAdOperation")
aga = op.create
aga.ad_group = AD_GROUP
aga.status = client.enums.AdGroupAdStatusEnum.ENABLED
ad = aga.ad
ad.final_urls.append(FINAL_URL)
rsa = ad.responsive_search_ad
rsa.path1 = "traffic-tickets"
rsa.path2 = "free-review"
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
print(f"  [1] RSA #2 created (ENABLED): {res.results[0].resource_name}")

# ---- 2) Create sitelink assets ----
asset_svc = client.get_service("AssetService")
ops = []
for title, d1, d2, url in SITELINKS:
    o = client.get_type("AssetOperation")
    asset = o.create
    asset.final_urls.append(url)
    sl = asset.sitelink_asset
    sl.link_text = title
    sl.description1 = d1
    sl.description2 = d2
    ops.append(o)
res = asset_svc.mutate_assets(customer_id=cid, operations=ops)
asset_names = [r.resource_name for r in res.results]
print(f"  [2] Created {len(asset_names)} sitelink assets")

# ---- 3) Link sitelinks to the campaign ----
ca_svc = client.get_service("CampaignAssetService")
ops = []
for rn in asset_names:
    o = client.get_type("CampaignAssetOperation")
    ca = o.create
    ca.campaign = CAMPAIGN
    ca.asset = rn
    ca.field_type = client.enums.AssetFieldTypeEnum.SITELINK
    ops.append(o)
res = ca_svc.mutate_campaign_assets(customer_id=cid, operations=ops)
print(f"  [3] Linked {len(res.results)} sitelinks to campaign 'Traffic ticket lawyer broad'")
print("\n  DONE — RSA #2 + 6 sitelinks are live (pending Google ad review).")
