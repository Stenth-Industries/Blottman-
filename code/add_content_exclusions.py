"""2026-06-24: Account-level content-label exclusions (Lever-2b) to trim PMAX's cheap
Display/Discover/YouTube junk reach. ACCOUNT-WIDE — applies to all enabled campaigns'
Display serving; does NOT touch Search/Maps/calls. Reversible (remove the same
customer_negative_criterion rows). Run: python code/add_content_exclusions.py"""
from dotenv import load_dotenv
import os, logging
from google.ads.googleads.client import GoogleAdsClient
logging.getLogger("google.ads.googleads").setLevel(logging.ERROR)
load_dotenv()
cfg={k:os.getenv(v) for k,v in {"developer_token":"GOOGLE_ADS_DEVELOPER_TOKEN","client_id":"GOOGLE_ADS_CLIENT_ID","client_secret":"GOOGLE_ADS_CLIENT_SECRET","refresh_token":"GOOGLE_ADS_REFRESH_TOKEN","login_customer_id":"GOOGLE_ADS_LOGIN_CUSTOMER_ID"}.items()}
cfg["use_proto_plus"]=True
client=GoogleAdsClient.load_from_dict(cfg)
cid=os.getenv("GOOGLE_ADS_CUSTOMER_ID")
ga=client.get_service("GoogleAdsService")
svc=client.get_service("CustomerNegativeCriterionService")

# already-present (skip): PARKED_DOMAIN, SEXUALLY_SUGGESTIVE, PROFANITY, LIVE_STREAMING_VIDEO
ADD = ["BELOW_THE_FOLD","BRAND_SUITABILITY_GAMES_FIGHTING","BRAND_SUITABILITY_GAMES_MATURE",
       "VIDEO_RATING_DV_MA","TRAGEDY","SOCIAL_ISSUES","EMBEDDED_VIDEO","JUVENILE"]

existing={r.customer_negative_criterion.content_label.type_.name for r in ga.search(customer_id=cid, query="""
  SELECT customer_negative_criterion.content_label.type FROM customer_negative_criterion
  WHERE customer_negative_criterion.type='CONTENT_LABEL'""")}
todo=[x for x in ADD if x not in existing]
print(f"Already excluded: {sorted(existing)}")
print(f"Adding: {todo}\n")

ops=[]
for label in todo:
    op=client.get_type("CustomerNegativeCriterionOperation")
    op.create.content_label.type_=client.enums.ContentLabelTypeEnum[label]
    ops.append(op)
if ops:
    res=svc.mutate_customer_negative_criteria(customer_id=cid, operations=ops)
    print(f"Added {len(res.results)} account-level content-label exclusions:")
    for label in todo: print(f"  + {label}")
else:
    print("Nothing to add (all present).")
print("\nAccount-wide; affects Display/Video/Discover only. Search & calls untouched.")
