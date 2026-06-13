"""Dump all non-removed RSAs in the 'Traffic Ticket Lawyer Legal Services' ad group:
id, status, ad strength, final URL, paths, headlines (with pins), descriptions.
Used to confirm the 3 live ads + spot duplicates before /generate-ads."""
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
    SELECT ad_group.id, ad_group.name, ad_group_ad.ad.id, ad_group_ad.status,
           ad_group_ad.ad_strength, ad_group_ad.policy_summary.approval_status,
           ad_group_ad.policy_summary.review_status,
           ad_group_ad.ad.final_urls,
           ad_group_ad.ad.responsive_search_ad.path1,
           ad_group_ad.ad.responsive_search_ad.path2,
           ad_group_ad.ad.responsive_search_ad.headlines,
           ad_group_ad.ad.responsive_search_ad.descriptions
    FROM ad_group_ad
    WHERE campaign.name = '{NAME}' AND ad_group_ad.status != 'REMOVED'
    ORDER BY ad_group.id
"""):
    a = r.ad_group_ad
    rsa = a.ad.responsive_search_ad
    print(f"\n{'='*70}")
    print(f"  AD GROUP: {r.ad_group.name} (id {r.ad_group.id})")
    print(f"  AD id: {a.ad.id}   status={a.status.name}   strength={a.ad_strength.name}")
    print(f"  approval={a.policy_summary.approval_status.name}  review={a.policy_summary.review_status.name}")
    print(f"  FINAL URL: {list(a.ad.final_urls)}")
    print(f"  PATHS: /{rsa.path1}/{rsa.path2}")
    print(f"  HEADLINES ({len(rsa.headlines)}):")
    for h in rsa.headlines:
        pin = h.pinned_field.name if h.pinned_field else "-"
        print(f"    ({len(h.text):>2}) [{pin:<11}] {h.text}")
    print(f"  DESCRIPTIONS ({len(rsa.descriptions)}):")
    for d in rsa.descriptions:
        pin = d.pinned_field.name if d.pinned_field else "-"
        print(f"    ({len(d.text):>2}) [{pin:<11}] {d.text}")
print()
