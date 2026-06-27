"""Expand the thin SKAG ad groups in the consolidated Search campaign
(23971101309). Adds curated PHRASE keywords per offence (from real search
intent), deduped against existing keywords so re-runs are safe. No 'paralegal'
in the new copy/keywords. Read existing -> add only new.
"""
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
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
ga = client.get_service("GoogleAdsService")
agc_svc = client.get_service("AdGroupCriterionService")
CID = 23971101309

# ad_group_id -> candidate PHRASE keywords (offence-specific, real search intent)
CANDIDATES = {
    193110648370: [  # No Licence
        "driving without a licence", "no licence ticket ontario",
        "driving with no licence charge", "fight no licence ticket"],
    196586978543: [  # Stunt Driving
        "stunt driving ticket", "stunt driving charge ontario",
        "stunt driving 50 over", "fight stunt driving charge"],
    196587002103: [  # Driving Under Suspension
        "driving while suspended ontario", "fight driving under suspension",
        "driving under suspension charge", "caught driving while suspended"],
    197764410413: [  # Fail to Stop
        "fail to stop ticket", "ran a stop sign ticket",
        "rolling stop ticket ontario", "fight fail to stop ticket"],
    197764412053: [  # No Insurance
        "driving without insurance ontario", "no insurance ticket ontario",
        "fight no insurance ticket", "driving uninsured ticket"],
    197907964077: [  # Speeding
        "speeding ticket ontario", "speeding ticket demerit points",
        "fight a speeding ticket ontario", "speeding over 50 ticket"],
    197907966677: [  # Careless Driving
        "careless driving ticket ontario", "careless driving charge",
        "careless driving demerit points", "fight careless driving charge"],
    198168134055: [  # Cell Phone
        "cell phone ticket ontario", "texting while driving ticket",
        "distracted driving charge ontario", "fight cell phone ticket"],
    198168137215: [  # Disobey Sign (most starved)
        "fail to obey sign ticket", "disobey stop sign ticket",
        "disobey traffic sign ontario", "fight disobey sign ticket",
        "disobeying a sign ticket"],
    206301755028: [  # General
        "dispute a traffic ticket ontario", "fight a traffic ticket",
        "traffic ticket help ontario", "contest traffic ticket ontario"],
}

# existing keyword texts per ad group (dedupe)
existing = {agid: set() for agid in CANDIDATES}
for r in ga.search(customer_id=cid, query=(
        f"SELECT ad_group.id, ad_group_criterion.keyword.text FROM ad_group_criterion "
        f"WHERE campaign.id={CID} AND ad_group_criterion.type=KEYWORD "
        f"AND ad_group_criterion.negative=false")):
    if r.ad_group.id in existing:
        existing[r.ad_group.id].add(r.ad_group_criterion.keyword.text.lower())

PHRASE = client.enums.KeywordMatchTypeEnum.PHRASE
ops = []
added = 0
for agid, kws in CANDIDATES.items():
    for kw in kws:
        if kw.lower() in existing[agid]:
            continue
        o = client.get_type("AdGroupCriterionOperation")
        c = o.create
        c.ad_group = f"customers/{cid}/adGroups/{agid}"
        c.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        c.keyword.text = kw
        c.keyword.match_type = PHRASE
        ops.append(o)
        added += 1

res = agc_svc.mutate_ad_group_criteria(customer_id=cid, operations=ops)
print(f"  added {len(res.results)} new PHRASE keywords across 10 ad groups (target ~7-8 each)")
