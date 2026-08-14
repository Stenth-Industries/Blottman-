"""Turn OFF automatically created text assets on BMX (campaign 22979153470).

WHY: the "Expanded final URL assets" report (UI, Aug-13) showed Google generating its
own headlines and descriptions for BMX by scraping the landing page, including:
    "Ontario Traffic Ticket Lawyers"                              (LSO: she is not a lawyer)
    "Get 98% win rate"                                            (unsubstantiated claim)
    "We represent ALL of Ontario and are SPECIALIZED in traffic
     ticket infractions with 98% win rate"                        (same)
    "Fight Driving With No Insurance Ticket & Win"                (outcome guarantee)
None of these exist in asset group 6607110351. They are auto-generated, which is why the
Aug-13 copy pass (17 assets removed for exactly these reasons) was being written back by
Google in parallel. Leaving this on means the copy pass never really holds.

Pairs with the UI-only fix applied the same day: Final URL expansion turned OFF, which
stopped BMX sending paid clicks to blottman.com subpages (real spend: CA$34.99 on
blottman.com/stunt-driving-ticket-lawyer/ on Aug 11). That was the actual cause of the
"One website per ad group" policy flag, and it is invisible to the API because
`url_expansion_opt_out` was removed from the Campaign resource in v24.

LEFT ON DELIBERATELY: GENERATE_IMAGE_EXTRACTION. It pulls images from the landing page,
which now means blottman.ca, and this account has been short of creative since June.
Images do not carry the claim risk that text does. Revisit if Leslie supplies real assets.

REVERT: set TEXT_ASSET_AUTOMATION back to OPTED_IN.

USAGE:  python code/stop_auto_assets_bmx.py            (dry run)
        python code/stop_auto_assets_bmx.py --apply
"""
import os
import sys
import logging

from dotenv import load_dotenv
from google.ads.googleads.client import GoogleAdsClient
from google.protobuf import field_mask_pb2

logging.getLogger("google.ads.googleads").setLevel(logging.CRITICAL)
load_dotenv()

APPLY = "--apply" in sys.argv
CAMPAIGN_ID = "22979153470"

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
campaign_service = client.get_service("CampaignService")
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")


def show(label):
    print(f"--- {label} ---")
    for r in ga.search(customer_id=cid, query=f"""
        SELECT campaign.id, campaign.name, campaign.status, campaign.asset_automation_settings
        FROM campaign WHERE campaign.id = {CAMPAIGN_ID}"""):
        for s in r.campaign.asset_automation_settings:
            print(f"  {s.asset_automation_type.name:42} {s.asset_automation_status.name}")
    print()


show("BEFORE")

if not APPLY:
    print("Would set TEXT_ASSET_AUTOMATION -> OPTED_OUT (all other settings preserved).")
    print("Dry run, nothing changed. Re-run with --apply.")
    sys.exit(0)

# Read current settings and resend the full list with only TEXT_ASSET_AUTOMATION flipped.
# Sending a partial list risks clearing the others (same class of trap as the Jul-17
# ai_max disable, which only worked when every related field went in one operation).
current = []
for r in ga.search(customer_id=cid, query=f"""
    SELECT campaign.id, campaign.asset_automation_settings
    FROM campaign WHERE campaign.id = {CAMPAIGN_ID}"""):
    current = list(r.campaign.asset_automation_settings)

op = client.get_type("CampaignOperation")
campaign = op.update
campaign.resource_name = campaign_service.campaign_path(cid, CAMPAIGN_ID)

# NOTE (logged Jul-17): AssetAutomationSetting is a NESTED type on Campaign, not a
# get_type() name -- client.get_type("AssetAutomationSetting") raises in v24.
Campaign = client.get_type("Campaign")
for s in current:
    setting = type(Campaign).AssetAutomationSetting()
    setting.asset_automation_type = s.asset_automation_type
    if s.asset_automation_type.name == "TEXT_ASSET_AUTOMATION":
        setting.asset_automation_status = client.enums.AssetAutomationStatusEnum.OPTED_OUT
    else:
        setting.asset_automation_status = s.asset_automation_status
    campaign.asset_automation_settings.append(setting)

client.copy_from(op.update_mask, field_mask_pb2.FieldMask(paths=["asset_automation_settings"]))
campaign_service.mutate_campaigns(customer_id=cid, operations=[op])
print("applied: TEXT_ASSET_AUTOMATION -> OPTED_OUT\n")

show("AFTER")
