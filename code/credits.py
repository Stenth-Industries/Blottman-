"""Billing adjustments / credits on the Blottman ad account (read-only).
'Adjustments' = Google's billing bucket for credits: promotional/coupon credits,
invalid-activity (invalid click) credits, over-delivery credits, manual refunds.
The API exposes the lifetime TOTAL on the account budget, not a dated per-credit
breakdown (that lives in Billing > Transactions in the UI). Run: python code/credits.py"""
from dotenv import load_dotenv
import os, logging
from google.ads.googleads.client import GoogleAdsClient
logging.getLogger("google.ads.googleads").setLevel(logging.ERROR)
load_dotenv()
cfg = {k: os.getenv(v) for k,v in {
    "developer_token":"GOOGLE_ADS_DEVELOPER_TOKEN","client_id":"GOOGLE_ADS_CLIENT_ID",
    "client_secret":"GOOGLE_ADS_CLIENT_SECRET","refresh_token":"GOOGLE_ADS_REFRESH_TOKEN",
    "login_customer_id":"GOOGLE_ADS_LOGIN_CUSTOMER_ID"}.items()}
cfg["use_proto_plus"]=True
ga = GoogleAdsClient.load_from_dict(cfg).get_service("GoogleAdsService")
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
d = lambda m: f"${m/1_000_000:,.2f}"

print("\n  === ACCOUNT BUDGETS (lifetime) ===")
for r in ga.search(customer_id=cid, query="""
  SELECT account_budget.id, account_budget.status, account_budget.amount_served_micros,
         account_budget.total_adjustments_micros
  FROM account_budget"""):
    b = r.account_budget
    print(f"  budget {b.id}  status={b.status.name}")
    print(f"     amount served (gross spend) : {d(b.amount_served_micros)}")
    print(f"     total adjustments / CREDITS : {d(b.total_adjustments_micros)}")
