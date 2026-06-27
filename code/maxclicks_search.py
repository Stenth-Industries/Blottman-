"""Switch the consolidated Search campaign (23971101309) from Manual CPC to
Maximize Clicks (TARGET_SPEND) to buy impression share while QS/conversion
history builds. BUDGET UNCHANGED at $30/day (per client). A $8 cpc bid ceiling
caps per-click cost so the daily budget buys click volume, not one click.

Revert: set bidding back to manual_cpc, or switch to Maximize Conversions once
the .ca Submit Lead Form signal accumulates enough volume to learn from.
"""
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

camp_svc = client.get_service("CampaignService")
o = client.get_type("CampaignOperation")
u = o.update
u.resource_name = f"customers/{cid}/campaigns/23971101309"
u.target_spend.cpc_bid_ceiling_micros = 8_000_000  # $8 ceiling
o.update_mask.paths.extend(["target_spend.cpc_bid_ceiling_micros"])
res = camp_svc.mutate_campaigns(customer_id=cid, operations=[o])
print("  updated:", res.results[0].resource_name)

ga = client.get_service("GoogleAdsService")
for r in ga.search(customer_id=cid, query=(
        "SELECT campaign.bidding_strategy_type, campaign_budget.amount_micros, "
        "campaign.target_spend.cpc_bid_ceiling_micros FROM campaign WHERE campaign.id=23971101309")):
    print(f"  bid={r.campaign.bidding_strategy_type.name}  "
          f"budget=${r.campaign_budget.amount_micros/1e6:.0f}/day  "
          f"cpc_ceiling=${r.campaign.target_spend.cpc_bid_ceiling_micros/1e6:.2f}")
