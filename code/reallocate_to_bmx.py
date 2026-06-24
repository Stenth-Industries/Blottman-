"""2026-06-24: Lever-2 reallocation (no budget increase, total stays $100/day). Move
$20/day from the Search campaigns (0 verified calls in 14d) into PMAX - Blottman Max
(the only call source). Reversible — old values in OLD{}. Run: python code/reallocate_to_bmx.py"""
from dotenv import load_dotenv
import os, logging
from google.ads.googleads.client import GoogleAdsClient
logging.getLogger("google.ads.googleads").setLevel(logging.ERROR)
load_dotenv()
cfg={k:os.getenv(v) for k,v in {"developer_token":"GOOGLE_ADS_DEVELOPER_TOKEN","client_id":"GOOGLE_ADS_CLIENT_ID","client_secret":"GOOGLE_ADS_CLIENT_SECRET","refresh_token":"GOOGLE_ADS_REFRESH_TOKEN","login_customer_id":"GOOGLE_ADS_LOGIN_CUSTOMER_ID"}.items()}
cfg["use_proto_plus"]=True
client=GoogleAdsClient.load_from_dict(cfg)
cid=os.getenv("GOOGLE_ADS_CUSTOMER_ID")
svc=client.get_service("CampaignBudgetService")

# budget_res : (new_dollars, old_dollars, label)
CHANGES = {
  "customers/8586214705/campaignBudgets/14910424501": (65, 45, "PMAX - Blottman Max"),
  "customers/8586214705/campaignBudgets/14912690384": (12, 20, "Traffic ticket lawyer"),
  "customers/8586214705/campaignBudgets/14746029755": ( 8, 15, "Lower Value - New"),
  "customers/8586214705/campaignBudgets/14945220177": ( 5, 10, "Traffic ticket lawyer broad"),
}
ops=[]
for res,(new,old,label) in CHANGES.items():
    op=client.get_type("CampaignBudgetOperation")
    op.update.resource_name=res
    op.update.amount_micros=int(new*1_000_000)
    op.update_mask.paths.append("amount_micros")
    ops.append(op)
svc.mutate_campaign_budgets(customer_id=cid, operations=ops)
print("Applied (total unchanged at $100/day):")
for res,(new,old,label) in CHANGES.items():
    print(f"  {label:32} ${old} -> ${new}")
print("  Higher Value - New: $5 (unchanged)\n  Blottman New pM: $5 (unchanged)")
print(f"  New total: ${65+12+8+5+5+5}/day")
