"""Impressions diagnosis — Blottman Law. Per-day delivery + budget context."""
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
def run(q): return list(ga.search(customer_id=cid, query=q))
def micros(n): return n / 1_000_000

# 1. Per-day account totals, last 14 days
print("\n=== ACCOUNT: per-day, last 14 days ===")
print(f"  {'Date':<12} {'Impr':>8} {'Clicks':>7} {'Spend':>9} {'Conv':>6}")
print("  " + "-"*48)
for r in run("""
    SELECT segments.date, metrics.impressions, metrics.clicks,
           metrics.cost_micros, metrics.conversions
    FROM customer WHERE segments.date DURING LAST_14_DAYS
    ORDER BY segments.date
"""):
    m = r.metrics
    print(f"  {r.segments.date:<12} {m.impressions:>8,.0f} {m.clicks:>7,.0f} "
          f"${micros(m.cost_micros):>8,.2f} {m.conversions:>6.1f}")

# 2. Per-campaign per-day, last 5 days (enabled)
print("\n=== PER CAMPAIGN x DAY, last 5 days (enabled) ===")
print(f"  {'Date':<12} {'Campaign':<30} {'Impr':>7} {'Spend':>9} {'Conv':>5} {'Status'}")
print("  " + "-"*72)
for r in run("""
    SELECT segments.date, campaign.name, campaign.status,
           campaign.serving_status,
           metrics.impressions, metrics.cost_micros, metrics.conversions
    FROM campaign WHERE segments.date DURING LAST_7_DAYS
      AND campaign.status='ENABLED'
    ORDER BY segments.date, metrics.cost_micros DESC
"""):
    m = r.metrics
    print(f"  {r.segments.date:<12} {r.campaign.name:<30} {m.impressions:>7,.0f} "
          f"${micros(m.cost_micros):>8,.2f} {m.conversions:>5.1f} {r.campaign.serving_status.name}")

# 3. Budget + utilization yesterday
print("\n=== BUDGET vs YESTERDAY SPEND ===")
for r in run("""
    SELECT campaign.name, campaign_budget.amount_micros,
           metrics.cost_micros
    FROM campaign WHERE campaign.status='ENABLED' AND segments.date DURING YESTERDAY
"""):
    b = micros(r.campaign_budget.amount_micros)
    s = micros(r.metrics.cost_micros)
    util = (s/b*100) if b else 0
    print(f"  {r.campaign.name:<32} budget ${b:>6.2f}  spent ${s:>6.2f}  ({util:>5.1f}%)")

# 4. PMAX asset group ad strength + status (delivery health)
print("\n=== PMAX ASSET GROUPS — status / ad strength ===")
for r in run("""
    SELECT campaign.name, asset_group.name, asset_group.status,
           asset_group.ad_strength,
           metrics.impressions, metrics.conversions
    FROM asset_group WHERE campaign.status='ENABLED'
      AND segments.date DURING LAST_7_DAYS
"""):
    m = r.metrics
    print(f"  {r.campaign.name:<28} {r.asset_group.name:<26} "
          f"{r.asset_group.status.name:<8} {r.asset_group.ad_strength.name:<12} "
          f"impr7d {m.impressions:>6,.0f} conv {m.conversions:.1f}")
print()
