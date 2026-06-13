"""One-off: campaign primary status + reasons + budget — Blottman Law.
Tells us WHY delivery stopped (eligibility / billing / budget / learning)."""
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

# Account status first
for r in ga.search(customer_id=cid, query="""
    SELECT customer.descriptive_name, customer.status, customer.id
    FROM customer
"""):
    c = r.customer
    print(f"\n  ACCOUNT: {c.descriptive_name} ({c.id}) — status {c.status.name}")

print("\n  Campaigns: status / primary status / reasons / budget\n")
for r in ga.search(customer_id=cid, query="""
    SELECT campaign.name, campaign.status, campaign.primary_status,
           campaign.primary_status_reasons, campaign.bidding_strategy_type,
           campaign_budget.amount_micros
    FROM campaign
    WHERE campaign.status != 'REMOVED'
    ORDER BY campaign.status
"""):
    c = r.campaign
    reasons = ", ".join(x.name for x in c.primary_status_reasons) or "-"
    budget = r.campaign_budget.amount_micros / 1e6
    print(f"  {c.name[:34]:<35}")
    print(f"      status={c.status.name}  primary={c.primary_status.name}  "
          f"bid={c.bidding_strategy_type.name}  budget=${budget:.2f}/day")
    print(f"      reasons: {reasons}")
print()
