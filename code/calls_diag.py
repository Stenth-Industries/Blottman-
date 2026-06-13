"""One-off: daily clicks/cost vs conversions, last 7 days — Blottman Law.
Separates a TRACKING break (clicks steady, conv=0) from a DELIVERY drop (clicks also fall)."""
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
    SELECT segments.date, metrics.impressions, metrics.clicks, metrics.cost_micros,
           metrics.conversions, metrics.all_conversions
    FROM customer WHERE segments.date DURING LAST_7_DAYS
    ORDER BY segments.date
"""))

print("\n  Daily delivery vs conversions - last 7 days\n")
print(f"  {'Date':<12}{'Impr':>9}{'Clicks':>8}{'Spend':>10}{'Conv':>7}{'AllConv':>9}")
print("  " + "-"*55)
for r in rows:
    m = r.metrics
    print(f"  {str(r.segments.date):<12}{m.impressions:>9,.0f}{m.clicks:>8,.0f}"
          f"${m.cost_micros/1e6:>9,.2f}{m.conversions:>7.1f}{m.all_conversions:>9.1f}")
print()
