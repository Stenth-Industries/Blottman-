"""Find the GA4 property linked to this Google Ads account (product_link)."""
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

try:
    rows = list(ga.search(customer_id=cid, query="""
        SELECT product_link.resource_name, product_link.type,
               product_link.google_ads.customer
        FROM product_link
    """))
    print(f"\n  product_link rows: {len(rows)}")
    for r in rows:
        pl = r.product_link
        print(f"  {pl.resource_name} | type={pl.type_.name}")
except Exception as e:
    print(f"  product_link query failed: {e}")

# data links / GA4 property via customer-level fields
try:
    rows = list(ga.search(customer_id=cid, query="""
        SELECT customer.id, customer.descriptive_name FROM customer
    """))
    for r in rows:
        print(f"\n  Ads account: {r.customer.descriptive_name} ({r.customer.id})")
except Exception as e:
    print(f"  customer query failed: {e}")
