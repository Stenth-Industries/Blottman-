"""2026-06-14: PMAX - Blottman Max (BMX, 22979153470) had NO geo targeting (served anywhere) ->
likely source of client's 'irrelevant / out-of-area calls'. Set geo = Ontario (she's an Ontario
paralegal, serves all ON) + PRESENCE-only (people physically in ON, not merely 'interested').
Idempotent-ish: prints current state, finds Ontario geo constant, adds it, sets PRESENCE."""
from dotenv import load_dotenv
import os, logging
from google.ads.googleads.client import GoogleAdsClient
logging.getLogger("google.ads.googleads").setLevel(logging.ERROR)
load_dotenv()
cfg={k:os.getenv(v) for k,v in {"developer_token":"GOOGLE_ADS_DEVELOPER_TOKEN","client_id":"GOOGLE_ADS_CLIENT_ID","client_secret":"GOOGLE_ADS_CLIENT_SECRET","refresh_token":"GOOGLE_ADS_REFRESH_TOKEN","login_customer_id":"GOOGLE_ADS_LOGIN_CUSTOMER_ID"}.items()}
cfg["use_proto_plus"]=True
client=GoogleAdsClient.load_from_dict(cfg)
ga=client.get_service("GoogleAdsService")
cid=os.getenv("GOOGLE_ADS_CUSTOMER_ID")
BMX="22979153470"

# 1) find Ontario, Canada (Province)
ont=None
for r in ga.search(customer_id=cid, query="""
    SELECT geo_target_constant.resource_name, geo_target_constant.canonical_name,
           geo_target_constant.target_type, geo_target_constant.country_code
    FROM geo_target_constant
    WHERE geo_target_constant.canonical_name = 'Ontario,Canada'"""):
    ont=r.geo_target_constant.resource_name
    print(f"Ontario geo constant: {ont}  ({r.geo_target_constant.canonical_name}, {r.geo_target_constant.target_type})")
assert ont, "Ontario geo constant not found"

# 2) current geo on BMX
existing=[r.campaign_criterion.location.geo_target_constant for r in ga.search(customer_id=cid, query=f"""
    SELECT campaign_criterion.location.geo_target_constant FROM campaign_criterion
    WHERE campaign.id={BMX} AND campaign_criterion.type='LOCATION' AND campaign_criterion.negative=FALSE""")]
print(f"BMX current positive geo targets: {existing or '(none)'}")

# 3) add Ontario if not present
if ont not in existing:
    cc_svc=client.get_service("CampaignCriterionService")
    op=client.get_type("CampaignCriterionOperation")
    c=op.create
    c.campaign=f"customers/{cid}/campaigns/{BMX}"
    c.location.geo_target_constant=ont
    c.negative=False
    res=cc_svc.mutate_campaign_criteria(customer_id=cid, operations=[op])
    print(f"Added geo target: Ontario -> {res.results[0].resource_name}")
else:
    print("Ontario already targeted; skipping add.")

# 4) set PRESENCE-only geo mode
camp_svc=client.get_service("CampaignService")
op=client.get_type("CampaignOperation")
camp=op.update
camp.resource_name=f"customers/{cid}/campaigns/{BMX}"
camp.geo_target_type_setting.positive_geo_target_type=client.enums.PositiveGeoTargetTypeEnum.PRESENCE
op.update_mask.paths.append("geo_target_type_setting.positive_geo_target_type")
res=camp_svc.mutate_campaigns(customer_id=cid, operations=[op])
print(f"Set positive geo mode = PRESENCE on BMX ({res.results[0].resource_name})")
