"""Deep-dive a single day (default YESTERDAY): campaigns, devices, geo, search terms."""
import os, sys, logging
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
PERIOD = sys.argv[1].upper() if len(sys.argv) > 1 else "YESTERDAY"
def run(q): return list(ga.search(customer_id=cid, query=q))
def usd(m): return m / 1_000_000

print(f"\n  === {PERIOD}: campaigns (enabled, with traffic) ===")
rows = run(f"""
    SELECT campaign.name, campaign.advertising_channel_type,
           metrics.impressions, metrics.clicks, metrics.cost_micros,
           metrics.conversions, metrics.all_conversions, metrics.average_cpc
    FROM campaign
    WHERE segments.date DURING {PERIOD} AND campaign.status = 'ENABLED'
      AND metrics.impressions > 0
    ORDER BY metrics.cost_micros DESC
""")
print(f"  {'Campaign':32} {'Impr':>6} {'Clk':>4} {'Cost':>8} {'CPC':>6} {'AllConv':>7}")
for r in rows:
    m = r.metrics
    print(f"  {r.campaign.name[:32]:32} {m.impressions:>6} {m.clicks:>4} "
          f"${usd(m.cost_micros):>7.2f} ${usd(m.average_cpc):>5.2f} {m.all_conversions:>7.1f}")

print(f"\n  === {PERIOD}: by device (account) ===")
rows = run(f"""
    SELECT segments.device, metrics.impressions, metrics.clicks,
           metrics.cost_micros, metrics.all_conversions
    FROM customer WHERE segments.date DURING {PERIOD}
""")
for r in rows:
    m = r.metrics
    print(f"  {r.segments.device.name:10} impr {m.impressions:>5} | clk {m.clicks:>3} | "
          f"${usd(m.cost_micros):>7.2f} | allconv {m.all_conversions:.1f}")

print(f"\n  === {PERIOD}: search terms (Search campaigns) ===")
rows = run(f"""
    SELECT campaign.name, search_term_view.search_term, segments.keyword.info.text,
           metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.all_conversions
    FROM search_term_view
    WHERE segments.date DURING {PERIOD}
    ORDER BY metrics.cost_micros DESC
""")
if not rows:
    print("  (no search-term rows)")
for r in rows:
    m = r.metrics
    print(f"  [{r.campaign.name[:20]:20}] \"{r.search_term_view.search_term[:42]:42}\" "
          f"impr {m.impressions:>3} clk {m.clicks:>2} ${usd(m.cost_micros):>6.2f} conv {m.all_conversions:.1f}")

print(f"\n  === {PERIOD}: geo (user location, top by cost) ===")
rows = run(f"""
    SELECT geographic_view.country_criterion_id, segments.geo_target_city,
           metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.all_conversions
    FROM geographic_view
    WHERE segments.date DURING {PERIOD} AND metrics.impressions > 0
    ORDER BY metrics.cost_micros DESC
""")
geo = {}
for r in rows:
    key = r.segments.geo_target_city or "unknown"
    g = geo.setdefault(key, [0, 0, 0, 0.0])
    g[0] += r.metrics.impressions; g[1] += r.metrics.clicks
    g[2] += r.metrics.cost_micros; g[3] += r.metrics.all_conversions
ids = [k.split("/")[-1] for k in geo if k != "unknown"]
names = {}
if ids:
    gt = run("SELECT geo_target_constant.resource_name, geo_target_constant.name "
             "FROM geo_target_constant WHERE geo_target_constant.id IN (" + ",".join(ids) + ")")
    names = {r.geo_target_constant.resource_name: r.geo_target_constant.name for r in gt}
for k, g in sorted(geo.items(), key=lambda x: -x[1][2])[:15]:
    label = names.get(k, k)
    print(f"  {label[:28]:28} impr {g[0]:>5} | clk {g[1]:>3} | ${usd(g[2]):>7.2f} | conv {g[3]:.1f}")
