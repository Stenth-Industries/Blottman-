"""Attach the existing Lead Form asset (371903420556) to the two Search SKAGs
that don't have it yet: 'Lower Value - New' and 'Higher Value - New'.
Skips any campaign that already has an ENABLED link (idempotent).
Run: python attach_lead_form.py
"""
from dotenv import load_dotenv
import os, logging
from google.ads.googleads.client import GoogleAdsClient

logging.getLogger("google.ads.googleads").setLevel(logging.WARNING)
load_dotenv("E:/Blottman-law/.env")
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

LEAD_FORM_ASSET = "371903420556"
TARGET_NAMES = {"Lower Value - New", "Higher Value - New"}
asset_res = f"customers/{cid}/assets/{LEAD_FORM_ASSET}"

# resolve target campaign ids
targets = {}
for r in ga.search(customer_id=cid, query="""
    SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type
    FROM campaign WHERE campaign.status='ENABLED'
"""):
    if r.campaign.name in TARGET_NAMES:
        targets[r.campaign.id] = (r.campaign.name, r.campaign.advertising_channel_type.name)

# which already have it
already = set()
for r in ga.search(customer_id=cid, query=f"""
    SELECT campaign.id, campaign.status, campaign_asset.status
    FROM campaign_asset
    WHERE asset.id={LEAD_FORM_ASSET} AND campaign.status='ENABLED'
      AND campaign_asset.status='ENABLED'
"""):
    already.add(r.campaign.id)

svc = client.get_service("CampaignAssetService")
ops, planned = [], []
for cmp_id, (name, chan) in targets.items():
    if cmp_id in already:
        print(f"  SKIP (already linked): {name}")
        continue
    op = client.get_type("CampaignAssetOperation")
    op.create.campaign = f"customers/{cid}/campaigns/{cmp_id}"
    op.create.asset = asset_res
    op.create.field_type = client.enums.AssetFieldTypeEnum.LEAD_FORM
    ops.append(op)
    planned.append(f"{name} ({chan})")

if not ops:
    print("\n  Nothing to do — both targets already have the lead form.\n")
    raise SystemExit

print("\n  Will link lead form to:")
for p in planned:
    print(f"   + {p}")
resp = svc.mutate_campaign_assets(customer_id=cid, operations=ops)
print(f"\n  Linked {len(resp.results)}:")
for res in resp.results:
    print(f"   {res.resource_name}")

# verify
print("\n  Verify — ENABLED lead-form links on the targets:")
for r in ga.search(customer_id=cid, query=f"""
    SELECT campaign.name, campaign_asset.status
    FROM campaign_asset
    WHERE asset.id={LEAD_FORM_ASSET} AND campaign.status='ENABLED'
"""):
    if r.campaign.name in TARGET_NAMES:
        print(f"   [{r.campaign.name}] link={r.campaign_asset.status.name}")
print()
