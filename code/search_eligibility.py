"""Full eligibility + health audit of 'Search - Ontario Traffic Tickets (Consolidated)'.

Covers: campaign settings drift (budget/bid/AI Max), ad approval + Ad Strength per
ad group, keyword status + Quality Score, extension/asset stack, and impression
share (where we're actually losing). Read-only.
"""
from dotenv import load_dotenv
import os, logging
from collections import defaultdict
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
CAMP = 23971101309

print("=" * 78)
print("1) CAMPAIGN SETTINGS (watch for drift vs CLAUDE.md)")
print("=" * 78)
for r in ga.search(customer_id=cid, query=f"""
    SELECT campaign.id, campaign.name, campaign.status, campaign.primary_status,
           campaign.primary_status_reasons, campaign.bidding_strategy_type,
           campaign.target_spend.cpc_bid_ceiling_micros,
           campaign.ai_max_setting.enable_ai_max,
           campaign.advertising_channel_type,
           campaign_budget.amount_micros, campaign_budget.id
    FROM campaign WHERE campaign.id = {CAMP}"""):
    c = r.campaign
    print(f"  {c.name}")
    print(f"    status={c.status.name}  primary={c.primary_status.name}")
    print(f"    reasons={[x.name for x in c.primary_status_reasons] or '-'}")
    print(f"    bid={c.bidding_strategy_type.name}  "
          f"cpc_ceiling=${c.target_spend.cpc_bid_ceiling_micros/1e6:.2f}")
    print(f"    AI Max enabled = {c.ai_max_setting.enable_ai_max}   <-- must stay False (Jul-17)")
    print(f"    budget=${r.campaign_budget.amount_micros/1e6:.2f}/day "
          f"(res {r.campaign_budget.id})   <-- CLAUDE.md logs $30")

print()
print("=" * 78)
print("2) AD GROUPS: status, ad approval, AD STRENGTH")
print("=" * 78)
for r in ga.search(customer_id=cid, query=f"""
    SELECT campaign.id, ad_group.id, ad_group.name, ad_group.status,
           ad_group_ad.ad.id, ad_group_ad.status,
           ad_group_ad.ad_strength,
           ad_group_ad.policy_summary.approval_status,
           ad_group_ad.policy_summary.review_status
    FROM ad_group_ad
    WHERE campaign.id = {CAMP} AND ad_group_ad.status != 'REMOVED'
    ORDER BY ad_group.name"""):
    a = r.ad_group_ad
    flag = "" if a.policy_summary.approval_status.name == "APPROVED" else "  <<< NOT APPROVED"
    weak = "  <<< WEAK" if a.ad_strength.name in ("POOR", "AVERAGE", "PENDING") else ""
    print(f"  {r.ad_group.name[:30]:32s} [{r.ad_group.status.name:7}] ad {a.ad.id} "
          f"{a.policy_summary.approval_status.name:9} strength={a.ad_strength.name}{flag}{weak}")

print()
print("=" * 78)
print("3) KEYWORDS: status + Quality Score (14d impressions)")
print("=" * 78)
kw = {}
for r in ga.search(customer_id=cid, query=f"""
    SELECT campaign.id, ad_group.name, ad_group_criterion.keyword.text,
           ad_group_criterion.keyword.match_type, ad_group_criterion.status,
           ad_group_criterion.system_serving_status,
           ad_group_criterion.quality_info.quality_score,
           metrics.impressions, metrics.clicks, metrics.cost_micros
    FROM keyword_view
    WHERE campaign.id = {CAMP} AND segments.date DURING LAST_14_DAYS
      AND ad_group_criterion.status = 'ENABLED'"""):
    c = r.ad_group_criterion
    k = (r.ad_group.name, c.keyword.text, c.keyword.match_type.name)
    e = kw.setdefault(k, {"qs": c.quality_info.quality_score,
                          "serve": c.system_serving_status.name,
                          "impr": 0, "clk": 0, "cost": 0.0})
    e["impr"] += r.metrics.impressions
    e["clk"] += r.metrics.clicks
    e["cost"] += r.metrics.cost_micros / 1e6

qs_buckets = defaultdict(int)
rare = 0
for (ag, text, mt), e in kw.items():
    q = e["qs"]
    if q:
        qs_buckets[q] += 1
    else:
        rare += 1
print(f"  enabled keywords with 14d data: {len(kw)}")
print(f"  Quality Score distribution: "
      + "  ".join(f"QS{q}={n}" for q, n in sorted(qs_buckets.items())) or "  (none)")
print(f"  no QS yet (too few impressions): {rare}")
print("\n  --- top 15 keywords by spend ---")
for (ag, text, mt), e in sorted(kw.items(), key=lambda x: -x[1]["cost"])[:15]:
    print(f"    [{mt[:3]}] {text[:38]:40s} QS={e['qs'] or '-':>2} "
          f"impr={e['impr']:5d} clk={e['clk']:3d} ${e['cost']:6.2f}  {e['serve']}")

print()
print("=" * 78)
print("4) EXTENSIONS / ASSETS attached (ENABLED links only)")
print("=" * 78)
counts = defaultdict(int)
for r in ga.search(customer_id=cid, query=f"""
    SELECT campaign.id, campaign_asset.field_type, campaign_asset.status,
           campaign_asset.primary_status, asset.id
    FROM campaign_asset
    WHERE campaign.id = {CAMP} AND campaign_asset.status = 'ENABLED'"""):
    counts[r.campaign_asset.field_type.name] += 1
if counts:
    for ft, n in sorted(counts.items()):
        print(f"  {ft:26s} x{n}")
else:
    print("  (none)")

print()
print("=" * 78)
print("5) IMPRESSION SHARE: where are we losing? (LAST_14_DAYS)")
print("=" * 78)
for r in ga.search(customer_id=cid, query=f"""
    SELECT campaign.id, metrics.search_impression_share,
           metrics.search_rank_lost_impression_share,
           metrics.search_budget_lost_impression_share,
           metrics.impressions, metrics.clicks, metrics.cost_micros,
           metrics.average_cpc, metrics.ctr
    FROM campaign
    WHERE campaign.id = {CAMP} AND segments.date DURING LAST_14_DAYS"""):
    m = r.metrics
    print(f"  impr={m.impressions}  clicks={m.clicks}  cost=${m.cost_micros/1e6:.2f}"
          f"  CTR={m.ctr*100:.2f}%  avgCPC=${m.average_cpc/1e6:.2f}")
    print(f"  Search impression share ....... {m.search_impression_share*100:6.2f}%")
    print(f"  LOST to RANK (ad quality) ..... {m.search_rank_lost_impression_share*100:6.2f}%")
    print(f"  LOST to BUDGET ................ {m.search_budget_lost_impression_share*100:6.2f}%")
