"""Full Google Ads account audit — Blottman Law"""

from dotenv import load_dotenv
import os
from google.ads.googleads.client import GoogleAdsClient

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

def run(query):
    return list(ga.search(customer_id=cid, query=query))

def divider(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")

def fmt(n): return f"{n:,.0f}"
def money(n): return f"${n:,.2f}"
def pct(n): return f"{n*100:.2f}%"
def micros(n): return n / 1_000_000


# ── 1. ACCOUNT SUMMARY ───────────────────────────────────────────────────────
divider("1. ACCOUNT SUMMARY — Last 30 Days")

rows = run("""
    SELECT
        metrics.impressions, metrics.clicks, metrics.ctr,
        metrics.cost_micros, metrics.conversions,
        metrics.cost_per_conversion, metrics.conversions_value
    FROM customer
    WHERE segments.date DURING LAST_30_DAYS
""")
m = rows[0].metrics
spend = micros(m.cost_micros)
cpa = micros(m.cost_per_conversion) if m.conversions else 0
print(f"  Impressions   : {fmt(m.impressions)}")
print(f"  Clicks        : {fmt(m.clicks)}")
print(f"  CTR           : {pct(m.ctr)}")
print(f"  Total Spend   : {money(spend)}")
print(f"  Conversions   : {m.conversions:.1f}")
print(f"  CPA           : {money(cpa)}")


# ── 2. CAMPAIGN PERFORMANCE — 30 days vs yesterday ──────────────────────────
divider("2. CAMPAIGN PERFORMANCE")

c30 = run("""
    SELECT campaign.name, metrics.impressions, metrics.clicks,
           metrics.ctr, metrics.cost_micros, metrics.conversions,
           metrics.cost_per_conversion, campaign.bidding_strategy_type
    FROM campaign
    WHERE campaign.status = 'ENABLED'
      AND segments.date DURING LAST_30_DAYS
""")

cy = run("""
    SELECT campaign.name, metrics.impressions, metrics.clicks,
           metrics.cost_micros, metrics.conversions
    FROM campaign
    WHERE campaign.status = 'ENABLED'
      AND segments.date DURING YESTERDAY
""")

yest = {r.campaign.name: r.metrics for r in cy}

print(f"\n  {'Campaign':<35} {'Impr':>8} {'Clicks':>7} {'CTR':>7} {'Spend':>9} {'Conv':>6} {'CPA':>9} | Yesterday Spend / Conv")
print(f"  {'-'*105}")
for r in c30:
    name = r.campaign.name
    m = r.metrics
    sp = micros(m.cost_micros)
    cpa = micros(m.cost_per_conversion) if m.conversions else 0
    y = yest.get(name)
    ysp = money(micros(y.cost_micros)) if y else "$0.00"
    yconv = f"{y.conversions:.1f}" if y else "0.0"
    print(f"  {name:<35} {fmt(m.impressions):>8} {fmt(m.clicks):>7} {pct(m.ctr):>7} {money(sp):>9} {m.conversions:>6.1f} {money(cpa):>9} | {ysp} / {yconv}")


# ── 3. BUDGETS ───────────────────────────────────────────────────────────────
divider("3. BUDGET UTILIZATION")

rows = run("""
    SELECT
        campaign.name,
        campaign_budget.amount_micros,
        campaign_budget.period,
        metrics.cost_micros
    FROM campaign
    WHERE campaign.status = 'ENABLED'
      AND segments.date DURING YESTERDAY
""")

print(f"\n  {'Campaign':<35} {'Daily Budget':>14} {'Yesterday Spend':>16} {'Utilization':>13}")
print(f"  {'-'*82}")
for r in rows:
    budget = micros(r.campaign_budget.amount_micros)
    spent = micros(r.metrics.cost_micros)
    util = (spent / budget * 100) if budget else 0
    bar = "#" * int(util / 5) + "-" * (20 - int(util / 5))
    print(f"  {r.campaign.name:<35} {money(budget):>14} {money(spent):>16} {util:>11.1f}%  [{bar}]")


# ── 4. DEVICE BREAKDOWN ──────────────────────────────────────────────────────
divider("4. DEVICE BREAKDOWN — Last 30 Days")

rows = run("""
    SELECT
        segments.device,
        metrics.impressions, metrics.clicks, metrics.ctr,
        metrics.cost_micros, metrics.conversions
    FROM campaign
    WHERE campaign.status = 'ENABLED'
      AND segments.date DURING LAST_30_DAYS
""")

devices = {}
for r in rows:
    d = r.segments.device.name
    m = r.metrics
    if d not in devices:
        devices[d] = {"impr": 0, "clicks": 0, "spend": 0, "conv": 0}
    devices[d]["impr"] += m.impressions
    devices[d]["clicks"] += m.clicks
    devices[d]["spend"] += micros(m.cost_micros)
    devices[d]["conv"] += m.conversions

print(f"\n  {'Device':<20} {'Impressions':>12} {'Clicks':>8} {'Spend':>10} {'Conv':>7} {'CPA':>10}")
print(f"  {'-'*72}")
for d, v in sorted(devices.items(), key=lambda x: -x[1]["spend"]):
    cpa = v["spend"] / v["conv"] if v["conv"] else 0
    print(f"  {d:<20} {fmt(v['impr']):>12} {fmt(v['clicks']):>8} {money(v['spend']):>10} {v['conv']:>7.1f} {money(cpa):>10}")


# ── 5. TOP GEOGRAPHIC AREAS ──────────────────────────────────────────────────
divider("5. TOP GEOGRAPHIC AREAS — Last 30 Days (by Spend)")

rows = run("""
    SELECT
        geographic_view.location_type,
        segments.geo_target_city,
        metrics.impressions, metrics.clicks,
        metrics.cost_micros, metrics.conversions
    FROM geographic_view
    WHERE segments.date DURING LAST_30_DAYS
    ORDER BY metrics.cost_micros DESC
    LIMIT 15
""")

print(f"\n  {'Location':<35} {'Impressions':>12} {'Clicks':>8} {'Spend':>10} {'Conv':>7}")
print(f"  {'-'*76}")
geo_svc = client.get_service("GeoTargetConstantService")
for r in rows:
    city_id = r.segments.geo_target_city.split("/")[-1] if r.segments.geo_target_city else ""
    try:
        geo = geo_svc.get_geo_target_constant(resource_name=r.segments.geo_target_city)
        loc = geo.canonical_name
    except Exception:
        loc = f"ID:{city_id}"
    m = r.metrics
    print(f"  {loc:<35} {fmt(m.impressions):>12} {fmt(m.clicks):>8} {money(micros(m.cost_micros)):>10} {m.conversions:>7.1f}")


# ── 6. ASSET GROUPS (PMAX) ───────────────────────────────────────────────────
divider("6. PMAX ASSET GROUPS")

rows = run("""
    SELECT
        campaign.name,
        asset_group.name,
        asset_group.status,
        metrics.impressions, metrics.clicks,
        metrics.cost_micros, metrics.conversions
    FROM asset_group
    WHERE campaign.status = 'ENABLED'
      AND segments.date DURING LAST_30_DAYS
""")

print(f"\n  {'Campaign':<28} {'Asset Group':<28} {'Status':<10} {'Impr':>8} {'Clicks':>7} {'Spend':>9} {'Conv':>6}")
print(f"  {'-'*102}")
for r in rows:
    m = r.metrics
    print(f"  {r.campaign.name:<28} {r.asset_group.name:<28} {r.asset_group.status.name:<10} {fmt(m.impressions):>8} {fmt(m.clicks):>7} {money(micros(m.cost_micros)):>9} {m.conversions:>6.1f}")


# ── 7. CHANGE HISTORY (yesterday) ───────────────────────────────────────────
divider("7. CHANGES MADE YESTERDAY")

rows = run("""
    SELECT
        change_event.change_date_time,
        change_event.change_resource_type,
        change_event.changed_fields,
        change_event.resource_name,
        change_event.user_email,
        change_event.client_type,
        change_event.campaign,
        change_event.new_resource,
        change_event.old_resource
    FROM change_event
    WHERE change_event.change_date_time DURING YESTERDAY
    ORDER BY change_event.change_date_time DESC
    LIMIT 50
""")

if not rows:
    print("\n  No changes recorded yesterday.")
else:
    print(f"\n  {'Time':<22} {'Type':<28} {'Campaign':<30} {'User':<30} {'Fields Changed'}")
    print(f"  {'-'*130}")
    for r in rows:
        e = r.change_event
        t = str(e.change_date_time)[:19].replace("T", " ")
        rtype = e.change_resource_type.name
        fields = ", ".join(e.changed_fields.paths) if e.changed_fields and e.changed_fields.paths else "—"
        camp = e.campaign.split("/")[-1] if e.campaign else "—"
        user = e.user_email if e.user_email else e.client_type.name
        print(f"  {t:<22} {rtype:<28} {camp:<30} {user:<30} {fields}")


# ── 8. CONVERSION ACTIONS ───────────────────────────────────────────────────
divider("8. CONVERSION ACTIONS — Last 30 Days")

rows = run("""
    SELECT
        conversion_action.name,
        conversion_action.status,
        conversion_action.type,
        metrics.conversions,
        metrics.all_conversions
    FROM conversion_action
    WHERE segments.date DURING LAST_30_DAYS
      AND conversion_action.status = 'ENABLED'
""")

print(f"\n  {'Conversion Action':<40} {'Type':<25} {'Conversions':>13} {'All Conv':>10}")
print(f"  {'-'*92}")
for r in rows:
    if r.metrics.all_conversions > 0:
        print(f"  {r.conversion_action.name:<40} {r.conversion_action.type_.name:<25} {r.metrics.conversions:>13.1f} {r.metrics.all_conversions:>10.1f}")

print("\n\nAudit complete.\n")
