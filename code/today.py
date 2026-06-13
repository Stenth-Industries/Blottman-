"""Today's snapshot — Blottman Law. Run: python today.py"""
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

for label, clause in (("TODAY", "TODAY"), ("YESTERDAY", "YESTERDAY")):
    rows = run(f"""
        SELECT metrics.impressions, metrics.clicks, metrics.cost_micros,
               metrics.conversions, metrics.all_conversions
        FROM customer WHERE segments.date DURING {clause}
    """)
    m = rows[0].metrics if rows else None
    if m:
        print(f"\n  === {label} (account) ===")
        print(f"  Impr {m.impressions:,.0f} | Clicks {m.clicks:,.0f} | "
              f"Spend ${micros(m.cost_micros):,.2f} | Conv {m.conversions:.1f} | "
              f"AllConv {m.all_conversions:.1f}")

print("\n  === TODAY by campaign (enabled) ===")
print(f"  {'Campaign':<32} {'Impr':>7} {'Clk':>5} {'Spend':>9} {'Conv':>6}")
print("  " + "-"*64)
for r in run("""
    SELECT campaign.name, metrics.impressions, metrics.clicks,
           metrics.cost_micros, metrics.conversions
    FROM campaign WHERE campaign.status='ENABLED' AND segments.date DURING TODAY
    ORDER BY metrics.cost_micros DESC
"""):
    m = r.metrics
    print(f"  {r.campaign.name:<32} {m.impressions:>7,.0f} {m.clicks:>5,.0f} "
          f"${micros(m.cost_micros):>8,.2f} {m.conversions:>6.1f}")

print("\n  === TODAY conversions by action (all_conversions>0) ===")
hit = False
for r in run("""
    SELECT segments.conversion_action_name, metrics.all_conversions,
           metrics.all_conversions_value
    FROM customer WHERE segments.date DURING TODAY
"""):
    if r.metrics.all_conversions > 0:
        hit = True
        print(f"  {r.segments.conversion_action_name:<42} "
              f"{r.metrics.all_conversions:>6.1f}  ${r.metrics.all_conversions_value:,.2f}")
if not hit:
    print("  (no conversions recorded yet today)")
print()
