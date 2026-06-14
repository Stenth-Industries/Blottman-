"""2026-06-14: client reports blottman.com/traffic-tickets is BROKEN. Repoint all live ad
click-destinations from /traffic-tickets -> homepage (https://blottman.com/). Fixes the RSAs
(main click dest) and reports which /traffic-tickets sitelinks are attached to ENABLED campaigns."""
from dotenv import load_dotenv
import os, logging
from google.api_core import protobuf_helpers
from google.ads.googleads.client import GoogleAdsClient
logging.getLogger("google.ads.googleads").setLevel(logging.ERROR)
load_dotenv()
cfg={k:os.getenv(v) for k,v in {"developer_token":"GOOGLE_ADS_DEVELOPER_TOKEN","client_id":"GOOGLE_ADS_CLIENT_ID","client_secret":"GOOGLE_ADS_CLIENT_SECRET","refresh_token":"GOOGLE_ADS_REFRESH_TOKEN","login_customer_id":"GOOGLE_ADS_LOGIN_CUSTOMER_ID"}.items()}
cfg["use_proto_plus"]=True
client=GoogleAdsClient.load_from_dict(cfg)
ga=client.get_service("GoogleAdsService")
cid=os.getenv("GOOGLE_ADS_CUSTOMER_ID")
HOME="https://blottman.com/"

# --- 1) Fix RSAs whose final_urls contain /traffic-tickets ---
ad_ids=["812451424746","812455198290","812451172230"]
ad_svc=client.get_service("AdService")
ops=[]
for aid in ad_ids:
    op=client.get_type("AdOperation")
    ad=op.update
    ad.resource_name=f"customers/{cid}/ads/{aid}"
    ad.final_urls.append(HOME)
    op.update_mask.paths.append("final_urls")
    ops.append(op)
res=ad_svc.mutate_ads(customer_id=cid, operations=ops)
print(f"RSAs repointed to homepage ({len(res.results)}):")
for aid,r in zip(ad_ids,res.results): print(f"  ad {aid} -> {HOME}")

# --- 2) Which /traffic-tickets sitelinks are LIVE on enabled campaigns? ---
print("\nSitelinks pointing to /traffic-tickets that are attached to ENABLED campaigns:")
live=set()
for r in ga.search(customer_id=cid, query="""
    SELECT campaign.name, campaign.status, asset.id, asset.final_urls,
           asset.sitelink_asset.link_text, campaign_asset.status
    FROM campaign_asset
    WHERE campaign.status='ENABLED' AND asset.type='SITELINK'"""):
    urls=list(r.asset.final_urls)
    if any('/traffic-tickets' in u for u in urls):
        live.add(r.asset.id)
        print(f"  campaign '{r.campaign.name}' [{r.campaign_asset.status.name}] sitelink {r.asset.id} '{r.asset.sitelink_asset.link_text}' -> {urls}")
if not live: print("  (none live)")
