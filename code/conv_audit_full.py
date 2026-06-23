"""Read-only full conversion-action audit for Blottman Law.
Shows config (type/origin/primary/counting/value/min-call-sec) for every
non-removed action, joined with last-30-day volume (all_conversions / bid
conversions). No mutations."""
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

# 1) Config for every non-removed action
cfg = {}
for r in ga.search(customer_id=cid, query="""
    SELECT conversion_action.id, conversion_action.name, conversion_action.status,
           conversion_action.type, conversion_action.origin, conversion_action.category,
           conversion_action.primary_for_goal, conversion_action.counting_type,
           conversion_action.phone_call_duration_seconds,
           conversion_action.value_settings.default_value,
           conversion_action.value_settings.always_use_default_value
    FROM conversion_action
    WHERE conversion_action.status != 'REMOVED'
"""):
    ca = r.conversion_action
    cfg[str(ca.id)] = {
        "name": ca.name, "status": ca.status.name, "type": ca.type_.name,
        "origin": ca.origin.name, "primary": ca.primary_for_goal,
        "counting": ca.counting_type.name, "min_sec": ca.phone_call_duration_seconds,
        "defval": ca.value_settings.default_value,
        "always": ca.value_settings.always_use_default_value,
        "allconv": 0.0, "bidconv": 0.0,
    }

# 2) Last-30-day volume per action (account level)
for r in ga.search(customer_id=cid, query="""
    SELECT segments.conversion_action, segments.conversion_action_name,
           metrics.all_conversions, metrics.conversions
    FROM customer
    WHERE segments.date DURING LAST_30_DAYS
"""):
    rn = r.segments.conversion_action  # customers/x/conversionActions/ID
    aid = rn.split("/")[-1]
    if aid in cfg:
        cfg[aid]["allconv"] += r.metrics.all_conversions
        cfg[aid]["bidconv"] += r.metrics.conversions

print(f"\n  CONVERSION ACTIONS — config + last 30 days  (customer {cid})\n")
hdr = f"  {'ID':<12}{'Name':<30}{'Type':<16}{'Pri':<5}{'30d all':>9}{'30d bid':>9}{'Val':>6}"
print(hdr); print("  " + "-"*92)
for aid, c in sorted(cfg.items(), key=lambda kv: (-kv[1]["primary"], -kv[1]["allconv"])):
    pri = "P" if c["primary"] else "sec"
    val = f"${c['defval']:.0f}" if c["defval"] else "-"
    print(f"  {aid:<12}{c['name'][:29]:<30}{c['type'][:15]:<16}{pri:<5}"
          f"{c['allconv']:>9.1f}{c['bidconv']:>9.1f}{val:>6}")
print("\n  P = primary (used for bidding) · sec = secondary (observe only)")
print("  30d all = all_conversions · 30d bid = counted in 'Conversions' (bidding)\n")
