"""Build the consolidated SKAG Search campaign (PAUSED) per search-consolidation-plan.md.
One offence per ad group, each landing on its matching blottman.ca page. Phrase+exact only.
Creates: budget -> campaign (PAUSED, Search-only, Ontario PRESENCE, ManualCPC) -> ad groups
-> keywords -> 1 RSA each (offence pinned H1). Attaches both shared negative lists.
Idempotent guard: aborts if a campaign with the same name already exists.
Run: python code/build_consolidated_search.py
"""
from dotenv import load_dotenv
import os, logging, sys
from google.ads.googleads.client import GoogleAdsClient
logging.getLogger("google.ads.googleads").setLevel(logging.CRITICAL)
load_dotenv()
cfg = {k: os.getenv(v) for k, v in {
    "developer_token": "GOOGLE_ADS_DEVELOPER_TOKEN", "client_id": "GOOGLE_ADS_CLIENT_ID",
    "client_secret": "GOOGLE_ADS_CLIENT_SECRET", "refresh_token": "GOOGLE_ADS_REFRESH_TOKEN",
    "login_customer_id": "GOOGLE_ADS_LOGIN_CUSTOMER_ID"}.items()}
cfg["use_proto_plus"] = True
client = GoogleAdsClient.load_from_dict(cfg)
ga = client.get_service("GoogleAdsService")
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")

CAMPAIGN_NAME = "Search - Ontario Traffic Tickets (Consolidated)"
BUDGET_DAILY = 30_000_000          # $30/day
AG_CPC = 3_000_000                 # $3 default CPC
ONTARIO = "geoTargetConstants/20121"
ENGLISH = "languageConstants/1000"
NEG_SHARED_SETS = ["12109076551", "11960214627"]  # Master Negatives + neg list

SHARED_HEADLINES = [
    "Licensed Ontario Paralegal", "500+ Traffic Tickets Handled", "Free Case Review Today",
    "Protect Your Driving Record", "Avoid Costly Demerit Points", "Keep Your Insurance Low",
    "Most Clients Never Go To Court", "We Deal With The Court For You", "Serving All Of Ontario",
    "Affordable Flat-Fee Defence", "Skilled Ticket Defence Team", "Call For A Free Consultation",
    "Don't Just Pay The Fine", "Fast, Confidential Help",
]
DESCRIPTIONS = [
    "Licensed Ontario paralegal fighting traffic tickets to protect your record and insurance.",
    "We handle the paperwork and court so you don't have to. 500+ tickets handled in Ontario.",
    "Fight your ticket and the demerit points that raise your insurance for years. Talk free.",
    "Affordable flat-fee defence. Most clients never set foot in court. Free case review today.",
]
# (ad group name, landing url, pinned offence H1, [(kw, match)])
P, E = "PHRASE", "EXACT"
AD_GROUPS = [
    ("Speeding", "https://blottman.ca/speeding", "Fight Your Speeding Ticket",
     [("fight speeding ticket", P), ("speeding ticket help", P), ("fight my speeding ticket", P),
      ("speeding ticket paralegal ontario", E)]),
    ("Careless Driving", "https://blottman.ca/careless-driving", "Fight a Careless Charge",
     [("fight careless driving ticket", P), ("careless driving ticket help", P),
      ("careless driving paralegal", E)]),
    ("Stunt Driving", "https://blottman.ca/stunt-driving", "Fight a Stunt Driving Charge",
     [("fight stunt driving ticket", P), ("stunt driving ticket help", P),
      ("stunt driving paralegal ontario", E)]),
    ("Cell Phone", "https://blottman.ca/cell-phone", "Fight a Cell Phone Ticket",
     [("cell phone ticket", P), ("distracted driving ticket", P), ("driving while on phone ticket", P),
      ("phone in hand ticket", P), ("fight distracted driving ticket", P)]),
    ("Fail to Stop", "https://blottman.ca/fail-to-stop", "Fight a Stop Sign Ticket",
     [("fail to stop at stop sign ticket", P), ("stop sign ticket ontario", P),
      ("failure to stop ticket", P), ("fight a stop sign ticket", P)]),
    ("Disobey Sign", "https://blottman.ca/disobey-sign", "Fight a Disobey Sign Ticket",
     [("disobey sign ticket", P), ("disobey sign ticket ontario", E)]),
    ("No Insurance", "https://blottman.ca/no-insurance", "Fight a No-Insurance Ticket",
     [("no insurance ticket", P), ("without insurance ticket", P),
      ("fighting no insurance ticket ontario", P)]),
    ("Driving Under Suspension", "https://blottman.ca/driving-under-suspension", "Driving Suspension Defence",
     [("suspended license ticket ontario", P), ("driving under suspension ticket", P),
      ("drive while suspended ticket", P)]),
    ("No Licence", "https://blottman.ca/no-licence", "Fight a No-Licence Ticket",
     [("no licence ticket", P), ("driving with no licence ticket", P), ("fail to surrender licence", P)]),
    ("General - Fight Ticket", "https://blottman.ca/", "Fight Your Traffic Ticket",
     [("how to fight a traffic ticket", P), ("traffic ticket paralegal", P),
      ("fight traffic ticket ontario", P), ("traffic ticket defence ontario", P),
      ("ontario traffic ticket dispute", P), ("traffic ticket legal help", P)]),
]

# --- length guard (Google: headline<=30, description<=90) ---
bad = [h for h in SHARED_HEADLINES if len(h) > 30] + \
      [ag[2] for ag in AD_GROUPS if len(ag[2]) > 30] + \
      [d for d in DESCRIPTIONS if len(d) > 90]
