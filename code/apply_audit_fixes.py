"""Two audit fixes:
1. 'Traffic ticket lawyer' (23002273381): set TARGET_SPEND cpc_bid_ceiling = $10 (was uncapped).
2. 'Traffic ticket lawyer broad' (23039650759): turn OFF Display Network (was True).
Verifies both after."""
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
svc = client.get_service("CampaignService")

ops = []

# 1) CPC ceiling on TTL
op1 = client.get_type("CampaignOperation")
c1 = op1.update
c1.resource_name = f"customers/{cid}/campaigns/23002273381"
c1.target_spend.cpc_bid_ceiling_micros = 10_000_000
client.copy_from(op1.update_mask, protobuf_helpers.field_mask(None, c1._pb))
ops.append(op1)

# 2) Display Network off on broad
op2 = client.get_type("CampaignOperation")
c2 = op2.update
c2.resource_name = f"customers/{cid}/campaigns/23039650759"
c2.network_settings.target_content_network = False
# False is proto3 default -> field_mask(None, pb) would omit it; set the path explicitly
op2.update_mask.paths.append("network_settings.target_content_network")
ops.append(op2)

res = svc.mutate_campaigns(customer_id=cid, operations=ops)
print(f"  Applied {len(res.results)} campaign updates.")

rows = ga.search(customer_id=cid, query="""
    SELECT campaign.id, campaign.name, campaign.target_spend.cpc_bid_ceiling_micros,
           campaign.network_settings.target_content_network
    FROM campaign WHERE campaign.id IN (23002273381, 23039650759)
""")
print("\n  Verified:")
for r in rows:
    c = r.campaign
    print(f"    {c.name}: cpc_ceiling=${c.target_spend.cpc_bid_ceiling_micros/1e6:.2f}  "
          f"display_network={c.network_settings.target_content_network}")
