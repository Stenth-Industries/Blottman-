"""What ARE the 'Contact Us' conversions, and why does Leslie never see them?

Checks:
  1. The conversion action's own config (type/origin/counting/status).
  2. Where BMX actually sends traffic (asset group final URLs) - .com or .ca?
  3. Contact Us volume by campaign + network, last 14d.
  4. The REAL form action (Submit Lead Form - STENTH) for comparison.
Read-only.
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

CONTACT_US = 7262635666
SUBMIT_LEAD = 7173263227

print("=" * 78)
print("1) Conversion action config: Contact Us vs the real .ca form action")
print("=" * 78)
for aid in (CONTACT_US, SUBMIT_LEAD):
    for r in ga.search(customer_id=cid, query=f"""
        SELECT conversion_action.id, conversion_action.name, conversion_action.type,
               conversion_action.status, conversion_action.category, conversion_action.origin,
               conversion_action.counting_type, conversion_action.primary_for_goal,
               conversion_action.include_in_conversions_metric,
               conversion_action.click_through_lookback_window_days
        FROM conversion_action WHERE conversion_action.id = {aid}"""):
        c = r.conversion_action
        print(f"\n  [{c.id}] {c.name}")
        print(f"     type={c.type_.name}  origin={c.origin.name}  category={c.category.name}")
        print(f"     status={c.status.name}  counting={c.counting_type.name}")
        print(f"     primary={c.primary_for_goal}  in_conversions_metric={c.include_in_conversions_metric}")
        print(f"     lookback={c.click_through_lookback_window_days}d")

print()
print("=" * 78)
print("2) Where does BMX actually send traffic? (asset group final URLs)")
print("=" * 78)
for r in ga.search(customer_id=cid, query="""
    SELECT asset_group.id, asset_group.name, asset_group.status, asset_group.final_urls
    FROM asset_group WHERE campaign.name='PMAX - Blottman Max'"""):
    a = r.asset_group
    print(f"  [{a.id}] {a.name} status={a.status.name} urls={list(a.final_urls)}")

print("\n  --- Search Consolidated, for contrast (ad final URLs) ---")
seen = set()
for r in ga.search(customer_id=cid, query="""
    SELECT ad_group_ad.ad.final_urls, ad_group_ad.status
    FROM ad_group_ad
    WHERE campaign.name='Search - Ontario Traffic Tickets (Consolidated)'
      AND ad_group_ad.status='ENABLED'"""):
    for u in r.ad_group_ad.ad.final_urls:
        seen.add(u)
for u in sorted(seen):
    print(f"    {u}")

print()
print("=" * 78)
print("3) 'Contact Us' by campaign + network, last 14d (all_conversions)")
print("=" * 78)
agg = {}
for r in ga.search(customer_id=cid, query="""
    SELECT campaign.name, segments.ad_network_type, segments.conversion_action_name,
           metrics.all_conversions, metrics.conversions
    FROM campaign
    WHERE segments.date BETWEEN '2026-07-26' AND '2026-08-08'
      AND segments.conversion_action_name = 'Contact Us'"""):
    key = (r.campaign.name[:34], r.segments.ad_network_type.name)
    a = agg.setdefault(key, [0.0, 0.0])
    a[0] += r.metrics.all_conversions
    a[1] += r.metrics.conversions
for (camp, net), (acv, cv) in sorted(agg.items()):
    print(f"  {camp:36s} {net:16s} all={acv:6.2f} biddable={cv:5.2f}")

print()
print("=" * 78)
print("4) The REAL .ca form action (Submit Lead Form - STENTH), last 14d")
print("=" * 78)
tot = 0.0
for r in ga.search(customer_id=cid, query="""
    SELECT campaign.name, segments.conversion_action_name, metrics.all_conversions
    FROM campaign
    WHERE segments.date BETWEEN '2026-07-26' AND '2026-08-08'
      AND segments.conversion_action_name = 'Submit Lead Form - STENTH'"""):
    print(f"  {r.campaign.name[:36]:38s} all={r.metrics.all_conversions:.2f}")
    tot += r.metrics.all_conversions
print(f"  TOTAL real .ca form submissions in 14d: {tot:.0f}")
