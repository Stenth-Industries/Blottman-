"""Fix 'targeted goal is missing a primary conversion action' on
Search - Ontario Traffic Tickets (Consolidated) (23971101309) + make its
REAL signals biddable. Two mutations:

1. Campaign-specific conversion goals on 23971101309 ONLY (BMX untouched):
     biddable TRUE : SUBMIT_LEAD_FORM/WEBSITE (.ca QuickForm - Submit Lead Form - STENTH),
                     SUBMIT_LEAD_FORM/GOOGLE_HOSTED (in-ad lead form),
                     PHONE_CALL_LEAD/WEBSITE, PHONE_CALL_LEAD/CALL_FROM_ADS
     biddable FALSE: DOWNLOAD/APP, CONVERTED_LEAD/CALL_FROM_ADS, CONTACT/CALL_FROM_ADS
2. Re-promote 'Lead form - Submit' (7645568580) primary_for_goal -> True
   (it's the only action in the targeted GOOGLE_HOSTED lead-form goal,
   hence the UI warning).
   !! FAILS via API: MUTATE_NOT_ALLOWED - Google-hosted lead-form actions are
   system-managed, primary/secondary can only be flipped in the UI
   (Goals > Conversions > Summary > Lead form - Submit > Edit settings).
   demote_leadform_secondary.py therefore never worked either; the original
   demotion was a UI change.

GOTCHA (2026-07-11): mutate_campaign_conversion_goals rejects a BATCH of
operations atomically with MUTATE_NOT_ALLOWED, but the SAME operations
succeed when sent one per request - so this script sends them individually.

REVERT: campaign goals before this run (all others were already non-biddable):
  biddable TRUE was: DOWNLOAD/APP, PHONE_CALL_LEAD/WEBSITE, PHONE_CALL_LEAD/CALL_FROM_ADS,
                     SUBMIT_LEAD_FORM/GOOGLE_HOSTED, CONTACT/CALL_FROM_ADS,
                     CONVERTED_LEAD/CALL_FROM_ADS
  SUBMIT_LEAD_FORM/WEBSITE was biddable FALSE.
  7645568580 primary_for_goal was False."""
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

CAMPAIGN = "23971101309"
LEAD_FORM_ACTION = "7645568580"  # Lead form - Submit (GOOGLE_HOSTED in-ad form)

# (category, origin) -> desired biddable
DESIRED = {
    ("SUBMIT_LEAD_FORM", "WEBSITE"): True,        # Submit Lead Form - STENTH (.ca form)
    ("SUBMIT_LEAD_FORM", "GOOGLE_HOSTED"): True,  # in-ad lead form
    ("PHONE_CALL_LEAD", "WEBSITE"): True,
    ("PHONE_CALL_LEAD", "CALL_FROM_ADS"): True,
    ("DOWNLOAD", "APP"): False,                   # no app; empty goal
    ("CONVERTED_LEAD", "CALL_FROM_ADS"): False,   # no actions in it
    ("CONTACT", "CALL_FROM_ADS"): False,          # Smart Campaign leftover
}

# --- 1. campaign-specific goals (one mutate per request; batches get rejected) ---
rows = list(ga.search(customer_id=cid, query=f"""
    SELECT campaign_conversion_goal.resource_name,
           campaign_conversion_goal.category,
           campaign_conversion_goal.origin,
           campaign_conversion_goal.biddable
    FROM campaign_conversion_goal
    WHERE campaign.id = {CAMPAIGN}"""))

svc = client.get_service("CampaignConversionGoalService")
changed = 0
for r in rows:
    g = r.campaign_conversion_goal
    key = (g.category.name, g.origin.name)
    if key in DESIRED and g.biddable != DESIRED[key]:
        op = client.get_type("CampaignConversionGoalOperation")
        op.update.resource_name = g.resource_name
        op.update.biddable = DESIRED[key]
        op.update_mask.paths.append("biddable")
        svc.mutate_campaign_conversion_goals(customer_id=cid, operations=[op])
        changed += 1
        print(f"  goal {key[0]}/{key[1]}: biddable {g.biddable} -> {DESIRED[key]}")

print(f"  -> {changed} campaign goal(s) updated on {CAMPAIGN}" if changed
      else "  campaign goals already in desired state")

# --- 2. in-ad lead form action: API-immutable, UI only (see docstring) ---
print(f"  REMINDER: flip 'Lead form - Submit' ({LEAD_FORM_ACTION}) to Primary in the UI"
      "\n            Goals > Conversions > Summary > Lead form - Submit > Edit settings")

# --- verify ---
print("\n  VERIFY - biddable campaign goals on Search now:")
for r in ga.search(customer_id=cid, query=f"""
    SELECT campaign_conversion_goal.category, campaign_conversion_goal.origin,
           campaign_conversion_goal.biddable
    FROM campaign_conversion_goal WHERE campaign.id = {CAMPAIGN}"""):
    g = r.campaign_conversion_goal
    if g.biddable:
        print(f"    BIDDABLE  {g.category.name:<20} {g.origin.name}")

print("\n  VERIFY - BMX campaign goals unchanged (biddable set):")
for r in ga.search(customer_id=cid, query="""
    SELECT campaign_conversion_goal.category, campaign_conversion_goal.origin,
           campaign_conversion_goal.biddable
    FROM campaign_conversion_goal WHERE campaign.id = 22979153470"""):
    g = r.campaign_conversion_goal
    if g.biddable:
        print(f"    BIDDABLE  {g.category.name:<20} {g.origin.name}")
