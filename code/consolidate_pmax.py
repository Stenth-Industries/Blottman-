"""2026-06-14: Consolidate PMAX. Pause redundant pM #2 (23753177178) + pM #3 (23757095274)
(near-duplicate of winner BMX, mis-geo'd to Sarnia+Windsor, generating legal-aid/immigration
junk reach = client's 'irrelevant calls'). Raise BMX (22979153470) budget $50->$60 (+20%, safe
step) for headroom to absorb volume as it recovers. User-approved 'Consolidate' option."""
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

# 1) pause #2 and #3
camp_svc=client.get_service("CampaignService")
ops=[]
for cmp in ["23753177178","23757095274"]:
    op=client.get_type("CampaignOperation")
    op.update.resource_name=f"customers/{cid}/campaigns/{cmp}"
    op.update.status=client.enums.CampaignStatusEnum.PAUSED
    op.update_mask.paths.append("status")
    ops.append(op)
res=camp_svc.mutate_campaigns(customer_id=cid, operations=ops)
print(f"Paused {len(res.results)} campaigns: pM #2, pM #3")

# 2) raise BMX budget 50 -> 60
brow=list(ga.search(customer_id=cid, query=f"""
    SELECT campaign_budget.resource_name, campaign_budget.amount_micros, campaign_budget.name
    FROM campaign WHERE campaign.id={BMX}"""))[0]
bres=brow.campaign_budget.resource_name
print(f"BMX budget '{brow.campaign_budget.name}' currently ${brow.campaign_budget.amount_micros/1e6:.2f}/day")
bud_svc=client.get_service("CampaignBudgetService")
bop=client.get_type("CampaignBudgetOperation")
bop.update.resource_name=bres
bop.update.amount_micros=60_000_000
bop.update_mask.paths.append("amount_micros")
bres2=bud_svc.mutate_campaign_budgets(customer_id=cid, operations=[bop])
print(f"BMX budget raised -> $60.00/day ({bres2.results[0].resource_name})")

# 3) summary of enabled budgets now
print("\nEnabled campaign budgets now:")
tot=0
for r in ga.search(customer_id=cid, query="""
    SELECT campaign.name, campaign.advertising_channel_type, campaign_budget.amount_micros
    FROM campaign WHERE campaign.status='ENABLED' ORDER BY campaign_budget.amount_micros DESC"""):
    amt=r.campaign_budget.amount_micros/1e6; tot+=amt
    print(f"  ${amt:6.2f}  {r.campaign.advertising_channel_type.name:14} {r.campaign.name}")
print(f"  -------\n  ${tot:6.2f}/day total (~${tot*30.4:,.0f}/mo)")
