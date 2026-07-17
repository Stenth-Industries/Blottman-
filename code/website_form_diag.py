"""Read-only: where does paid traffic actually land, and what fires there?"""
from dotenv import load_dotenv
import os, logging
from google.ads.googleads.client import GoogleAdsClient
logging.getLogger("google.ads.googleads").setLevel(logging.CRITICAL)
load_dotenv(r"E:\Blottman-law\.env")
client = GoogleAdsClient.load_from_dict({
    "developer_token": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
    "client_id": os.getenv("GOOGLE_ADS_CLIENT_ID"),
    "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
    "refresh_token": os.getenv("GOOGLE_ADS_REFRESH_TOKEN"),
    "login_customer_id": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),
    "use_proto_plus": True,
})
ga = client.get_service("GoogleAdsService")
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
def run(q): return list(ga.search(customer_id=cid, query=q))

print("\n=== LANDING PAGES actually clicked, LAST_14_DAYS ===")
for r in run("""
    SELECT landing_page_view.unexpanded_final_url, campaign.name,
           metrics.clicks, metrics.impressions
    FROM landing_page_view
    WHERE segments.date DURING LAST_14_DAYS AND metrics.clicks > 0
    ORDER BY metrics.clicks DESC
"""):
    print(f"  clicks {r.metrics.clicks:>4} | {r.campaign.name[:34]:<34} | {r.landing_page_view.unexpanded_final_url}")

print("\n=== Campaign tracking template / suffix (AI Max Jul-6 edits) ===")
for r in run("""
    SELECT campaign.name, campaign.tracking_url_template, campaign.final_url_suffix,
           campaign.status
    FROM campaign WHERE campaign.status = 'ENABLED'
"""):
    c = r.campaign
    print(f"  {c.name[:40]:<40}\n     tracking_url_template: {c.tracking_url_template or '(none)'}\n     final_url_suffix:      {c.final_url_suffix or '(none)'}")

print("\n=== Ad final URLs on the Search campaign (enabled ads) ===")
for r in run("""
    SELECT ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.final_urls,
           ad_group_ad.status
    FROM ad_group_ad
    WHERE campaign.id = 23971101309 AND ad_group_ad.status = 'ENABLED'
"""):
    print(f"  {r.ad_group.name[:30]:<30} | {list(r.ad_group_ad.ad.final_urls)}")
