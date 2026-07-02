"""BMX delivery split: per-day spend vs $65 budget, by network and device (last 7d)."""
import os, logging
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
BMX = "22979153470"
def run(q): return list(ga.search(customer_id=cid, query=q))
def usd(m): return m / 1_000_000

print("\n  === BMX: spend per day vs $65 budget (last 7d) ===")
rows = run(f"""
    SELECT segments.date, metrics.impressions, metrics.clicks,
           metrics.cost_micros, metrics.all_conversions
    FROM campaign
    WHERE campaign.id = {BMX} AND segments.date DURING LAST_7_DAYS
    ORDER BY segments.date
""")
print(f"  {'Date':12} {'Impr':>7} {'Clk':>4} {'Cost':>8} {'/$65':>6} {'Conv':>5}")
for r in rows:
    m = r.metrics
    cost = usd(m.cost_micros)
    print(f"  {r.segments.date:12} {m.impressions:>7} {m.clicks:>4} "
          f"${cost:>7.2f} {cost/65*100:>5.0f}% {m.all_conversions:>5.1f}")

print("\n  === BMX: by network (last 7d) ===")
rows = run(f"""
    SELECT segments.ad_network_type, metrics.impressions, metrics.clicks,
           metrics.cost_micros, metrics.all_conversions
    FROM campaign
    WHERE campaign.id = {BMX} AND segments.date DURING LAST_7_DAYS
""")
print(f"  {'Network':24} {'Impr':>7} {'Clk':>4} {'Cost':>8} {'Conv':>5}")
for r in rows:
    m = r.metrics
    net = r.segments.ad_network_type.name
    print(f"  {net:24} {m.impressions:>7} {m.clicks:>4} "
          f"${usd(m.cost_micros):>7.2f} {m.all_conversions:>5.1f}")

print("\n  === BMX: by device (last 7d) ===")
rows = run(f"""
    SELECT segments.device, metrics.impressions, metrics.clicks,
           metrics.cost_micros, metrics.all_conversions
    FROM campaign
    WHERE campaign.id = {BMX} AND segments.date DURING LAST_7_DAYS
""")
print(f"  {'Device':16} {'Impr':>7} {'Clk':>4} {'Cost':>8} {'Conv':>5}")
for r in rows:
    m = r.metrics
    print(f"  {r.segments.device.name:16} {m.impressions:>7} {m.clicks:>4} "
          f"${usd(m.cost_micros):>7.2f} {m.all_conversions:>5.1f}")
