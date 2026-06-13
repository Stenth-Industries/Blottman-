"""Pull the gtag snippets for 'Submit Lead Form' (7173263227) so it can be installed on blottman.com."""
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
    SELECT conversion_action.id, conversion_action.name, conversion_action.tag_snippets
    FROM conversion_action
    WHERE conversion_action.id = 7173263227
"""))
for r in rows:
    ca = r.conversion_action
    print(f"\n  Action: {ca.name} ({ca.id})  snippets: {len(ca.tag_snippets)}")
    for sn in ca.tag_snippets:
        print(f"\n  --- type={sn.type_.name} format={sn.page_format.name} ---")
        print("  GLOBAL SITE TAG:")
        print(sn.global_site_tag)
        print("  EVENT SNIPPET:")
        print(sn.event_snippet)
