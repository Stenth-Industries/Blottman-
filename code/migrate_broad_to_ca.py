"""2026-06-24: Make 'Traffic ticket lawyer broad' (23039650759, ad group 186398312300)
run cleanly on blottman.ca (the new landing page). Clears the ONE_WEBSITE_PER_AD_GROUP
disapproval by making the ENTIRE ad group single-domain (.ca).

User decision: scope = broad campaign only; remove the .com subpage sitelinks (the .ca
site / landing-v2 only has /, /speeding, /privacy — no matching subpages).

Actions:
  1. Repoint all 4 ads (2 enabled + 2 paused) -> https://blottman.ca/
  2. Remove the 10 .com sitelink links from the campaign
  3. Detach the shared lead form from broad (it points to blottman.com/ = last .com
     reference; broad gets ~0 form impr so zero cost). The lead-form ASSET is NOT edited
     (still serves on the 3 other .com Search campaigns).

Reversible (assets are only unlinked, not deleted). Run: python code/migrate_broad_to_ca.py"""
from dotenv import load_dotenv
import os, logging
from google.ads.googleads.client import GoogleAdsClient
logging.getLogger("google.ads.googleads").setLevel(logging.ERROR)
load_dotenv()
cfg={k:os.getenv(v) for k,v in {"developer_token":"GOOGLE_ADS_DEVELOPER_TOKEN","client_id":"GOOGLE_ADS_CLIENT_ID","client_secret":"GOOGLE_ADS_CLIENT_SECRET","refresh_token":"GOOGLE_ADS_REFRESH_TOKEN","login_customer_id":"GOOGLE_ADS_LOGIN_CUSTOMER_ID"}.items()}
cfg["use_proto_plus"]=True
client=GoogleAdsClient.load_from_dict(cfg)
cid=os.getenv("GOOGLE_ADS_CUSTOMER_ID")
CA="https://blottman.ca/"
ad_ids=["812451424746","812455198290","774748697421","812451172230"]
links=[
 "customers/8586214705/campaignAssets/23039650759~371903420556~LEAD_FORM",
 "customers/8586214705/campaignAssets/23039650759~322570766588~SITELINK",
 "customers/8586214705/campaignAssets/23039650759~322570766594~SITELINK",
 "customers/8586214705/campaignAssets/23039650759~322570766597~SITELINK",
 "customers/8586214705/campaignAssets/23039650759~322570766600~SITELINK",
 "customers/8586214705/campaignAssets/23039650759~371561327376~SITELINK",
 "customers/8586214705/campaignAssets/23039650759~371561327379~SITELINK",
 "customers/8586214705/campaignAssets/23039650759~371561327382~SITELINK",
 "customers/8586214705/campaignAssets/23039650759~371561327385~SITELINK",
 "customers/8586214705/campaignAssets/23039650759~371561327388~SITELINK",
 "customers/8586214705/campaignAssets/23039650759~371561327391~SITELINK",
]

# 1) ads -> .ca
ad_svc=client.get_service("AdService")
ops=[]
for aid in ad_ids:
    op=client.get_type("AdOperation")
    op.update.resource_name=f"customers/{cid}/ads/{aid}"
    op.update.final_urls.append(CA)
    op.update_mask.paths.append("final_urls")
    ops.append(op)
ad_svc.mutate_ads(customer_id=cid, operations=ops)
print(f"1) Repointed {len(ad_ids)} ads -> {CA}")
for aid in ad_ids: print(f"     ad {aid}")

# 2+3) unlink the 11 .com campaign assets (10 sitelinks + lead form) from broad
ca_svc=client.get_service("CampaignAssetService")
rm_ops=[]
for rn in links:
    op=client.get_type("CampaignAssetOperation")
    op.remove=rn
    rm_ops.append(op)
ca_svc.mutate_campaign_assets(customer_id=cid, operations=rm_ops)
print(f"\n2) Unlinked {len(links)} .com assets from broad (10 sitelinks + lead form)")
print("   (assets unlinked only, not deleted; lead form still serves on other campaigns)")

print("\nDone. Broad ad group is now 100% blottman.ca.")
print("ONE_WEBSITE_PER_AD_GROUP should clear on re-review (hrs -> ~1 business day).")
print("Verify: python code/approval_status.py")
