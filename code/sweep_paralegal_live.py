"""Remove 'paralegal' from the LIVE consolidated Search campaign (23971101309).
Replaces the shared 'Licensed Ontario Paralegal' headline with 'Licensed in
Ontario' (pins preserved) and swaps in a paralegal-free 4-description set.
Skips the 3 ad groups already handled by strengthen_poor_rsas.py. Idempotent-ish
(re-running just re-sets the same clean copy). In-place RSA update -> re-review.

NOTE: the PAUSED legacy campaigns also contain 'paralegal' AND worse claims
('We Are Actual Lawyers, Not Paralegals' x13, '98% Win Rate', 'Lawyer') -- those
need a holistic rewrite/pause, not a token swap, so they are deliberately NOT
touched here. See CLAUDE.md change log.
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
ga = client.get_service("GoogleAdsService")
ad_svc = client.get_service("AdService")

DONE = {814321604804, 814246896223, 814213882242}  # already fixed by strengthen_poor_rsas.py
CLEAN_DESC = [
    "Fight your ticket with a licensed Ontario team that protects your record and insurance.",
    "We handle the paperwork and court so you don't have to. 500+ tickets handled in Ontario.",
    "Fight your ticket and the demerit points that raise your insurance for years. Talk free.",
    "Free case review today. Most clients never set foot in court. Don't just pay the fine.",
]
for d in CLEAN_DESC:
    assert len(d) <= 90, d

q = ("SELECT ad_group.name, ad_group_ad.ad.id, "
     "ad_group_ad.ad.responsive_search_ad.headlines "
     "FROM ad_group_ad WHERE campaign.id=23971101309 AND ad_group_ad.status='ENABLED'")
ops, touched = [], []
for r in ga.search(customer_id=cid, query=q):
    ad = r.ad_group_ad.ad
    if ad.id in DONE:
        continue
    o = client.get_type("AdOperation")
    u = o.update
    u.resource_name = f"customers/{cid}/ads/{ad.id}"
    rsa = u.responsive_search_ad
    for h in ad.responsive_search_ad.headlines:
        a = client.get_type("AdTextAsset")
        a.text = "Licensed in Ontario" if h.text == "Licensed Ontario Paralegal" else h.text
        if h.pinned_field:
            a.pinned_field = h.pinned_field
        rsa.headlines.append(a)
    for t in CLEAN_DESC:
        a = client.get_type("AdTextAsset")
        a.text = t
        rsa.descriptions.append(a)
    o.update_mask.paths.extend(["responsive_search_ad.headlines", "responsive_search_ad.descriptions"])
    ops.append(o)
    touched.append((r.ad_group.name, ad.id))

res = ad_svc.mutate_ads(customer_id=cid, operations=ops)
for (nm, aid), _ in zip(touched, res.results):
    print(f"  fixed {nm:26} ad {aid}")
print(f"  {len(res.results)} live ad groups cleaned of 'paralegal'")
