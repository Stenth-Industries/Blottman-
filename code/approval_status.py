"""Account-wide ad approval check. Read-only. Lists every enabled/paused ad on
every ENABLED campaign with its approval + review status, final URL, and any
policy topics. Surfaces what is NOT approved. Run: python code/approval_status.py"""
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

print("\n=== ENABLED-campaign ADS: approval / review status ===")
rows = ga.search(customer_id=cid, query="""
    SELECT campaign.name, campaign.id, campaign.advertising_channel_type,
           ad_group.name, ad_group_ad.ad.id, ad_group_ad.status,
           ad_group_ad.ad.type, ad_group_ad.ad.final_urls,
           ad_group_ad.policy_summary.approval_status,
           ad_group_ad.policy_summary.review_status,
           ad_group_ad.policy_summary.policy_topic_entries
    FROM ad_group_ad
    WHERE campaign.status = 'ENABLED'
    ORDER BY campaign.name, ad_group_ad.status
""")
cur = None
for r in rows:
    if r.campaign.name != cur:
        cur = r.campaign.name
        print(f"\n— {cur}  (id {r.campaign.id}, {r.campaign.advertising_channel_type.name})")
    a = r.ad_group_ad
    ps = a.policy_summary
    urls = ", ".join(a.ad.final_urls) or "(none)"
    flag = "" if ps.approval_status.name == "APPROVED" else "   <<< NOT APPROVED"
    print(f"  [{a.status.name:8}] ad {a.ad.id} {a.ad.type_.name}")
    print(f"      approval={ps.approval_status.name}  review={ps.review_status.name}{flag}")
    print(f"      url: {urls}")
    for t in ps.policy_topic_entries:
        print(f"      policy: {t.topic}  ({t.type_.name})")

print("\n=== ALL ads in 'Traffic ticket lawyer broad' ad group (incl. paused) — URL + status ===")
for r in ga.search(customer_id=cid, query="""
    SELECT ad_group.id, ad_group_ad.ad.id, ad_group_ad.status,
           ad_group_ad.ad.final_urls,
           ad_group_ad.policy_summary.approval_status
    FROM ad_group_ad
    WHERE campaign.id = 23039650759
    ORDER BY ad_group.id, ad_group_ad.status
"""):
    a = r.ad_group_ad
    print(f"  ag {r.ad_group.id} [{a.status.name:8}] ad {a.ad.id} "
          f"{a.policy_summary.approval_status.name}: {', '.join(a.ad.final_urls)}")

print("\n=== Keyword-level final URLs in broad ad group (these also count for one-website rule) ===")
any_kw = False
for r in ga.search(customer_id=cid, query="""
    SELECT ad_group_criterion.keyword.text, ad_group_criterion.final_urls
    FROM ad_group_criterion
    WHERE campaign.id = 23039650759
      AND ad_group_criterion.type = 'KEYWORD'
      AND ad_group_criterion.final_urls != ''
"""):
    any_kw = True
    print(f"  kw '{r.ad_group_criterion.keyword.text}': {list(r.ad_group_criterion.final_urls)}")
if not any_kw:
    print("  (no keyword-level final URLs)")
print()
