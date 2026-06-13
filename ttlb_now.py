"""Current delivery + status for 'Traffic ticket lawyer broad'."""
from dotenv import load_dotenv
import os, logging
from google.ads.googleads.client import GoogleAdsClient
logging.getLogger("google.ads.googleads").setLevel(logging.WARNING)
load_dotenv()
config = {k: os.getenv(v) for k,v in {
    "developer_token":"GOOGLE_ADS_DEVELOPER_TOKEN","client_id":"GOOGLE_ADS_CLIENT_ID",
    "client_secret":"GOOGLE_ADS_CLIENT_SECRET","refresh_token":"GOOGLE_ADS_REFRESH_TOKEN",
    "login_customer_id":"GOOGLE_ADS_LOGIN_CUSTOMER_ID"}.items()}
config["use_proto_plus"]=True
client = GoogleAdsClient.load_from_dict(config)
ga = client.get_service("GoogleAdsService")
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
NAME = "Traffic ticket lawyer broad"
def m(x): return x/1e6

for r in ga.search(customer_id=cid, query=f"""
    SELECT campaign.status, campaign.serving_status, campaign_budget.amount_micros
    FROM campaign WHERE campaign.name = '{NAME}'"""):
    print(f"status={r.campaign.status.name}  serving={r.campaign.serving_status.name}  "
          f"budget=${m(r.campaign_budget.amount_micros):.2f}/day")

print("\nTODAY / YESTERDAY:")
for seg in ("TODAY","YESTERDAY"):
    rows=list(ga.search(customer_id=cid, query=f"""
        SELECT segments.date, metrics.impressions, metrics.clicks, metrics.cost_micros,
               metrics.conversions
        FROM campaign WHERE campaign.name='{NAME}' AND segments.date DURING {seg}"""))
    if not rows: print(f"  {seg}: no rows"); continue
    for r in rows:
        s=r.metrics
        print(f"  {seg} {r.segments.date}: impr={s.impressions} clk={s.clicks} "
              f"cost=${m(s.cost_micros):.2f} conv={s.conversions:.1f}")

print("\nLAST_14_DAYS daily:")
for r in ga.search(customer_id=cid, query=f"""
    SELECT segments.date, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions
    FROM campaign WHERE campaign.name='{NAME}' AND segments.date DURING LAST_14_DAYS
    ORDER BY segments.date"""):
    s=r.metrics
    print(f"  {r.segments.date}: impr={s.impressions:>4} clk={s.clicks:>3} "
          f"cost=${m(s.cost_micros):>6.2f} conv={s.conversions:.1f}")
