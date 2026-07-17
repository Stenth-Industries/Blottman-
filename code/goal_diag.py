"""Read-only: why does the Search campaign say 'targeted goal is missing a primary
conversion action'? Dumps campaign conversion goals, account goals, and every
conversion action's category / origin / primary flag."""
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

SEARCH = "23971101309"

print("\n=== ENABLED CAMPAIGNS: bidding + goal config ===")
for r in ga.search(customer_id=cid, query="""
    SELECT campaign.id, campaign.name, campaign.status,
           campaign.advertising_channel_type,
           campaign.bidding_strategy_type,
           campaign.selective_optimization.conversion_actions
    FROM campaign WHERE campaign.status = 'ENABLED'
"""):
    c = r.campaign
    print(f"  {c.id} {c.name} | {c.advertising_channel_type.name} | {c.bidding_strategy_type.name}")
    if c.selective_optimization.conversion_actions:
        print("      selective_optimization:", list(c.selective_optimization.conversion_actions))

print("\n=== CAMPAIGN CONVERSION GOALS (Search consolidated) ===")
for r in ga.search(customer_id=cid, query=f"""
    SELECT campaign_conversion_goal.category, campaign_conversion_goal.origin,
           campaign_conversion_goal.biddable, campaign.id
    FROM campaign_conversion_goal
    WHERE campaign.id = {SEARCH}
"""):
    g = r.campaign_conversion_goal
    if g.biddable:
        print(f"  BIDDABLE  {g.category.name:<22} {g.origin.name}")

print("\n=== ACCOUNT-LEVEL (customer) CONVERSION GOALS ===")
for r in ga.search(customer_id=cid, query="""
    SELECT customer_conversion_goal.category, customer_conversion_goal.origin,
           customer_conversion_goal.biddable
    FROM customer_conversion_goal
"""):
    g = r.customer_conversion_goal
    if g.biddable:
        print(f"  BIDDABLE  {g.category.name:<22} {g.origin.name}")

print("\n=== CONVERSION ACTIONS (enabled) ===")
print(f"  {'id':<12} {'name':<40} {'category':<20} {'origin':<18} prim  inMetric")
for r in ga.search(customer_id=cid, query="""
    SELECT conversion_action.id, conversion_action.name, conversion_action.status,
           conversion_action.category, conversion_action.origin,
           conversion_action.primary_for_goal,
           conversion_action.include_in_conversions_metric,
           conversion_action.type
    FROM conversion_action
    WHERE conversion_action.status = 'ENABLED'
"""):
    a = r.conversion_action
    print(f"  {a.id:<12} {a.name[:39]:<40} {a.category.name:<20} {a.origin.name:<18} "
          f"{str(a.primary_for_goal):<5} {a.include_in_conversions_metric}")
