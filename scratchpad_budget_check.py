"""Ad-hoc: find every campaign_budget resource on the account (shared or not),
its amount (daily + implied monthly), delivery method, and which campaigns use it.
Also checks for any account-level billing budget object exposed via the API."""
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

print("=== ALL CAMPAIGN BUDGETS (incl. any not currently attached to a live campaign) ===")
for r in ga.search(customer_id=cid, query="""
    SELECT campaign_budget.id, campaign_budget.name, campaign_budget.amount_micros,
           campaign_budget.status, campaign_budget.explicitly_shared,
           campaign_budget.delivery_method, campaign_budget.reference_count,
           campaign_budget.period, campaign_budget.type
    FROM campaign_budget
    ORDER BY campaign_budget.amount_micros DESC
"""):
    b = r.campaign_budget
    daily = b.amount_micros / 1e6
    monthly = daily * 30.4
    print(f"  id={b.id:<12} '{b.name}' status={b.status.name} shared={b.explicitly_shared} "
          f"refs={b.reference_count} period={b.period.name} type={b.type_.name} "
          f"daily=${daily:,.2f}  ~monthly=${monthly:,.2f}")

print("\n=== Which campaigns point at each budget ===")
for r in ga.search(customer_id=cid, query="""
    SELECT campaign.name, campaign.status, campaign_budget.id, campaign_budget.name,
           campaign_budget.amount_micros
    FROM campaign
    WHERE campaign.status != 'REMOVED'
    ORDER BY campaign_budget.amount_micros DESC
"""):
    c = r.campaign
    b = r.campaign_budget
    print(f"  {c.name:<45} status={c.status.name:<10} -> budget '{b.name}' (id={b.id}) ${b.amount_micros/1e6:,.2f}/day")

print("\n=== Account info ===")
for r in ga.search(customer_id=cid, query="""
    SELECT customer.descriptive_name, customer.id, customer.currency_code,
           customer.manager, customer.test_account
    FROM customer
"""):
    c = r.customer
    print(f"  {c.descriptive_name} ({c.id}) currency={c.currency_code} manager={c.manager} test={c.test_account}")