if bad:
    print("ABORT - over-length copy:", bad); sys.exit(1)

# --- idempotent guard ---
for r in ga.search(customer_id=cid, query=f"""SELECT campaign.id FROM campaign
    WHERE campaign.name = '{CAMPAIGN_NAME}'"""):
    print(f"ABORT - campaign '{CAMPAIGN_NAME}' already exists (id {r.campaign.id}). Nothing created.")
    sys.exit(1)

def svc(n): return client.get_service(n)
def op(n): return client.get_type(n)

# 1) BUDGET (reuse if one with this name already exists, e.g. from a failed run)
BUD_NAME = CAMPAIGN_NAME + " Budget"
bud_res = None
for r in ga.search(customer_id=cid, query=f"""SELECT campaign_budget.resource_name
    FROM campaign_budget WHERE campaign_budget.name = '{BUD_NAME}'"""):
    bud_res = r.campaign_budget.resource_name; break
if bud_res:
    print("budget: reusing existing", bud_res)
else:
    bud_op = op("CampaignBudgetOperation")
    b = bud_op.create
    b.name = BUD_NAME
    b.amount_micros = BUDGET_DAILY
    b.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
    b.explicitly_shared = False
    bud_res = svc("CampaignBudgetService").mutate_campaign_budgets(
        customer_id=cid, operations=[bud_op]).results[0].resource_name
    print("budget:", bud_res)

# 2) CAMPAIGN (PAUSED, Search-only, ManualCPC)
c_op = op("CampaignOperation")
c = c_op.create
c.name = CAMPAIGN_NAME
c.status = client.enums.CampaignStatusEnum.PAUSED
c.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SEARCH
c.campaign_budget = bud_res
c.contains_eu_political_advertising = \
    client.enums.EuPoliticalAdvertisingStatusEnum.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
c.manual_cpc.enhanced_cpc_enabled = False
c.network_settings.target_google_search = True
c.network_settings.target_search_network = False
c.network_settings.target_content_network = False
c.network_settings.target_partner_search_network = False
c.geo_target_type_setting.positive_geo_target_type = \
    client.enums.PositiveGeoTargetTypeEnum.PRESENCE
camp_res = svc("CampaignService").mutate_campaigns(
    customer_id=cid, operations=[c_op]).results[0].resource_name
print("campaign:", camp_res)

# 3) CAMPAIGN CRITERIA: geo + language
crit_ops = []
geo_op = op("CampaignCriterionOperation"); geo_op.create.campaign = camp_res
geo_op.create.location.geo_target_constant = ONTARIO; crit_ops.append(geo_op)
lang_op = op("CampaignCriterionOperation"); lang_op.create.campaign = camp_res
lang_op.create.language.language_constant = ENGLISH; crit_ops.append(lang_op)
svc("CampaignCriterionService").mutate_campaign_criteria(customer_id=cid, operations=crit_ops)
print("geo=Ontario PRESENCE + language=English set")

# 4) negative shared lists
try:
    css_ops = []
    for sid in NEG_SHARED_SETS:
        o = op("CampaignSharedSetOperation")
        o.create.campaign = camp_res
        o.create.shared_set = f"customers/{cid}/sharedSets/{sid}"
        css_ops.append(o)
    svc("CampaignSharedSetService").mutate_campaign_shared_sets(customer_id=cid, operations=css_ops)
    print("attached negative lists:", NEG_SHARED_SETS)
except Exception as ex:
    print("WARN could not attach shared negatives (attach in UI):", str(ex)[:120])

# 5) AD GROUPS + keywords + RSA
ags = svc("AdGroupService"); agc = svc("AdGroupCriterionService"); aga = svc("AdGroupAdService")
for name, url, pinned_h1, kws in AD_GROUPS:
    ag_op = op("AdGroupOperation"); a = ag_op.create
    a.name = name; a.campaign = camp_res
    a.status = client.enums.AdGroupStatusEnum.ENABLED
    a.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
    a.cpc_bid_micros = AG_CPC
    ag_res = ags.mutate_ad_groups(customer_id=cid, operations=[ag_op]).results[0].resource_name
    # keywords
    kw_ops = []
    for txt, mt in kws:
        ko = op("AdGroupCriterionOperation"); k = ko.create
        k.ad_group = ag_res
        k.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        k.keyword.text = txt
        k.keyword.match_type = getattr(client.enums.KeywordMatchTypeEnum, mt)
        kw_ops.append(ko)
    agc.mutate_ad_group_criteria(customer_id=cid, operations=kw_ops)
    # RSA
    ad_op = op("AdGroupAdOperation"); ada = ad_op.create
    ada.ad_group = ag_res
    ada.status = client.enums.AdGroupAdStatusEnum.ENABLED
    ada.ad.final_urls.append(url)
    rsa = ada.ad.responsive_search_ad
    h1 = op("AdTextAsset"); h1.text = pinned_h1
    h1.pinned_field = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1
    rsa.headlines.append(h1)
    for h in SHARED_HEADLINES:
        ta = op("AdTextAsset"); ta.text = h; rsa.headlines.append(ta)
    for d in DESCRIPTIONS:
        da = op("AdTextAsset"); da.text = d; rsa.descriptions.append(da)
    aga.mutate_ad_group_ads(customer_id=cid, operations=[ad_op])
    print(f"  ad group OK: {name:26} -> {url}  ({len(kws)} kw, RSA)")

print("\nDONE. Campaign created PAUSED. Verify, then enable.")
print("CAMPAIGN_RES:", camp_res)
