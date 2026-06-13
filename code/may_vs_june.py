"""May vs June (1-12) performance comparison."""
from dotenv import load_dotenv
import os, logging
load_dotenv()
logging.getLogger("google.ads.googleads").setLevel(logging.CRITICAL)
cfg = {
    "developer_token": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
    "client_id": os.getenv("GOOGLE_ADS_CLIENT_ID"),
    "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
    "refresh_token": os.getenv("GOOGLE_ADS_REFRESH_TOKEN"),
    "login_customer_id": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),
    "use_proto_plus": True,
}
from google.ads.googleads.client import GoogleAdsClient
client = GoogleAdsClient.load_from_dict(cfg)
ga = client.get_service("GoogleAdsService")
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
def run(q): return list(ga.search(customer_id=cid, query=q))
def usd(m): return m / 1_000_000

periods = [
    ("MAY 2026 (full month)", "BETWEEN '2026-05-01' AND '2026-05-31'"),
    ("JUNE 2026 (Jun 1-12)", "BETWEEN '2026-06-01' AND '2026-06-12'"),
]

for label, period in periods:
    print(f"\n{'='*55}")
    print(f"  {label}")
    print(f"{'='*55}")

    # Account totals
    rows = run(f"""
        SELECT metrics.impressions, metrics.clicks, metrics.cost_micros,
               metrics.conversions, metrics.all_conversions
        FROM customer WHERE segments.date {period}
    """)
    impr = clicks = cost = conv = allconv = 0
    for r in rows:
        m = r.metrics
        impr += m.impressions; clicks += m.clicks
        cost += m.cost_micros; conv += m.conversions; allconv += m.all_conversions
    spend = usd(cost)
    ctr = clicks / impr * 100 if impr else 0
    cpc = spend / clicks if clicks else 0
    cpa = spend / conv if conv else 0
    print(f"  Impr {impr:>8,}  Clicks {clicks:>5,}  Spend ${spend:>8,.2f}")
    print(f"  Conv {conv:>5.0f}  AllConv {allconv:>5.0f}  CPA ${cpa:>7.2f}  CTR {ctr:.2f}%  CPC ${cpc:.2f}")

    # By campaign
    rows = run(f"""
        SELECT campaign.name, metrics.impressions, metrics.clicks,
               metrics.cost_micros, metrics.conversions, metrics.all_conversions
        FROM campaign
        WHERE segments.date {period} AND metrics.impressions > 0
        ORDER BY metrics.cost_micros DESC
    """)
    print(f"\n  {'Campaign'[:38]:38} {'Impr':>7} {'Clk':>4} {'Spend':>9} {'Conv':>5} {'CPA':>7}")
    for r in rows:
        m = r.metrics
        sp = usd(m.cost_micros)
        cpa_c = f"${sp/m.conversions:.0f}" if m.conversions > 0 else "-"
        print(f"  {r.campaign.name[:38]:38} {m.impressions:>7,} {m.clicks:>4} ${sp:>8,.2f} {m.conversions:>5.0f} {cpa_c:>7}")

    # Conversions by action
    rows = run(f"""
        SELECT conversion_action.name, metrics.all_conversions
        FROM conversion_action
        WHERE segments.date {period} AND metrics.all_conversions > 0
        ORDER BY metrics.all_conversions DESC
    """)
    print(f"\n  Conversions by action:")
    for r in rows:
        print(f"    {r.conversion_action.name[:42]:42} {r.metrics.all_conversions:.0f}")
