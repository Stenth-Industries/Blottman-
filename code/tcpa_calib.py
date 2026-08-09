"""Calibrate the right tCPA for BMX.

Key question: tCPA operates on BIDDABLE conversions (metrics.conversions),
NOT all_conversions and NOT stenth-only. The Jul-17 $95 was derived from
stenth-only CPA ($1583/17=$93). If biddable conv count >> stenth count,
then $95 is a far looser cap than intended.
"""
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
client = GoogleAdsClient.load_from_dict(cfg)
ga = client.get_service("GoogleAdsService")
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
BMX = "PMAX - Blottman Max"

PERIODS = [
    ("PRE  Jul14-27  (tCPA $95 in force)", "2026-07-14", "2026-07-27"),
    ("POST Jul28-Aug8 (uncapped)",         "2026-07-28", "2026-08-08"),
]

print("=" * 78)
print("A) BMX by network: cost vs BIDDABLE conversions vs all_conversions")
print("=" * 78)
for label, s, e in PERIODS:
    agg = {}
    for r in ga.search(customer_id=cid, query=f"""
        SELECT segments.ad_network_type, metrics.cost_micros,
               metrics.conversions, metrics.all_conversions
        FROM campaign
        WHERE campaign.name='{BMX}' AND segments.date BETWEEN '{s}' AND '{e}'"""):
        n = r.segments.ad_network_type.name
        a = agg.setdefault(n, [0.0, 0.0, 0.0])
        a[0] += r.metrics.cost_micros / 1e6
        a[1] += r.metrics.conversions
        a[2] += r.metrics.all_conversions
    print(f"\n--- {label} ---")
    tc = tcv = 0.0
    for n, (c, cv, acv) in sorted(agg.items()):
        tc += c; tcv += cv
        cpa = f"${c/cv:8.2f}" if cv else "     n/a"
        print(f"  {n:16s} cost=${c:8.2f}  biddable={cv:6.2f}  all={acv:6.2f}  CPA={cpa}")
    print(f"  {'TOTAL':16s} cost=${tc:8.2f}  biddable={tcv:6.2f}"
          f"  -> blended CPA={'$%.2f' % (tc/tcv) if tcv else 'n/a'}")

print()
print("=" * 78)
print("B) WHICH conversion actions, split by network (last 14d)")
print("=" * 78)
agg = {}
for r in ga.search(customer_id=cid, query=f"""
    SELECT segments.ad_network_type, segments.conversion_action_name,
           metrics.conversions, metrics.all_conversions
    FROM campaign
    WHERE campaign.name='{BMX}' AND segments.date BETWEEN '2026-07-26' AND '2026-08-08'"""):
    key = (r.segments.ad_network_type.name, r.segments.conversion_action_name)
    a = agg.setdefault(key, [0.0, 0.0])
    a[0] += r.metrics.conversions
    a[1] += r.metrics.all_conversions
for (net, action), (cv, acv) in sorted(agg.items()):
    flag = "  <-- BIDDABLE" if cv > 0 else ""
    print(f"  {net:16s} {action:42s} biddable={cv:6.2f} all={acv:6.2f}{flag}")

print()
print("=" * 78)
print("C) stenth-only (the real money signal) CPA by period")
print("=" * 78)
for label, s, e in PERIODS:
    st = 0.0
    for r in ga.search(customer_id=cid, query=f"""
        SELECT segments.conversion_action_name, metrics.all_conversions
        FROM campaign
        WHERE campaign.name='{BMX}' AND segments.date BETWEEN '{s}' AND '{e}'
          AND segments.conversion_action_name = 'Inbound call - Blottman (stenth)'"""):
        st += r.metrics.all_conversions
    cost = 0.0
    for r in ga.search(customer_id=cid, query=f"""
        SELECT metrics.cost_micros FROM campaign
        WHERE campaign.name='{BMX}' AND segments.date BETWEEN '{s}' AND '{e}'"""):
        cost += r.metrics.cost_micros / 1e6
    print(f"  {label}: cost=${cost:.2f}  stenth={st:.1f}"
          f"  -> stenth CPA={'$%.2f' % (cost/st) if st else 'n/a'}")
