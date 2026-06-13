"""Lift both ENABLED RSAs in ad group 186398312300 from Average by adding the
highest-impression missing keywords (defence 219, dispute 140, speeding 112,
suspended 32, careless 5). In-place update of each ad's responsive_search_ad
(same ad id, single re-review). Validates char limits + pin count locally first."""
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
H1 = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1

# (text, pinned-to-slot-1?)
COURT = [
    ("Toronto Traffic Ticket Lawyer", True),
    ("Traffic Ticket Lawyer Ontario", True),
    ("Fight Your Traffic Ticket", True),
    ("You Don't Attend Court", False),
    ("Don't Just Plead Guilty", False),
    ("Dispute Your Traffic Ticket", False),
    ("500+ Ticket Cases Handled", False),
    ("Licensed Ontario Paralegals", False),
    ("Traffic Ticket Defence", False),
    ("Act Before Your Court Date", False),
    ("Fight a Speeding Ticket", False),
    ("Suspended Licence Help", False),
    ("Careless Driving Defence", False),
    ("Book a Free Case Review", False),
    ("Get Traffic Ticket Help", False),
]
RECORD = [
    ("Traffic Ticket Lawyer Toronto", True),
    ("Ontario Traffic Ticket Lawyer", True),
    ("Traffic Ticket Lawyer Near You", True),
    ("Defend Your Driving Record", False),
    ("Fight Demerit Points", False),
    ("Protect Your Insurance Rate", False),
    ("500+ Car Ticket Cases Handled", False),
    ("Licensed Traffic Paralegals", False),
    ("Traffic Ticket Defence", False),
    ("Act Before Your Court Date", False),
    ("Dispute Your Traffic Ticket", False),
    ("Fight a Speeding Ticket", False),
    ("Suspended Licence Help", False),
    ("Careless Driving Defence", False),
    ("Free, No-Obligation Review", False),
]
# descriptions unchanged — re-send existing so the update is headline-only in effect
DESC_COURT = [
    "Charged with a traffic ticket in Ontario? Experienced paralegals can help fast.",
    "Licensed Ontario paralegals. Upfront, honest pricing with no hidden fees.",
    "Your paralegal attends court so you don't have to. Don't just plead guilty.",
    "Book a free case review today and find out how to fight your traffic ticket.",
]
DESC_RECORD = [
    "Fight your traffic ticket with experienced Ontario paralegals. Free case review.",
    "Licensed, LSO-regulated paralegals. Upfront, fair pricing with no hidden fees.",
    "Keep demerit points off your record and protect your insurance rate. Local team.",
    "Book your free, no-obligation case review today. Don't just pay the fine.",
]

JOBS = [
    ("812455198290", "traffic-tickets", "defence",     COURT,  DESC_COURT),
    ("812451424746", "traffic-tickets", "free-review", RECORD, DESC_RECORD),
]

# ---- local validation ----
errs = []
for ad_id, _, _, H, D in JOBS:
    if len(H) != 15: errs.append(f"{ad_id}: not 15 headlines")
    if len(D) != 4:  errs.append(f"{ad_id}: not 4 descriptions")
    if sum(1 for _, p in H if p) != 3: errs.append(f"{ad_id}: expected 3 pins")
    for t, _ in H:
        if len(t) > 30: errs.append(f"{ad_id}: H over 30 ({len(t)}): {t}")
        if "!" in t:    errs.append(f"{ad_id}: H has '!': {t}")
    seen = set()
    for t, _ in H:
        if t.lower() in seen: errs.append(f"{ad_id}: duplicate H: {t}")
        seen.add(t.lower())
    for d in D:
        if len(d) > 90: errs.append(f"{ad_id}: D over 90 ({len(d)}): {d}")
    if sum(d.count("!") for d in D) > 1: errs.append(f"{ad_id}: too many '!'")
if errs:
    print("VALIDATION FAILED:"); [print("  -", e) for e in errs]; sys.exit(1)
print("  [0] Local validation passed for both ads (15 H <=30, 4 D <=90, 3 pins, no dupes).")

ad_svc = client.get_service("AdService")
for ad_id, p1, p2, H, D, in [(j[0], j[1], j[2], j[3], j[4]) for j in JOBS]:
    op = client.get_type("AdOperation")
    ad = op.update
    ad.resource_name = f"customers/{cid}/ads/{ad_id}"
    ad.responsive_search_ad.path1 = p1
    ad.responsive_search_ad.path2 = p2
    for text, pinned in H:
        a = client.get_type("AdTextAsset"); a.text = text
        if pinned: a.pinned_field = H1
        ad.responsive_search_ad.headlines.append(a)
    for text in D:
        a = client.get_type("AdTextAsset"); a.text = text
        ad.responsive_search_ad.descriptions.append(a)
    op.update_mask.paths.extend([
        "responsive_search_ad.headlines",
        "responsive_search_ad.descriptions",
        "responsive_search_ad.path1",
        "responsive_search_ad.path2",
    ])
    res = ad_svc.mutate_ads(customer_id=cid, operations=[op])
    print(f"  Updated ad {ad_id}: {res.results[0].resource_name}")
print("\n  DONE — both RSAs updated in place; each will re-enter editorial review once.")
