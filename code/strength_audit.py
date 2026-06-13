"""Thorough Ad Strength audit for ad group 186398312300:
- both ENABLED RSAs: every headline + description
- full ad-group keyword list with impressions (to prioritise gaps by real volume)
So we decide exactly how many headline swaps are needed, not guess."""
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
ga = client.get_service("GoogleAdsService")
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
AG = 186398312300

print("\n=== ENABLED RSAs in ad group ===")
for r in ga.search(customer_id=cid, query=f"""
    SELECT ad_group_ad.ad.id, ad_group_ad.ad_strength,
           ad_group_ad.ad.responsive_search_ad.headlines
    FROM ad_group_ad
    WHERE ad_group.id = {AG} AND ad_group_ad.status = 'ENABLED'
    ORDER BY ad_group_ad.ad.id"""):
    a = r.ad_group_ad
    hs = a.ad.responsive_search_ad.headlines
    print(f"\n  AD {a.ad.id}  strength={a.ad_strength.name}")
    for h in hs:
        pin = h.pinned_field.name if h.pinned_field else "-"
        print(f"    [{pin:<10}] {h.text}")

print("\n\n=== AD-GROUP KEYWORDS by impressions (LAST_30_DAYS) ===")
rows = []
for r in ga.search(customer_id=cid, query=f"""
    SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
           metrics.impressions, metrics.clicks
    FROM keyword_view
    WHERE ad_group.id = {AG} AND ad_group_criterion.negative = FALSE
      AND segments.date DURING LAST_30_DAYS"""):
    rows.append((r.metrics.impressions, r.metrics.clicks,
                 r.ad_group_criterion.keyword.text))
# merge any dupes across dates
agg = {}
for imp, clk, txt in rows:
    a = agg.setdefault(txt, [0, 0]); a[0]+=imp; a[1]+=clk
for txt, (imp, clk) in sorted(agg.items(), key=lambda x: -x[1][0]):
    print(f"    {imp:>4} impr  {clk:>2} clk   {txt}")
print()
