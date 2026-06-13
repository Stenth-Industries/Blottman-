"""Inspect 'Traffic ticket lawyer broad' before enabling — Blottman Law.
Shows budget, bidding, locations, negative shared sets, ad/asset presence."""
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
NAME = "Traffic ticket lawyer broad"

# Campaign basics + budget + bidding
for r in ga.search(customer_id=cid, query=f"""
    SELECT campaign.id, campaign.name, campaign.status, campaign.bidding_strategy_type,
           campaign.maximize_conversions.target_cpa_micros,
           campaign.target_spend.cpc_bid_ceiling_micros,
           campaign_budget.amount_micros, campaign_budget.resource_name
    FROM campaign WHERE campaign.name = '{NAME}'
"""):
    c = r.campaign
    print(f"\n  CAMPAIGN: {c.name}  id={c.id}  status={c.status.name}")
    print(f"  bidding={c.bidding_strategy_type.name}  "
          f"cpc_ceiling=${c.target_spend.cpc_bid_ceiling_micros/1e6:.2f}")
    print(f"  budget=${r.campaign_budget.amount_micros/1e6:.2f}/day  "
          f"budget_res={r.campaign_budget.resource_name}")

# Location targeting
print("\n  LOCATIONS:")
loc = False
for r in ga.search(customer_id=cid, query=f"""
    SELECT campaign_criterion.location.geo_target_constant, campaign_criterion.negative,
           campaign_criterion.criterion_id
    FROM campaign_criterion
    WHERE campaign.name = '{NAME}' AND campaign_criterion.type = 'LOCATION'
"""):
    loc = True
    cc = r.campaign_criterion
    sign = "EXCLUDE" if cc.negative else "target "
    print(f"    {sign}  {cc.location.geo_target_constant}  (crit {cc.criterion_id})")
if not loc:
    print("    (none — campaign has NO location targeting!)")

# Negative shared sets attached
print("\n  NEGATIVE SHARED SETS:")
ns = False
for r in ga.search(customer_id=cid, query=f"""
    SELECT shared_set.name, shared_set.type, campaign_shared_set.status
    FROM campaign_shared_set WHERE campaign.name = '{NAME}'
"""):
    ns = True
    print(f"    {r.shared_set.name}  ({r.shared_set.type.name})")
if not ns:
    print("    (none attached)")

# Ads + call assets presence
print("\n  AD GROUPS / ADS:")
for r in ga.search(customer_id=cid, query=f"""
    SELECT ad_group.name, ad_group.status FROM ad_group
    WHERE campaign.name = '{NAME}' AND ad_group.status != 'REMOVED'
"""):
    print(f"    [{r.ad_group.status.name}] {r.ad_group.name}")
n_ads = len(list(ga.search(customer_id=cid, query=f"""
    SELECT ad_group_ad.ad.id FROM ad_group_ad
    WHERE campaign.name = '{NAME}' AND ad_group_ad.status != 'REMOVED'
""")))
print(f"    total ads: {n_ads}")
print()
