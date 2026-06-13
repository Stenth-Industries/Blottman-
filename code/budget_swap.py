"""Neutral budget swap (total unchanged at $35/day between the two Search campaigns):
  Traffic ticket lawyer broad (23039650759): $30 -> $20/day
  Traffic ticket lawyer       (23002273381): $5.01 -> $15/day
Resolves each campaign's budget resource, sanity-checks current amounts, applies, verifies."""
from dotenv import load_dotenv
import os, logging
from google.api_core import protobuf_helpers
from google.ads.googleads.client import GoogleAdsClient

logging.getLogger("google.ads.googleads").setLevel(logging.WARNING)
load_dotenv()
cfg = {
    "developer_token": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
    "client_id": os.getenv("GOOGLE_ADS_CLIENT_ID"),
    "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
    "refresh_token": os.getenv("GOOGLE_ADS_REFRESH_TOKEN"),
    "login_customer_id": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),
    "use_proto_plus": True,
}
client = GoogleAdsClient.load_from_dict(cfg)
ga = client.get_service("GoogleAdsService")
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")

TARGETS = {
    23039650759: ("Traffic ticket lawyer broad", 20.0),
    23002273381: ("Traffic ticket lawyer", 15.0),
}

rows = list(ga.search(customer_id=cid, query=f"""
    SELECT campaign.id, campaign.name, campaign_budget.resource_name,
           campaign_budget.amount_micros, campaign_budget.explicitly_shared
    FROM campaign WHERE campaign.id IN ({",".join(str(i) for i in TARGETS)})
"""))

ops = []
svc = client.get_service("CampaignBudgetService")
for r in rows:
    cmp_id = r.campaign.id
    name, new_daily = TARGETS[cmp_id]
    cur = r.campaign_budget.amount_micros / 1_000_000
    if r.campaign_budget.explicitly_shared:
        print(f"  !! {name}: budget is SHARED — skipping, needs manual review")
        continue
    print(f"  {name}: ${cur:.2f}/day -> ${new_daily:.2f}/day  ({r.campaign_budget.resource_name})")
    op = client.get_type("CampaignBudgetOperation")
    b = op.update
    b.resource_name = r.campaign_budget.resource_name
    b.amount_micros = int(new_daily * 1_000_000)
    client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, b._pb))
    ops.append(op)

if ops:
    res = svc.mutate_campaign_budgets(customer_id=cid, operations=ops)
    print(f"\n  Applied {len(res.results)} budget updates.")

# verify
rows = list(ga.search(customer_id=cid, query=f"""
    SELECT campaign.id, campaign.name, campaign_budget.amount_micros
    FROM campaign WHERE campaign.id IN ({",".join(str(i) for i in TARGETS)})
"""))
print("\n  Verified:")
for r in rows:
    print(f"    {r.campaign.name}: ${r.campaign_budget.amount_micros/1_000_000:.2f}/day")
