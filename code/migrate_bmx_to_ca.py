"""Migrate PMAX - Blottman Max (BMX) from blottman.com -> blottman.ca, and make the
website lead form biddable on that campaign.

WHY: BMX is ~60% of spend and still lands on the OLD site (blottman.com), which has no
form tag, no lead delivery, and a phone number people tap straight from cheap Display
clicks. Those taps register only as the phantom codeless "Contact Us" action (24 in 14d,
0 biddable, 9 of them from the Content network) and never reach Leslie as a lead. The .ca
site is form-first, tagged (AW-11165656868), and every submission emails
legal@blottman.com in real time via n8n.

WHAT IT DOES (4 changes, all on campaign 22979153470 only):
  1. asset_group 6607110351 final_urls: blottman.com/ -> blottman.ca/
  2. creates 2 NEW sitelink assets pointing at blottman.ca and links them to BMX
     (new assets rather than editing the old ones, because the old ones are SHARED with
     paused campaigns whose ads still point at .com -- editing in place would leave those
     campaigns with mixed domains and re-trigger the ONE_WEBSITE_PER_AD_GROUP disapproval
     from Jun-23/24 the moment anyone re-enables them)
  3. unlinks the 2 old .com sitelinks from BMX (assets themselves untouched)
  4. flips campaign_conversion_goal SUBMIT_LEAD_FORM/WEBSITE to biddable=True so form
     fills actually feed bidding (BMX was bidding on PHONE_CALL_LEAD only)

BONUS: old sitelink 283883603301 "Contact Us" carries description "98% Win Rate, Traffic
Law Experts" -- the unsubstantiated claim behind the Jun-17 clickbait flag, still live.
Unlinking it removes that claim from the account's biggest campaign.

REVERT VALUES (to undo):
  asset_group 6607110351 final_urls -> ["https://blottman.com/"]
  re-link sitelink assets 283883603298 ("Car Ticket Defence", blottman.com/)
                      and 283883603301 ("Contact Us", blottman.com/contact-us/)
  unlink the new sitelink assets printed by this script
  campaign_conversion_goal 22979153470~SUBMIT_LEAD_FORM~WEBSITE biddable -> False

USAGE:  python code/migrate_bmx_to_ca.py          (dry run, no mutations)
        python code/migrate_bmx_to_ca.py --apply  (applies)
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

CAMPAIGN_ID = "22979153470"          # PMAX - Blottman Max
ASSET_GROUP_ID = "6607110351"        # Asset Group 1
NEW_URL = "https://blottman.ca/"
OLD_SITELINK_ASSETS = ["283883603298", "283883603301"]

# .ca has no /contact-us route; the homepage carries the QuickForm, so both point home.
NEW_SITELINKS = [
    {
        "text": "Car Ticket Defence",
        "desc1": "Ontario traffic tickets",
        "desc2": "Free case review",
        "url": NEW_URL,
    },
    {
        "text": "Free Case Review",
        "desc1": "Tell us what happened",
        "desc2": "We reply within 1 day",
        "url": NEW_URL,
    },
]

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

banner = "APPLYING CHANGES" if APPLY else "DRY RUN (no mutations; pass --apply to execute)"
print(f"=== BMX -> blottman.ca | {banner} ===\n")


def show_state(label):
    print(f"--- {label} ---")
    for r in ga.search(customer_id=cid, query=f"""
        SELECT asset_group.id, asset_group.final_urls, campaign.id, campaign.status
        FROM asset_group WHERE asset_group.id = {ASSET_GROUP_ID}"""):
        print(f"  asset group {ASSET_GROUP_ID} final_urls = {list(r.asset_group.final_urls)}")
    for r in ga.search(customer_id=cid, query=f"""
        SELECT campaign.id, campaign.status, asset.id, asset.sitelink_asset.link_text,
               asset.sitelink_asset.description1, asset.final_urls, campaign_asset.status
        FROM campaign_asset
        WHERE campaign.id = {CAMPAIGN_ID} AND campaign_asset.field_type = 'SITELINK'
          AND campaign_asset.status = 'ENABLED'"""):
        s = r.asset.sitelink_asset
        print(f"  sitelink {r.asset.id} '{s.link_text}' d1='{s.description1}' -> {list(r.asset.final_urls)}")
    for r in ga.search(customer_id=cid, query=f"""
        SELECT campaign.id, campaign.status, campaign_conversion_goal.category,
               campaign_conversion_goal.origin, campaign_conversion_goal.biddable
        FROM campaign_conversion_goal WHERE campaign.id = {CAMPAIGN_ID}"""):
        g = r.campaign_conversion_goal
        if g.biddable or g.category.name == "SUBMIT_LEAD_FORM":
            print(f"  goal {g.category.name}/{g.origin.name} biddable={g.biddable}")
    print()


show_state("BEFORE")

if not APPLY:
    print("Would apply:")
    print(f"  1. asset group {ASSET_GROUP_ID} final_urls -> ['{NEW_URL}']")
    for sl in NEW_SITELINKS:
        print(f"  2. CREATE sitelink '{sl['text']}' -> {sl['url']}  ({sl['desc1']} / {sl['desc2']})")
    print(f"  3. UNLINK old sitelinks {OLD_SITELINK_ASSETS} from campaign {CAMPAIGN_ID}")
    print(f"  4. campaign_conversion_goal SUBMIT_LEAD_FORM/WEBSITE biddable -> True")
    sys.exit(0)

# ---- 1. asset group final URL -------------------------------------------------
ag_service = client.get_service("AssetGroupService")
op = client.get_type("AssetGroupOperation")
ag = op.update
ag.resource_name = ag_service.asset_group_path(cid, ASSET_GROUP_ID)
ag.final_urls.append(NEW_URL)
client.copy_from(op.update_mask, field_mask_pb2.FieldMask(paths=["final_urls"]))
ag_service.mutate_asset_groups(customer_id=cid, operations=[op])
print(f"[1/4] asset group {ASSET_GROUP_ID} final_urls -> {NEW_URL}")

# ---- 2. create new .ca sitelink assets ----------------------------------------
asset_service = client.get_service("AssetService")
new_asset_ids = []
for sl in NEW_SITELINKS:
    a_op = client.get_type("AssetOperation")
    asset = a_op.create
    asset.name = f"Sitelink (.ca) - {sl['text']}"
    asset.final_urls.append(sl["url"])
    asset.sitelink_asset.link_text = sl["text"]
    asset.sitelink_asset.description1 = sl["desc1"]
    asset.sitelink_asset.description2 = sl["desc2"]
    resp = asset_service.mutate_assets(customer_id=cid, operations=[a_op])
    rn = resp.results[0].resource_name
    new_asset_ids.append(rn.split("/")[-1])
    print(f"[2/4] created sitelink asset {rn.split('/')[-1]} '{sl['text']}' -> {sl['url']}")

# ---- 3. link new, unlink old ---------------------------------------------------
ca_service = client.get_service("CampaignAssetService")
ops = []
for aid in new_asset_ids:
    c_op = client.get_type("CampaignAssetOperation")
    ca = c_op.create
    ca.campaign = ga.campaign_path(cid, CAMPAIGN_ID)
    ca.asset = asset_service.asset_path(cid, aid)
    ca.field_type = client.enums.AssetFieldTypeEnum.SITELINK
    ops.append(c_op)
for aid in OLD_SITELINK_ASSETS:
    c_op = client.get_type("CampaignAssetOperation")
    c_op.remove = f"customers/{cid}/campaignAssets/{CAMPAIGN_ID}~{aid}~SITELINK"
    ops.append(c_op)
ca_service.mutate_campaign_assets(customer_id=cid, operations=ops)
print(f"[3/4] linked {new_asset_ids}, unlinked {OLD_SITELINK_ASSETS}")

# ---- 4. make the website lead form biddable ------------------------------------
# NOTE (Jul-11 gotcha): campaign_conversion_goal mutates fail as a batch but succeed
# one operation per request. BMX is already goal_config_level=CAMPAIGN.
ccg_service = client.get_service("CampaignConversionGoalService")
g_op = client.get_type("CampaignConversionGoalOperation")
goal = g_op.update
goal.resource_name = f"customers/{cid}/campaignConversionGoals/{CAMPAIGN_ID}~SUBMIT_LEAD_FORM~WEBSITE"
goal.biddable = True
client.copy_from(g_op.update_mask, field_mask_pb2.FieldMask(paths=["biddable"]))
ccg_service.mutate_campaign_conversion_goals(customer_id=cid, operations=[g_op])
print("[4/4] SUBMIT_LEAD_FORM/WEBSITE biddable -> True")

print()
show_state("AFTER")
