"""Finish the .ca migration: drop the 8 account-level blottman.com sitelinks.

WHY: today's BMX migration only moved the 2 CAMPAIGN-level sitelinks. Account-level
sitelinks serve on any campaign that has room for them, so 8 blottman.com links were
still eligible to show on BMX (and on Search). That leaves the migration half-done:
clicks on those sitelinks still land on the old site, which is the exact thing the
migration was meant to stop. Step 3 of the Aug-11 REMINDER.md checklist.

Two of them are independently worth killing:
  - 283883603301 "Contact Us" carries description "98% Win Rate, Traffic Law Experts",
    the Jun-17 clickbait claim. Unlinking it from BMX at campaign level earlier today
    did NOT stop it serving, because this account-level link kept it eligible.
  - 288982271386 "Traffic Ticket Defence" points at blottman.com/traffic-tickets/,
    the page the client reported BROKEN on Jun-14.

TOP-UP: removing 8 account-level sitelinks would leave BMX with only the 2 campaign-level
ones created today. Google needs 2 to serve them at all and shows more when available, so
this also links 2 already-approved .ca sitelinks (live on Search Consolidated for ~6
weeks) to BMX, keeping it at 4. This is compensating for the removal, not a new bet.

NOTE on the Jun-24 "multi-page hold": Search Consolidated has served .ca per-offence
sitelinks since Jun-27, so that directive was already superseded in practice. Reusing the
same assets on BMX is consistent with how the account already runs.

REVERT: re-link the 8 asset ids in REMOVE_ACCOUNT_SITELINKS as customer_assets with
field_type SITELINK; unlink TOPUP_FOR_BMX from campaign 22979153470.

USAGE:  python code/fix_account_sitelinks.py            (dry run)
        python code/fix_account_sitelinks.py --apply
"""
import os
import sys
import logging

from dotenv import load_dotenv
from google.ads.googleads.client import GoogleAdsClient

logging.getLogger("google.ads.googleads").setLevel(logging.CRITICAL)
load_dotenv()

APPLY = "--apply" in sys.argv
BMX = "22979153470"

REMOVE_ACCOUNT_SITELINKS = {
    "100824706793": "Read our Google Reviews  -> blottman.com/#reviews",
    "108661741540": "Get Free Consultation    -> blottman.com/#consultwhat",
    "283879806624": "Fight Your Car Tickets   -> blottman.com/",
    "283883603301": "Contact Us               -> blottman.com/contact-us/  [98% WIN RATE CLAIM]",
    "288982271380": "Stunt Driving Charge     -> blottman.com/stunt-driving-ticket/",
    "288982271383": "Drive Under Suspension   -> blottman.com/careless-driving-ticket/ (mismatched)",
    "288982271386": "Traffic Ticket Defence   -> blottman.com/traffic-tickets/  [BROKEN PAGE]",
    "288982271392": "Traffic Violations Law   -> blottman.com/traffic-violations/",
}

# Already-approved .ca sitelinks, live on Search Consolidated since late June.
TOPUP_FOR_BMX = {
    "380225943852": "Speeding Tickets  -> blottman.ca/speeding",
    "380225943855": "Careless Driving  -> blottman.ca/careless-driving",
}

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
cust_service = client.get_service("CustomerAssetService")
camp_service = client.get_service("CampaignAssetService")
asset_service = client.get_service("AssetService")
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")


def remaining_com():
    hits = []
    for r in ga.search(customer_id=cid, query="""
        SELECT asset.id, asset.sitelink_asset.link_text, asset.final_urls, customer_asset.status
        FROM customer_asset
        WHERE customer_asset.field_type = 'SITELINK' AND customer_asset.status = 'ENABLED'"""):
        if any("blottman.com" in u for u in r.asset.final_urls):
            hits.append((r.asset.id, r.asset.sitelink_asset.link_text))
    for r in ga.search(customer_id=cid, query="""
        SELECT campaign.id, campaign.name, campaign.status, asset.id,
               asset.sitelink_asset.link_text, asset.final_urls, campaign_asset.status
        FROM campaign_asset
        WHERE campaign.status = 'ENABLED' AND campaign_asset.status = 'ENABLED'
          AND campaign_asset.field_type = 'SITELINK'"""):
        if any("blottman.com" in u for u in r.asset.final_urls):
            hits.append((r.asset.id, f"{r.asset.sitelink_asset.link_text} [{r.campaign.name[:20]}]"))
    return hits


print(f"blottman.com sitelinks currently able to serve: {len(remaining_com())}\n")

if not APPLY:
    print("DRY RUN (pass --apply to execute)\n  UNLINK from account level:")
    for aid, why in REMOVE_ACCOUNT_SITELINKS.items():
        print(f"    {aid}  {why}")
    print("  LINK to BMX (top-up, already-approved .ca assets):")
    for aid, what in TOPUP_FOR_BMX.items():
        print(f"    {aid}  {what}")
    sys.exit(0)

# One operation per request: batched asset mutates are validated against pre-batch state
# and fail wholesale on this account (see fix_bmx_copy.py).
for aid, why in REMOVE_ACCOUNT_SITELINKS.items():
    op = client.get_type("CustomerAssetOperation")
    op.remove = f"customers/{cid}/customerAssets/{aid}~SITELINK"
    try:
        cust_service.mutate_customer_assets(customer_id=cid, operations=[op])
        print(f"  unlinked {aid}  {why}")
    except Exception as e:
        print(f"  FAILED   {aid}: {str(e)[-110:]}")

for aid, what in TOPUP_FOR_BMX.items():
    op = client.get_type("CampaignAssetOperation")
    op.create.campaign = ga.campaign_path(cid, BMX)
    op.create.asset = asset_service.asset_path(cid, aid)
    op.create.field_type = client.enums.AssetFieldTypeEnum.SITELINK
    try:
        camp_service.mutate_campaign_assets(customer_id=cid, operations=[op])
        print(f"  linked to BMX {aid}  {what}")
    except Exception as e:
        print(f"  FAILED link   {aid}: {str(e)[-110:]}")

print("\n--- verification ---")
left = remaining_com()
print(f"blottman.com sitelinks still able to serve: {len(left)}")
for aid, txt in left:
    print(f"  STILL LIVE: {aid} {txt}")

print("\nBMX sitelinks now:")
for r in ga.search(customer_id=cid, query=f"""
    SELECT campaign.id, campaign.status, asset.id, asset.sitelink_asset.link_text,
           asset.final_urls, campaign_asset.status
    FROM campaign_asset WHERE campaign.id = {BMX}
      AND campaign_asset.field_type = 'SITELINK' AND campaign_asset.status = 'ENABLED'"""):
    print(f"  {r.asset.id} | {r.asset.sitelink_asset.link_text[:24]:24} | {list(r.asset.final_urls)}")
