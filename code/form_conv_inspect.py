"""Inspect form-related conversion actions: type, origin, tag snippets, 30d firing."""
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

print("\n  All non-removed actions: type / category / origin / counting\n")
rows = list(ga.search(customer_id=cid, query="""
    SELECT conversion_action.id, conversion_action.name, conversion_action.type,
           conversion_action.category, conversion_action.origin,
           conversion_action.status, conversion_action.primary_for_goal,
           conversion_action.counting_type,
           conversion_action.value_settings.default_value,
           conversion_action.value_settings.always_use_default_value
    FROM conversion_action
    WHERE conversion_action.status != 'REMOVED'
"""))
for r in rows:
    ca = r.conversion_action
    print(f"  [{ca.id}] {ca.name[:36]:36}")
    print(f"      type={ca.type_.name}  cat={ca.category.name}  origin={ca.origin.name}")
    print(f"      primary={ca.primary_for_goal}  counting={ca.counting_type.name}  "
          f"defval={ca.value_settings.default_value}  alwaysDefault={ca.value_settings.always_use_default_value}")

print("\n  30-day firing per action (all_conversions)\n")
rows = list(ga.search(customer_id=cid, query="""
    SELECT segments.conversion_action_name, metrics.all_conversions
    FROM customer
    WHERE segments.date DURING LAST_30_DAYS AND metrics.all_conversions > 0
"""))
agg = {}
for r in rows:
    agg[r.segments.conversion_action_name] = agg.get(r.segments.conversion_action_name, 0) + r.metrics.all_conversions
for name, v in sorted(agg.items(), key=lambda x: -x[1]):
    print(f"  {name[:40]:40} {v:>8.1f}")
