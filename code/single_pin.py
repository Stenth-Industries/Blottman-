"""Final Ad Strength move: drop both enabled RSAs from 3 pins to 1 pin.
Keep one keyword+city headline pinned to slot 1 (guarantees keyword in pos 1 = QS),
unpin the other two so Google can rotate (lifts Average -> Good). Headlines/descriptions
otherwise unchanged from the keyword rebuild. In-place update; single re-review each."""
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

# Only the FIRST headline stays pinned to slot 1; the next two are now unpinned.
COURT = [
    ("Toronto Traffic Ticket Lawyer", True),
    ("Traffic Ticket Lawyer Ontario", False),
    ("Fight Your Traffic Ticket", False),
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
    ("Ontario Traffic Ticket Lawyer", False),
    ("Traffic Ticket Lawyer Near You", False),
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

errs = []
for ad_id, _, _, H, D in JOBS:
    if sum(1 for _, p in H if p) != 1: errs.append(f"{ad_id}: expected exactly 1 pin")
    for t, _ in H:
        if len(t) > 30 or "!" in t: errs.append(f"{ad_id}: bad headline: {t}")
if errs:
    print("VALIDATION FAILED:"); [print("  -", e) for e in errs]; sys.exit(1)
print("  [0] Validation passed (exactly 1 pin per ad).")

ad_svc = client.get_service("AdService")
for ad_id, p1, p2, H, D in JOBS:
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
        "responsive_search_ad.headlines", "responsive_search_ad.descriptions",
        "responsive_search_ad.path1", "responsive_search_ad.path2",
    ])
    res = ad_svc.mutate_ads(customer_id=cid, operations=[op])
    print(f"  Updated ad {ad_id} -> 1 pin: {res.results[0].resource_name}")
print("\n  DONE — both RSAs now single-pinned. Re-review pending; strength will recompute.")
