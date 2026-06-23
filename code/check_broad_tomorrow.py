"""Morning check after repointing 'Traffic ticket lawyer broad' (23039650759)
to blottman.ca. Read-only. Confirms: (1) both enabled RSAs' final URL + approval/
review status, (2) the ads are serving, (3) any conversions from the campaign
yesterday/today. Run: python code/check_broad_tomorrow.py"""
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

print("\n  === Broad RSAs: URL + approval/review status ===")
for r in ga.search(customer_id=cid, query=f"""
    SELECT ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.ad.final_urls,
           ad_group_ad.policy_summary.approval_status,
           ad_group_ad.policy_summary.review_status
    FROM ad_group_ad
    WHERE campaign.id = {BROAD} AND ad_group_ad.status = 'ENABLED'
"""):
    a = r.ad_group_ad
    ps = a.policy_summary
    urls = ", ".join(a.ad.final_urls)
    print(f"    ad {a.ad.id}: {urls}")
    print(f"       approval={ps.approval_status.name}  review={ps.review_status.name}")

print("\n  === Broad campaign delivery + conversions (last 2 days) ===")
for r in ga.search(customer_id=cid, query=f"""
    SELECT segments.date, metrics.impressions, metrics.clicks, metrics.cost_micros,
           metrics.conversions, metrics.all_conversions
    FROM campaign
    WHERE campaign.id = {BROAD} AND segments.date DURING LAST_2_DAYS
    ORDER BY segments.date
"""):
    m, d = r.metrics, r.segments.date
    print(f"    {d}: impr {m.impressions}  clk {m.clicks}  "
          f"${m.cost_micros/1e6:.2f}  conv {m.conversions:.1f}  allconv {m.all_conversions:.1f}")
print("\n  Goal: approval=APPROVED, ads serving, clicks landing on blottman.ca, a conversion showing.\n")
