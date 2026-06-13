"""Live hierarchy view of 'Traffic ticket lawyer broad' — campaign > ad group > ads,
with each ad's status, approval, landing page, and headlines."""
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
c = GoogleAdsClient.load_from_dict(cfg)
ga = c.get_service("GoogleAdsService")
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
NAME = "Traffic ticket lawyer broad"

# campaign + budget
for r in ga.search(customer_id=cid, query=f"""
    SELECT campaign.name, campaign.status, campaign.primary_status,
           campaign_budget.amount_micros
    FROM campaign WHERE campaign.name='{NAME}'"""):
    print("\n" + "="*60)
    print(f"  CAMPAIGN: {r.campaign.name}")
    print(f"  status={r.campaign.status.name}  serving={r.campaign.primary_status.name}"
          f"  budget=${r.campaign_budget.amount_micros/1e6:.0f}/day")
    print("="*60)

# ads grouped by ad group
ag_seen = set()
for r in ga.search(customer_id=cid, query=f"""
    SELECT ad_group.name, ad_group_ad.ad.id, ad_group_ad.status,
           ad_group_ad.policy_summary.approval_status,
           ad_group_ad.ad.final_urls,
           ad_group_ad.ad.responsive_search_ad.headlines
    FROM ad_group_ad
    WHERE campaign.name='{NAME}' AND ad_group_ad.status!='REMOVED'
    ORDER BY ad_group_ad.status"""):
    if r.ad_group.name not in ag_seen:
        ag_seen.add(r.ad_group.name)
        print(f"\n  AD GROUP: {r.ad_group.name}")
    a = r.ad_group_ad
    icon = {"ENABLED": "[LIVE] ", "PAUSED": "[PAUSED]"}.get(a.status.name, a.status.name)
    appr = a.policy_summary.approval_status.name
    rev = " (in review)" if appr == "UNKNOWN" else f" ({appr.lower()})"
    hs = [h.text for h in a.ad.responsive_search_ad.headlines][:3]
    print(f"\n    {icon} Ad {a.ad.id}{rev}")
    print(f"        -> {list(a.ad.final_urls)[0] if a.ad.final_urls else '-'}")
    print(f"        headlines: {' | '.join(hs)} ...")

# recent performance
print("\n  " + "-"*56)
print("  Last 7 days:")
for r in ga.search(customer_id=cid, query=f"""
    SELECT metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions
    FROM campaign WHERE campaign.name='{NAME}' AND segments.date DURING LAST_7_DAYS"""):
    m = r.metrics
    print(f"    impr {m.impressions:,.0f} | clicks {m.clicks:,.0f} | "
          f"spend ${m.cost_micros/1e6:,.2f} | conv {m.conversions:.1f}")
print()
