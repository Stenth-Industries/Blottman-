"""Build + publish the full campaign-level EXTENSION STACK for the consolidated
Search campaign 'Search - Ontario Traffic Tickets (Consolidated)' (23971101309).
Sitelinks (10), callouts (10), structured snippets (2 headers), call asset, and
re-attach the existing Lead Form asset. All copy LSO-safe (no lawyer/paralegal,
no win-rate/guarantees). Run once. Prints resource names + a re-link count.
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

CAMPAIGN = f"customers/{cid}/campaigns/23971101309"
LEAD_FORM_ASSET = f"customers/{cid}/assets/371903420556"  # existing approved Lead Form
PHONE = "(647) 794-7750"

# (title<=25, desc1<=35, desc2<=35, final_url)
SITELINKS = [
    ("Speeding Tickets",      "Fight demerit points & fines",  "Protect your record & insurance", "https://blottman.ca/speeding"),
    ("Careless Driving",      "Avoid licence suspension",      "Free case review today",          "https://blottman.ca/careless-driving"),
    ("Stunt Driving",         "Fight roadside suspensions",    "Keep your licence & car",         "https://blottman.ca/stunt-driving"),
    ("Cell Phone Tickets",    "Distracted driving defence",    "Fight points on your record",     "https://blottman.ca/cell-phone"),
    ("Fail to Stop",          "Stop sign & light tickets",     "Challenge the charge",            "https://blottman.ca/fail-to-stop"),
    ("Disobey Sign Tickets",  "Dispute the officer's claim",   "Protect your driving record",     "https://blottman.ca/disobey-sign"),
    ("No Insurance Tickets",  "Fight heavy fines",             "Free case review today",          "https://blottman.ca/no-insurance"),
    ("Driving Suspension",    "Driving under suspension",      "Get back on the road",            "https://blottman.ca/driving-under-suspension"),
    ("Free Case Review",      "Talk through your options",     "No obligation, no pressure",      "https://blottman.ca/"),
    ("Call Us Today",         "Speak with our team direct",    "Evenings & weekends too",         "https://blottman.ca/"),
]

CALLOUTS = [
    "LSO Licensed", "Free Case Review", "Serving All Ontario", "Evenings & Weekends",
    "Phone Consultations", "500+ Tickets Handled", "We Attend Court", "Protect Your Record",
    "No Obligation Review", "We Fight Your Ticket",
]

SNIPPETS = [
    ("SERVICES", ["Speeding", "Careless Driving", "Stunt Driving", "Cell Phone",
                  "Fail to Stop", "Disobey Sign", "No Insurance", "Suspended Licence"]),
    ("TYPES",    ["Ticket Defence", "Court Representation", "Free Case Review",
                  "Phone Consults", "Demerit Point Help"]),
]

# ---- length guard (fail loud before any mutation) ----
for t, d1, d2, _ in SITELINKS:
    assert len(t) <= 25 and len(d1) <= 35 and len(d2) <= 35, f"sitelink too long: {t}"
for c in CALLOUTS:
    assert len(c) <= 25, f"callout too long: {c}"
for h, vals in SNIPPETS:
    for v in vals:
        assert len(v) <= 25, f"snippet value too long: {v}"

asset_svc = client.get_service("AssetService")
ca_svc = client.get_service("CampaignAssetService")
AFT = client.enums.AssetFieldTypeEnum


def link(asset_names, field_type, label):
    ops = []
    for rn in asset_names:
        o = client.get_type("CampaignAssetOperation")
        ca = o.create
        ca.campaign = CAMPAIGN
        ca.asset = rn
        ca.field_type = field_type
        ops.append(o)
    res = ca_svc.mutate_campaign_assets(customer_id=cid, operations=ops)
    print(f"  linked {len(res.results)} {label} -> campaign")


# ---- 1) sitelinks ----
ops = []
for title, d1, d2, url in SITELINKS:
    o = client.get_type("AssetOperation")
    a = o.create
    a.final_urls.append(url)
    a.sitelink_asset.link_text = title
    a.sitelink_asset.description1 = d1
    a.sitelink_asset.description2 = d2
    ops.append(o)
names = [r.resource_name for r in asset_svc.mutate_assets(customer_id=cid, operations=ops).results]
print(f"  [1] created {len(names)} sitelink assets")
link(names, AFT.SITELINK, "sitelinks")

# ---- 2) callouts ----
ops = []
for text in CALLOUTS:
    o = client.get_type("AssetOperation")
    o.create.callout_asset.callout_text = text
    ops.append(o)
names = [r.resource_name for r in asset_svc.mutate_assets(customer_id=cid, operations=ops).results]
print(f"  [2] created {len(names)} callout assets")
link(names, AFT.CALLOUT, "callouts")

# ---- 3) structured snippets ----
ops = []
for header, vals in SNIPPETS:
    o = client.get_type("AssetOperation")
    ss = o.create.structured_snippet_asset
    ss.header = header
    ss.values.extend(vals)
    ops.append(o)
names = [r.resource_name for r in asset_svc.mutate_assets(customer_id=cid, operations=ops).results]
print(f"  [3] created {len(names)} structured-snippet assets")
link(names, AFT.STRUCTURED_SNIPPET, "structured snippets")

# ---- 4) call asset ----
o = client.get_type("AssetOperation")
call = o.create.call_asset
call.country_code = "CA"
call.phone_number = PHONE
names = [r.resource_name for r in asset_svc.mutate_assets(customer_id=cid, operations=[o]).results]
print(f"  [4] created call asset {names[0]}")
link(names, AFT.CALL, "call asset")

# ---- 5) re-attach existing Lead Form asset ----
try:
    link([LEAD_FORM_ASSET], AFT.LEAD_FORM, "lead form")
except Exception as e:
    print(f"  [5] lead-form link skipped: {str(e).splitlines()[0][:120]}")

print("\n  DONE - extension stack live (assets enter Google editorial review).")
