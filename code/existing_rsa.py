"""Dump the existing RSA in 'Traffic ticket lawyer broad' — final URL, paths,
headlines (with pins), descriptions. So a 2nd RSA matches the LP + differs in angle."""
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

for r in ga.search(customer_id=cid, query=f"""
    SELECT ad_group.id, ad_group.name, ad_group_ad.ad.id,
           ad_group_ad.ad.final_urls,
           ad_group_ad.ad.responsive_search_ad.path1,
           ad_group_ad.ad.responsive_search_ad.path2,
           ad_group_ad.ad.responsive_search_ad.headlines,
           ad_group_ad.ad.responsive_search_ad.descriptions
    FROM ad_group_ad
    WHERE campaign.name = '{NAME}' AND ad_group_ad.status != 'REMOVED'
"""):
    rsa = r.ad_group_ad.ad.responsive_search_ad
    print(f"\n  AD GROUP: {r.ad_group.name} (id {r.ad_group.id})")
    print(f"  AD id: {r.ad_group_ad.ad.id}")
    print(f"  FINAL URL: {list(r.ad_group_ad.ad.final_urls)}")
    print(f"  PATHS: /{rsa.path1}/{rsa.path2}")
    print("\n  HEADLINES:")
    for h in rsa.headlines:
        pin = h.pinned_field.name if h.pinned_field else "-"
        print(f"    ({len(h.text):>2}) [{pin:<11}] {h.text}")
    print("\n  DESCRIPTIONS:")
    for d in rsa.descriptions:
        pin = d.pinned_field.name if d.pinned_field else "-"
        print(f"    ({len(d.text):>2}) [{pin:<11}] {d.text}")
print()
