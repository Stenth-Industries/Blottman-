"""Full dump of campaign sitelinks (text, descriptions, URL, asset id) to dedupe."""
from dotenv import load_dotenv
import os, logging
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
c = GoogleAdsClient.load_from_dict(cfg)
ga = c.get_service("GoogleAdsService")
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
for r in ga.search(customer_id=cid, query="""
    SELECT campaign.name, campaign_asset.resource_name, asset.id,
           asset.sitelink_asset.link_text, asset.sitelink_asset.description1,
           asset.sitelink_asset.description2, asset.final_urls
    FROM campaign_asset
    WHERE campaign.name='Traffic ticket lawyer broad'
      AND campaign_asset.field_type='SITELINK'
    ORDER BY asset.sitelink_asset.link_text"""):
    s = r.asset.sitelink_asset
    print(f"\n  '{s.link_text}'  (asset {r.asset.id})")
    print(f"     d1: {s.description1!r}")
    print(f"     d2: {s.description2!r}")
    print(f"     url: {list(r.asset.final_urls)}")
    print(f"     campaign_asset: {r.campaign_asset.resource_name}")
print()
