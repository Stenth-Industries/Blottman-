"""One-off: list conversion actions with status / primary-for-goal / counting — Blottman Law.
Reveals whether Max Conversions is bidding toward an action that isn't firing."""
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

rows = list(ga.search(customer_id=cid, query="""
    SELECT conversion_action.name, conversion_action.status, conversion_action.type,
           conversion_action.category, conversion_action.primary_for_goal,
           conversion_action.counting_type, conversion_action.value_settings.default_value
    FROM conversion_action
    WHERE conversion_action.status != 'REMOVED'
    ORDER BY conversion_action.primary_for_goal DESC
"""))

print("\n  Conversion actions (non-removed)\n")
print(f"  {'Name':<40}{'Status':<10}{'Primary':<8}{'DefVal':>8}")
print("  " + "-"*68)
for r in rows:
    ca = r.conversion_action
    print(f"  {ca.name[:39]:<40}{ca.status.name:<10}"
          f"{str(ca.primary_for_goal):<8}{ca.value_settings.default_value:>8.0f}")
print()
