"""Performance check on 'Traffic ticket lawyer broad' since it was enabled (2026-06-11).
Daily delivery, search terms, keyword spend, conversions, and CPA."""
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
ga = client.get_service("GoogleAdsService")
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
NAME = "Traffic ticket lawyer broad"

def m(x): return x/1e6

# Daily delivery
print(f"\n=== {NAME} — daily (last 7 days) ===")
print(f"  {'date':12} {'impr':>7} {'clk':>5} {'cost':>9} {'conv':>6} {'CTR':>6} {'avgCPC':>8}")
tot_cost=tot_clk=tot_imp=tot_conv=0.0
for r in ga.search(customer_id=cid, query=f"""
    SELECT segments.date, metrics.impressions, metrics.clicks, metrics.cost_micros,
           metrics.conversions, metrics.ctr, metrics.average_cpc
    FROM campaign
    WHERE campaign.name = '{NAME}' AND segments.date DURING LAST_7_DAYS
    ORDER BY segments.date
"""):
    s=r.metrics
    tot_cost+=m(s.cost_micros); tot_clk+=s.clicks; tot_imp+=s.impressions; tot_conv+=s.conversions
    print(f"  {r.segments.date:12} {s.impressions:>7} {s.clicks:>5} ${m(s.cost_micros):>8.2f} "
          f"{s.conversions:>6.1f} {s.ctr*100:>5.1f}% ${m(s.average_cpc):>7.2f}")
print(f"  {'TOTAL':12} {tot_imp:>7.0f} {tot_clk:>5.0f} ${tot_cost:>8.2f} {tot_conv:>6.1f}")
if tot_conv: print(f"  CPA = ${tot_cost/tot_conv:.2f}")
else: print(f"  CPA = n/a (0 conv)")

# Search terms
print(f"\n=== search terms (last 7 days, by cost) ===")
print(f"  {'term':45} {'impr':>6} {'clk':>4} {'cost':>8} {'conv':>5}")
for r in ga.search(customer_id=cid, query=f"""
    SELECT search_term_view.search_term, metrics.impressions, metrics.clicks,
           metrics.cost_micros, metrics.conversions
    FROM search_term_view
    WHERE campaign.name = '{NAME}' AND segments.date DURING LAST_7_DAYS
    ORDER BY metrics.cost_micros DESC
    LIMIT 30
"""):
    s=r.metrics; t=r.search_term_view.search_term[:44]
    print(f"  {t:45} {s.impressions:>6} {s.clicks:>4} ${m(s.cost_micros):>7.2f} {s.conversions:>5.1f}")

# Keyword performance
print(f"\n=== keywords (last 7 days) ===")
print(f"  {'kw':40} {'impr':>6} {'clk':>4} {'cost':>8} {'conv':>5} {'qs':>3}")
for r in ga.search(customer_id=cid, query=f"""
    SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
           ad_group_criterion.quality_info.quality_score,
           metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions
    FROM keyword_view
    WHERE campaign.name = '{NAME}' AND segments.date DURING LAST_7_DAYS
      AND ad_group_criterion.negative = FALSE
    ORDER BY metrics.cost_micros DESC
"""):
    s=r.metrics; k=r.ad_group_criterion.keyword
    qs=r.ad_group_criterion.quality_info.quality_score
    print(f"  [{k.match_type.name[:3]}] {k.text[:34]:34} {s.impressions:>6} {s.clicks:>4} "
          f"${m(s.cost_micros):>7.2f} {s.conversions:>5.1f} {qs:>3}")

# Budget-lost / impression share diagnostics
print(f"\n=== impression share (last 7 days) ===")
for r in ga.search(customer_id=cid, query=f"""
    SELECT metrics.search_impression_share, metrics.search_budget_lost_impression_share,
           metrics.search_rank_lost_impression_share, metrics.search_top_impression_share
    FROM campaign
    WHERE campaign.name = '{NAME}' AND segments.date DURING LAST_7_DAYS
"""):
    s=r.metrics
    print(f"  search IS={s.search_impression_share*100:.1f}%  "
          f"lost-budget={s.search_budget_lost_impression_share*100:.1f}%  "
          f"lost-rank={s.search_rank_lost_impression_share*100:.1f}%  "
          f"top-IS={s.search_top_impression_share*100:.1f}%")
print()
