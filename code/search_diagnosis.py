"""Why is Search - Ontario Traffic Tickets (23971101309) not producing?

Pulls the three things we have never looked at together:
  1. the QUALITY SCORE COMPONENT breakdown (expected CTR / ad relevance / landing page
     experience) -- this says WHICH of the three is dragging, instead of guessing
  2. weekly conversion RATE, to test whether the landing-page/form changes moved it
  3. ad-group level spend vs conversions, to see if the problem is concentrated

Read-only.
"""
import os
import logging
from collections import defaultdict

from dotenv import load_dotenv
from google.ads.googleads.client import GoogleAdsClient

logging.getLogger("google.ads.googleads").setLevel(logging.CRITICAL)
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
CAMP = "23971101309"


def q(sql):
    try:
        return list(ga.search(customer_id=cid, query=sql))
    except Exception as e:
        print("  ERR:", str(e)[-200:])
        return []


print("=== 1. QUALITY SCORE COMPONENTS (the part we never pulled) ===")
comp = {"creative": defaultdict(int), "postclick": defaultdict(int), "ctr": defaultdict(int)}
scored = 0
for r in q(f"""
    SELECT ad_group_criterion.keyword.text, ad_group_criterion.quality_info.quality_score,
           ad_group_criterion.quality_info.creative_quality_score,
           ad_group_criterion.quality_info.post_click_quality_score,
           ad_group_criterion.quality_info.search_predicted_ctr,
           ad_group_criterion.status, campaign.status
    FROM ad_group_criterion
    WHERE campaign.id = {CAMP} AND ad_group_criterion.type = 'KEYWORD'
      AND ad_group_criterion.status = 'ENABLED'"""):
    qi = r.ad_group_criterion.quality_info
    if not qi.quality_score:
        continue
    scored += 1
    comp["creative"][qi.creative_quality_score.name] += 1
    comp["postclick"][qi.post_click_quality_score.name] += 1
    comp["ctr"][qi.search_predicted_ctr.name] += 1
print(f"  keywords with a QS: {scored}")
print(f"  AD RELEVANCE          : {dict(comp['creative'])}")
print(f"  LANDING PAGE EXPERIENCE: {dict(comp['postclick'])}")
print(f"  EXPECTED CTR          : {dict(comp['ctr'])}")

print()
print("=== 2. WEEKLY: clicks, cost, conversions, CONVERSION RATE ===")
weeks = defaultdict(lambda: [0, 0.0, 0.0])
for r in q(f"""
    SELECT campaign.status, segments.date, metrics.clicks, metrics.cost_micros, metrics.conversions
    FROM campaign WHERE campaign.id = {CAMP} AND segments.date DURING LAST_30_DAYS"""):
    m = r.metrics
    wk = r.segments.date[:7] + "-w" + str((int(r.segments.date[8:10]) - 1) // 7 + 1)
    weeks[wk][0] += m.clicks
    weeks[wk][1] += m.cost_micros / 1e6
    weeks[wk][2] += m.conversions
for wk in sorted(weeks):
    c, cost, conv = weeks[wk]
    cr = (conv / c * 100) if c else 0
    cpl = (cost / conv) if conv else 0
    print(f"  {wk} | {c:4} clk | ${cost:7.2f} | conv {conv:4.1f} | CR {cr:5.2f}% | $/conv {cpl:7.2f}")

print()
print("=== 3. AD GROUP: spend vs conversions, last 30d ===")
rows = []
for r in q(f"""
    SELECT ad_group.name, campaign.status, metrics.impressions, metrics.clicks,
           metrics.cost_micros, metrics.conversions, metrics.ctr, metrics.average_cpc
    FROM ad_group WHERE campaign.id = {CAMP} AND segments.date DURING LAST_30_DAYS"""):
    m = r.metrics
    rows.append((m.cost_micros / 1e6, r.ad_group.name, m.impressions, m.clicks, m.conversions,
                 m.ctr * 100, m.average_cpc / 1e6))
for cost, name, impr, clk, conv, ctr, cpc in sorted(rows, reverse=True):
    print(f"  ${cost:7.2f} | {name[:30]:30} | {impr:5} impr {clk:4} clk | CTR {ctr:5.2f}% | "
          f"CPC ${cpc:5.2f} | conv {conv:4.1f}")

print()
print("=== 4. DEVICE split, last 30d ===")
for r in q(f"""
    SELECT campaign.status, segments.device, metrics.impressions, metrics.clicks,
           metrics.cost_micros, metrics.conversions
    FROM campaign WHERE campaign.id = {CAMP} AND segments.date DURING LAST_30_DAYS"""):
    m = r.metrics
    cr = (m.conversions / m.clicks * 100) if m.clicks else 0
    print(f"  {r.segments.device.name:10} | {m.impressions:6} impr | {m.clicks:4} clk | "
          f"${m.cost_micros/1e6:8.2f} | conv {m.conversions:4.1f} | CR {cr:5.2f}%")

print()
print("=== 5. IMPRESSION SHARE, last 30d ===")
for r in q(f"""
    SELECT campaign.status, metrics.search_impression_share,
           metrics.search_rank_lost_impression_share,
           metrics.search_budget_lost_impression_share, metrics.search_absolute_top_impression_share
    FROM campaign WHERE campaign.id = {CAMP} AND segments.date DURING LAST_30_DAYS"""):
    m = r.metrics
    print(f"  IS {m.search_impression_share*100:.2f}% | lost-to-RANK {m.search_rank_lost_impression_share*100:.2f}%"
          f" | lost-to-BUDGET {m.search_budget_lost_impression_share*100:.2f}%"
          f" | abs-top {m.search_absolute_top_impression_share*100:.2f}%")

print()
print("=== 6. TOP KEYWORDS by cost, last 30d ===")
kws = []
for r in q(f"""
    SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
           ad_group_criterion.quality_info.quality_score, campaign.status,
           metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions
    FROM keyword_view WHERE campaign.id = {CAMP} AND segments.date DURING LAST_30_DAYS"""):
    m = r.metrics
    if m.cost_micros:
        kws.append((m.cost_micros / 1e6, r.ad_group_criterion.keyword.text,
                    r.ad_group_criterion.keyword.match_type.name,
                    r.ad_group_criterion.quality_info.quality_score, m.clicks, m.conversions))
for cost, text, mt, qs, clk, conv in sorted(kws, reverse=True)[:20]:
    print(f"  ${cost:6.2f} | QS {qs or '-'} | {mt[:6]:6} | {clk:3} clk | conv {conv:4.1f} | {text[:45]}")
