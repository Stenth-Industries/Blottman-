"""Fix the AI Max junk-conversion doom loop (Jul-17 diagnosis, Leslie's
"calls for courthouse" complaint). Three changes:

  1. Search Consolidated (23971101309): AI Max OFF + Maximize Conversions ->
     Maximize Clicks (TARGET_SPEND, $8 cpc ceiling = its pre-Jul-6 state).
     Evidence: AI_MAX match type = $194 of $284 14d spend; produced ALL 18
     conversions; every converting term is a government pay-portal/lookup
     query converting at 50-100% (real intent converts at 5-15%) = misdirected
     citizens filling the in-ad lead form thinking it's the ticket office,
     then emailed to Leslie hourly by the Jul-12 Ad Lead Forwarder.
     Max Conversions must switch simultaneously: with AI Max off there are
     0 biddable conversions left (all other match types = 0 conv in 14d),
     which re-creates the Jul-11 "missing primary conversion action" break.

  2. Shared Master Negatives (12109076551): add the fused pay-portal tokens
     the existing negatives can't token-match (same lesson as excopper /
     parkingticketdispute). NOT blocking bare 'g1' - "driving with no
     experience" (unaccompanied G1) is a practice area; block test-prep only.

  3. BMX (22979153470): tCPA $51 -> $60. Kushagra's own Jul-6 contingency
     ("if spend collapses raise tCPA to ~$60-65") triggered: 7d actual spend
     $45.71/day vs $65 budget - tCPA is the binding constraint, not budget.

REVERT VALUES:
  - Search: ai_max_setting.enable_ai_max=True; bidding=MAXIMIZE_CONVERSIONS
    (no tCPA); cpc ceiling at flip time printed by this script.
  - BMX: maximize_conversions.target_cpa_micros = 51_000_000
  - Negatives: delete from shared set in UI.
"""
from dotenv import load_dotenv
import os, logging
from google.ads.googleads.client import GoogleAdsClient
logging.getLogger("google.ads.googleads").setLevel(logging.WARNING)
load_dotenv()
cfg = {
    "developer_token": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
    "client_id": os.getenv("GOOGLE_ADS_CLIENT_ID"),
    "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
    "refresh_token": os.getenv("GOOGLE_ADS_REFRESH_TOKEN"),
    "login_customer_id": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),
    "use_proto_plus": True,
}
client = GoogleAdsClient.load_from_dict(cfg)
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
ga = client.get_service("GoogleAdsService")
csvc = client.get_service("CampaignService")

SEARCH = "23971101309"
BMX = "22979153470"
SHARED_SET = f"customers/{cid}/sharedSets/12109076551"

# ------------------------------------------------ 0. print current state
print("--- current state (for the log / revert) ---")
for r in ga.search(customer_id=cid, query=f"""
  SELECT campaign.id, campaign.name, campaign.bidding_strategy_type,
         campaign.ai_max_setting.enable_ai_max,
         campaign.maximize_conversions.target_cpa_micros,
         campaign.target_spend.cpc_bid_ceiling_micros
  FROM campaign WHERE campaign.id IN ({SEARCH}, {BMX})"""):
    c = r.campaign
    print(f"  {c.name}: {c.bidding_strategy_type.name}, ai_max={c.ai_max_setting.enable_ai_max}, "
          f"tCPA=${c.maximize_conversions.target_cpa_micros/1e6:.2f}, "
          f"cpc_ceiling=${c.target_spend.cpc_bid_ceiling_micros/1e6:.2f}")

# ------------------------------------------------ 1. Search: Max Clicks first
# API GOTCHA (learned Jul-17): mutating ai_max_setting.enable_ai_max ALONE is
# rejected with the misleading fault "This feature is only available for
# campaigns with AI Max enabled". The disable only succeeds when sent in ONE
# operation together with both asset_automation_settings OPTED_OUT (mirrors
# what the UI toggle does). AssetAutomationSetting is a NESTED type on
# Campaign, not a standalone get_type() name.
print("\n--- 1a. Search Consolidated: Maximize Clicks ($8 ceiling) ---")
op = client.get_type("CampaignOperation")
camp = op.update
camp.resource_name = csvc.campaign_path(cid, SEARCH)
camp.target_spend.cpc_bid_ceiling_micros = 8_000_000
op.update_mask.paths.append("target_spend.cpc_bid_ceiling_micros")
try:
    res = csvc.mutate_campaigns(customer_id=cid, operations=[op])
    print(f"  OK: {res.results[0].resource_name}")
