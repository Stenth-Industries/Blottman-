"""Read-only: show enabled Search campaigns + the ads/final-URLs in
'Traffic ticket lawyer broad' (23039650759) so we can repoint ONE campaign
to blottman.ca as a staged test. No mutations."""
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
BROAD = "23039650759"

print("\n  ENABLED campaigns:")
for r in ga.search(customer_id=cid, query="""
    SELECT campaign.id, campaign.name, campaign.advertising_channel_type
    FROM campaign WHERE campaign.status = 'ENABLED' ORDER BY campaign.name
"""):
    c = r.campaign
    print(f"    {c.id:<13}{c.advertising_channel_type.name:<10}{c.name}")

print(f"\n  Ads in 'Traffic ticket lawyer broad' ({BROAD}):")
for r in ga.search(customer_id=cid, query=f"""
    SELECT ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.ad.type,
           ad_group_ad.ad.final_urls, ad_group.id
    FROM ad_group_ad
    WHERE campaign.id = {BROAD} AND ad_group_ad.status != 'REMOVED'
"""):
    a = r.ad_group_ad
    urls = ", ".join(a.ad.final_urls) or "(none)"
    print(f"    ad {a.ad.id:<14}{a.status.name:<9}{a.ad.type_.name:<22}-> {urls}")
print()
