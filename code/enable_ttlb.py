"""Configure + enable 'Traffic ticket lawyer broad' as an emergency lead tap.
Order = budget -> locations -> cpc cap + presence targeting -> ENABLE (last).
Stops before enabling if any earlier step errors."""
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
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")

CAMP_ID = "23039650759"
CAMP_RES = f"customers/{cid}/campaigns/{CAMP_ID}"
BUDGET_RES = f"customers/{cid}/campaignBudgets/14945220177"
CITIES = [1002451, 1002191, 1002350, 1002287]  # Toronto, Brampton, Mississauga, Hamilton

# 1) Budget -> $30/day
bsvc = client.get_service("CampaignBudgetService")
bop = client.get_type("CampaignBudgetOperation")
bop.update.resource_name = BUDGET_RES
bop.update.amount_micros = 30_000_000
bop.update_mask.paths.append("amount_micros")
bsvc.mutate_campaign_budgets(customer_id=cid, operations=[bop])
print("  [1/4] Budget set to $30.00/day")

# 2) Add 4 city locations (presence targeting handled in step 3)
csvc = client.get_service("CampaignCriterionService")
ops = []
for geo_id in CITIES:
    op = client.get_type("CampaignCriterionOperation")
    cc = op.create
    cc.campaign = CAMP_RES
    cc.location.geo_target_constant = f"geoTargetConstants/{geo_id}"
    ops.append(op)
csvc.mutate_campaign_criteria(customer_id=cid, operations=ops)
print(f"  [2/4] Added {len(CITIES)} city locations (Toronto, Brampton, Mississauga, Hamilton)")

# 3) CPC ceiling $10 + PRESENCE geo targeting
camp_svc = client.get_service("CampaignService")
op = client.get_type("CampaignOperation")
op.update.resource_name = CAMP_RES
op.update.target_spend.cpc_bid_ceiling_micros = 10_000_000
op.update.geo_target_type_setting.positive_geo_target_type = (
    client.enums.PositiveGeoTargetTypeEnum.PRESENCE)
op.update.geo_target_type_setting.negative_geo_target_type = (
    client.enums.NegativeGeoTargetTypeEnum.PRESENCE)
op.update_mask.paths.extend([
    "target_spend.cpc_bid_ceiling_micros",
    "geo_target_type_setting.positive_geo_target_type",
    "geo_target_type_setting.negative_geo_target_type",
])
camp_svc.mutate_campaigns(customer_id=cid, operations=[op])
print("  [3/4] CPC ceiling $10.00 + PRESENCE-only geo targeting set")

# 4) ENABLE (last)
op = client.get_type("CampaignOperation")
op.update.resource_name = CAMP_RES
op.update.status = client.enums.CampaignStatusEnum.ENABLED
op.update_mask.paths.append("status")
camp_svc.mutate_campaigns(customer_id=cid, operations=[op])
print("  [4/4] Campaign ENABLED ✅  — 'Traffic ticket lawyer broad' is now live")
print()
