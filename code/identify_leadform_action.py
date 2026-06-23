"""Read-only: list non-removed conversion actions with id/type/origin/primary_for_goal
so we can pinpoint the Google-hosted lead-form action to demote to secondary."""
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
    SELECT conversion_action.id, conversion_action.name, conversion_action.status,
           conversion_action.type, conversion_action.origin, conversion_action.category,
           conversion_action.primary_for_goal
    FROM conversion_action
    WHERE conversion_action.status != 'REMOVED'
    ORDER BY conversion_action.primary_for_goal DESC
"""))

print(f"\n  {'ID':<13}{'Name':<28}{'Status':<10}{'Origin':<14}{'Type':<22}{'Primary'}")
print("  " + "-"*100)
for r in rows:
    ca = r.conversion_action
    print(f"  {ca.id:<13}{ca.name[:27]:<28}{ca.status.name:<10}"
          f"{ca.origin.name:<14}{ca.type_.name[:21]:<22}{ca.primary_for_goal}")
print()
