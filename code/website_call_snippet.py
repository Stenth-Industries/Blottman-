"""Read-only: pull tag snippets + config for the 'Calls From Website' action
(7173397842, WEBSITE_CALL) so we can wire the phone-number snippet (number swap)
onto the landing page. Prints the global tag + phone snippet (AW- id + label)."""
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
    SELECT conversion_action.id, conversion_action.name, conversion_action.type,
           conversion_action.status, conversion_action.primary_for_goal,
           conversion_action.phone_call_duration_seconds,
           conversion_action.counting_type,
           conversion_action.value_settings.default_value,
           conversion_action.tag_snippets
    FROM conversion_action
    WHERE conversion_action.id = 7173397842
"""))
for r in rows:
    ca = r.conversion_action
    print(f"\n  {ca.name} ({ca.id})  type={ca.type_.name}  status={ca.status.name}")
    print(f"  primary_for_goal={ca.primary_for_goal}  "
          f"min_call_sec={ca.phone_call_duration_seconds}  "
          f"counting={ca.counting_type.name}  default_value={ca.value_settings.default_value}")
    for sn in ca.tag_snippets:
        print(f"\n  --- type={sn.type_.name} format={sn.page_format.name} ---")
        print("  GLOBAL SITE TAG:\n" + (sn.global_site_tag or "(none)"))
        print("  EVENT/PHONE SNIPPET:\n" + (sn.event_snippet or "(none)"))
