"""Lift the 3 POOR ad groups in the consolidated Search campaign (23971101309)
from POOR by injecting offence-specific keyword headlines (each ad had only 1
keyword headline + 14 shared generics). Keeps the slot-1 pin, drops 'paralegal'
per client directive, no win-rate/guarantee/superlative claims. In-place RSA
update via AdService (re-enters editorial review; strength recomputes). Run once.
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

# shared trust/benefit/CTA block (no 'paralegal', no guarantees/superlatives)
SHARED = [
    "500+ Traffic Tickets Handled",
    "Free Case Review Today",
    "Protect Your Driving Record",
    "Avoid Costly Demerit Points",
    "Keep Your Insurance Low",
    "We Attend Court For You",
    "Serving All Of Ontario",
    "Don't Just Pay The Fine",
    "Call For A Free Consultation",
    "Licensed in Ontario",
    "Fast, Confidential Help",
]

# ad_id -> (pinned H1 keyword headline, [3 offence-specific keyword headlines])
ADS = {
    814321604804: ("Fight a No-Licence Ticket",
                   ["No Licence Ticket Defence", "Charged With No Licence?", "Driving With No Licence"]),
    814246896223: ("Fight a Cell Phone Ticket",
                   ["Cell Phone Ticket Defence", "Distracted Driving Ticket", "Texting Ticket Defence"]),
    814213882242: ("Fight Your Traffic Ticket",
                   ["Ontario Traffic Ticket Help", "Dispute Your Traffic Ticket", "Traffic Ticket Defence"]),
}

DESCRIPTIONS = [
    "Fight your ticket with a licensed Ontario team that protects your record and insurance.",
    "We handle the paperwork and court so you don't have to. 500+ tickets handled in Ontario.",
    "Fight your ticket and the demerit points that raise your insurance for years. Talk free.",
    "Free case review today. Most clients never set foot in court. Don't just pay the fine.",
]

# ---- validate char limits before any mutation ----
for adid, (h1, kws) in ADS.items():
    heads = [h1] + kws + SHARED
    assert len(heads) == 15, f"{adid}: {len(heads)} headlines (need 15)"
    for h in heads:
        assert len(h) <= 30, f"headline too long ({len(h)}): {h}"
for d in DESCRIPTIONS:
    assert len(d) <= 90, f"description too long ({len(d)}): {d}"

ad_svc = client.get_service("AdService")
HE = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1

ops = []
for adid, (h1, kws) in ADS.items():
    o = client.get_type("AdOperation")
    ad = o.update
    ad.resource_name = f"customers/{cid}/ads/{adid}"
    rsa = ad.responsive_search_ad
    # pinned keyword headline first
    a0 = client.get_type("AdTextAsset")
    a0.text = h1
    a0.pinned_field = HE
    rsa.headlines.append(a0)
    for text in kws + SHARED:
        a = client.get_type("AdTextAsset")
        a.text = text
        rsa.headlines.append(a)
    for text in DESCRIPTIONS:
        a = client.get_type("AdTextAsset")
        a.text = text
        rsa.descriptions.append(a)
    o.update_mask.paths.extend([
        "responsive_search_ad.headlines",
        "responsive_search_ad.descriptions",
    ])
    ops.append(o)

res = ad_svc.mutate_ads(customer_id=cid, operations=ops)
for r in res.results:
    print(f"  updated {r.resource_name}")
print(f"\n  DONE - {len(res.results)} RSAs rebuilt (4 keyword headlines each, no 'paralegal').")
print("  Strength recomputes after re-review (PENDING until it clears).")