except Exception as e:
    print(f"  FAILED: {str(e)[:300]}")

print("\n--- 1b. Search Consolidated: AI Max OFF (+ asset automations opted out) ---")
CampaignT = client.get_type("Campaign")
op = client.get_type("CampaignOperation")
camp = op.update
camp.resource_name = csvc.campaign_path(cid, SEARCH)
camp.ai_max_setting.enable_ai_max = False
for t in ["TEXT_ASSET_AUTOMATION", "FINAL_URL_EXPANSION_TEXT_ASSET_AUTOMATION"]:
    s = type(CampaignT).AssetAutomationSetting()
    s.asset_automation_type = client.enums.AssetAutomationTypeEnum[t]
    s.asset_automation_status = client.enums.AssetAutomationStatusEnum.OPTED_OUT
    camp.asset_automation_settings.append(s)
op.update_mask.paths.extend(["ai_max_setting.enable_ai_max", "asset_automation_settings"])
try:
    res = csvc.mutate_campaigns(customer_id=cid, operations=[op])
    print(f"  OK: {res.results[0].resource_name}")
except Exception as e:
    print(f"  FAILED: {str(e)[:300]}")

# ------------------------------------------------ 2. fused pay-portal negatives
print("\n--- 2. fused pay-portal negatives -> Master Negatives ---")
NEW_NEGS = [
    ("paytickets", "BROAD"),        # www paytickets ca (3 junk conv, $27.33)
    ("ticketsandfines", "BROAD"),   # www ontario ticketsandfines
    ("cityofkingston", "BROAD"),    # www cityofkingston ca pay
    ("g1 test", "PHRASE"),          # test-prep only; bare g1 stays biddable
    ("g1 practice test", "PHRASE"),
]
rows = ga.search(customer_id=cid, query=f"""
    SELECT shared_criterion.keyword.text FROM shared_criterion
    WHERE shared_criterion.shared_set = '{SHARED_SET}'
      AND shared_criterion.type = 'KEYWORD'""")
existing = {r.shared_criterion.keyword.text.lower() for r in rows}
to_add = [(t, mt) for t, mt in NEW_NEGS if t.lower() not in existing]
for t, mt in NEW_NEGS:
    if t.lower() in existing:
        print(f"  skip (already present): {t}")
if to_add:
    svc = client.get_service("SharedCriterionService")
    ops = []
    for text, mt in to_add:
        o = client.get_type("SharedCriterionOperation")
        sc = o.create
        sc.shared_set = SHARED_SET
        sc.keyword.text = text
        sc.keyword.match_type = client.enums.KeywordMatchTypeEnum[mt]
        ops.append(o)
    res = svc.mutate_shared_criteria(customer_id=cid, operations=ops)
    for (text, mt), r in zip(to_add, res.results):
        print(f"  added [{mt[:3]}] {text}")

# ------------------------------------------------ 3. BMX tCPA 51 -> 60
print("\n--- 3. BMX tCPA $51 -> $60 ---")
op = client.get_type("CampaignOperation")
camp = op.update
camp.resource_name = csvc.campaign_path(cid, BMX)
camp.maximize_conversions.target_cpa_micros = 60_000_000
op.update_mask.paths.append("maximize_conversions.target_cpa_micros")
try:
    res = csvc.mutate_campaigns(customer_id=cid, operations=[op])
    print(f"  OK: {res.results[0].resource_name}")
except Exception as e:
    print(f"  FAILED: {str(e)[:300]}")

# ------------------------------------------------ verify
print("\n--- verify final state ---")
for r in ga.search(customer_id=cid, query=f"""
  SELECT campaign.id, campaign.name, campaign.bidding_strategy_type,
         campaign.ai_max_setting.enable_ai_max,
         campaign.maximize_conversions.target_cpa_micros,
         campaign.target_spend.cpc_bid_ceiling_micros
  FROM campaign WHERE campaign.id IN ({SEARCH}, {BMX})"""):
    c = r.campaign
    print(f"  {c.name}: {c.bidding_strategy_type.name}, ai_max={c.ai_max_setting.enable_ai_max}, "
          f"tCPA=${c.maximize_conversions.target_cpa_micros/1e6:.2f}, "
          f"cpc_ceiling=${c.target_spend.cpc_bid_ceiling_micros/1e6:.2f}")
