"""THE daily leads report — Blottman Law. Run: python code/leads.py
Always reads ALL conversions (never the misleading primary-only 'Conversions' column).
Shows: today + yesterday account totals, leads by campaign x action, 7-day trend, recent calls.
"""
from dotenv import load_dotenv
import os, logging
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
def run(q): return list(ga.search(customer_id=cid, query=q))
def usd(m): return m / 1_000_000

print("\n  ============ BLOTTMAN LEADS REPORT (all conversions) ============")
print("  (account day = Toronto time; reporting lags ~3h)")

for label in ("TODAY", "YESTERDAY"):
    rows = run(f"""
        SELECT metrics.impressions, metrics.clicks, metrics.cost_micros,
               metrics.all_conversions
        FROM customer WHERE segments.date DURING {label}
    """)
    m = rows[0].metrics if rows else None
    if m:
        print(f"\n  === {label} ===  impr {m.impressions} | clicks {m.clicks} | "
              f"spend ${usd(m.cost_micros):.2f} | LEADS {m.all_conversions:.0f}")
    rows = run(f"""
        SELECT campaign.name, segments.conversion_action_name, metrics.all_conversions
        FROM campaign
        WHERE segments.date DURING {label} AND metrics.all_conversions > 0
        ORDER BY metrics.all_conversions DESC
    """)
    for r in rows:
        print(f"      {r.campaign.name[:32]:32} | {r.segments.conversion_action_name[:30]:30} | "
              f"{r.metrics.all_conversions:.1f}")
    if not rows:
        print("      (no leads recorded yet)")

print("\n  === LAST 7 DAYS: leads by action ===")
rows = run("""
    SELECT segments.conversion_action_name, metrics.all_conversions
    FROM customer
    WHERE segments.date DURING LAST_7_DAYS AND metrics.all_conversions > 0
""")
agg = {}
for r in rows:
    agg[r.segments.conversion_action_name] = agg.get(r.segments.conversion_action_name, 0) + r.metrics.all_conversions
for name, v in sorted(agg.items(), key=lambda x: -x[1]):
    print(f"      {name[:40]:40} {v:>6.1f}")

print("\n  === 10 MOST RECENT CALLS (from call assets) ===")
rows = run("""
    SELECT call_view.start_call_date_time, call_view.call_duration_seconds,
           call_view.caller_area_code, call_view.call_status, campaign.name
    FROM call_view
""")
rows.sort(key=lambda r: r.call_view.start_call_date_time, reverse=True)
for r in rows[:10]:
    cv = r.call_view
    print(f"      {cv.start_call_date_time} | {cv.call_duration_seconds:>4}s | "
          f"area {cv.caller_area_code or '?':>3} | {cv.call_status.name:8} | {r.campaign.name[:26]}")
print()
