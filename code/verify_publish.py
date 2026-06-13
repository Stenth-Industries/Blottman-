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
print("\n  ADS in 'Traffic ticket lawyer broad':")
for r in ga.search(customer_id=cid, query="""
    SELECT ad_group_ad.ad.id, ad_group_ad.status,
           ad_group_ad.policy_summary.approval_status, ad_group_ad.ad.final_urls
    FROM ad_group_ad
    WHERE campaign.name='Traffic ticket lawyer broad' AND ad_group_ad.status!='REMOVED'"""):
    a = r.ad_group_ad
    print(f"    ad {a.ad.id}  status={a.status.name}  "
          f"approval={a.policy_summary.approval_status.name}  url={list(a.ad.final_urls)}")
print("\n  SITELINKS on campaign:")
for r in ga.search(customer_id=cid, query="""
    SELECT campaign.name, asset.sitelink_asset.link_text, campaign_asset.status
    FROM campaign_asset
    WHERE campaign.name='Traffic ticket lawyer broad' AND campaign_asset.field_type='SITELINK'"""):
    print(f"    - {r.asset.sitelink_asset.link_text}  ({r.campaign_asset.status.name})")
print()
