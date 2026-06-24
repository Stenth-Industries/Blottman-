"""2026-06-24: Inventory EVERY landing URL the account sends traffic to (ads + sitelinks +
keyword final URLs), across all ENABLED campaigns. Output = the distinct set of pages that
blottman.ca (landing-v2) would need to host for a full .com -> .ca migration. Read-only.
Run: python code/url_inventory.py"""
from dotenv import load_dotenv
import os, logging
from urllib.parse import urlparse
from collections import defaultdict
from google.ads.googleads.client import GoogleAdsClient
logging.getLogger("google.ads.googleads").setLevel(logging.WARNING)
load_dotenv()
cfg={k:os.getenv(v) for k,v in {"developer_token":"GOOGLE_ADS_DEVELOPER_TOKEN","client_id":"GOOGLE_ADS_CLIENT_ID","client_secret":"GOOGLE_ADS_CLIENT_SECRET","refresh_token":"GOOGLE_ADS_REFRESH_TOKEN","login_customer_id":"GOOGLE_ADS_LOGIN_CUSTOMER_ID"}.items()}
cfg["use_proto_plus"]=True
client=GoogleAdsClient.load_from_dict(cfg)
ga=client.get_service("GoogleAdsService")
cid=os.getenv("GOOGLE_ADS_CUSTOMER_ID")

def norm(u):
    p=urlparse(u)
    path=(p.path or "/").rstrip("/") or "/"
    return p.netloc.lower(), path

pages=defaultdict(lambda: {"sources":set(),"examples":set()})  # path -> info

# 1) Ad-level final URLs (enabled campaigns, enabled+paused ads)
for r in ga.search(customer_id=cid, query="""
  SELECT campaign.name, ad_group_ad.status, ad_group_ad.ad.final_urls
  FROM ad_group_ad WHERE campaign.status='ENABLED'"""):
    for u in r.ad_group_ad.ad.final_urls:
        host,path=norm(u)
        pages[path]["sources"].add("ad")
        pages[path]["examples"].add(f"{host}{path}")

# 2) Sitelink / asset final URLs on enabled campaigns
for r in ga.search(customer_id=cid, query="""
  SELECT campaign.name, campaign.status, asset.id, asset.type, asset.final_urls,
         asset.sitelink_asset.link_text, campaign_asset.status
  FROM campaign_asset WHERE campaign.status='ENABLED' AND campaign_asset.status!='REMOVED'"""):
    for u in r.asset.final_urls:
        host,path=norm(u)
        pages[path]["sources"].add(f"sitelink:{r.asset.sitelink_asset.link_text or r.asset.type_.name}")
        pages[path]["examples"].add(f"{host}{path}")

# 3) Keyword-level final URLs
for r in ga.search(customer_id=cid, query="""
  SELECT campaign.name, campaign.status, ad_group_criterion.keyword.text, ad_group_criterion.final_urls
  FROM ad_group_criterion WHERE campaign.status='ENABLED' AND ad_group_criterion.type='KEYWORD'"""):
    for u in r.ad_group_criterion.final_urls:
        host,path=norm(u)
        pages[path]["sources"].add("keyword")
        pages[path]["examples"].add(f"{host}{path}")

CA_HAS={"/","/speeding","/privacy"}
print(f"\n=== DISTINCT PAGES THE ACCOUNT SENDS TRAFFIC TO ({len(pages)}) ===\n")
for path in sorted(pages):
    info=pages[path]
    have="[ON .ca]" if path in CA_HAS else "[MISSING on .ca]"
    ex=sorted(info["examples"])[0]
    srcs=", ".join(sorted(info["sources"])[:4])
    print(f"  {have:18} {path}")
    print(f"       e.g. {ex}   [{srcs}]")
miss=[p for p in pages if p not in CA_HAS]
print(f"\n=== BLOTTMAN.CA NEEDS {len(miss)} NEW PAGE(S) for a full migration ===")
for p in sorted(miss): print(f"  blottman.ca{p}")
print(f"\n.ca already has: {', '.join(sorted(CA_HAS))}")
