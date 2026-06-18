"""Fix Clickbait + superlative policy violations on PMAX - Blottman Max / Asset Group 1.
Replaces the 6 "98% Win Rate" assets + 1 "#1 Lawyer" asset with policy-compliant copy.
Flow: (1) create 7 new text assets, (2) link them to the asset group,
(3) remove the 7 old asset-group links. Old assets are left in the account (unlinked),
not deleted. Run: python fix_clickbait_assets.py
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

# old_asset_id -> (field_type, new_text)
REPLACEMENTS = {
    "283366485527": ("HEADLINE",      "Skilled Ticket Defence Team"),
    "283878683260": ("HEADLINE",      "Fight Auto Fines & Keep Points"),
    "283878683272": ("HEADLINE",      "Avoid Costly Demerit Points"),
    "283882668013": ("HEADLINE",      "Experienced Ticket Paralegal"),
    "283878683284": ("LONG_HEADLINE", "Fight Your Car Ticket & Keep Your Licence · Free Case Review With Blottman"),
    "283811294381": ("DESCRIPTION",   "Fight your car ticket with 24/7 legal help. 500+ cases handled. Free case review."),
    "373198526544": ("DESCRIPTION",   "Ontario traffic ticket specialists. Fight your ticket with a free case review today."),
}
LIMITS = {"HEADLINE": 30, "LONG_HEADLINE": 90, "DESCRIPTION": 90}

# --- locate the asset group + the live old links ---
ag_id = None
for r in ga.search(customer_id=cid, query="""
    SELECT asset_group.id, asset_group.name FROM asset_group
    WHERE campaign.name = 'PMAX - Blottman Max' AND asset_group.name = 'Asset Group 1'
"""):
    ag_id = r.asset_group.id
assert ag_id, "Could not find PMAX - Blottman Max / Asset Group 1"
ag_res = f"customers/{cid}/assetGroups/{ag_id}"

old_links = {}  # old_asset_id -> (resource_name, status, text)
for r in ga.search(customer_id=cid, query=f"""
    SELECT asset_group_asset.resource_name, asset.id, asset.text_asset.text,
           asset_group_asset.field_type, asset_group_asset.status
    FROM asset_group_asset
    WHERE asset_group.id = {ag_id} AND asset.type = 'TEXT'
"""):
    aid = str(r.asset.id)
    if aid in REPLACEMENTS:
        old_links[aid] = (r.asset_group_asset.resource_name,
                          r.asset_group_asset.status.name, r.asset.text_asset.text)

print(f"\n  Asset group: {ag_res}")
print("  Pre-flight — char validation + old-link status:\n")
ok = True
for aid, (ft, new_text) in REPLACEMENTS.items():
    n = len(new_text)
    within = n <= LIMITS[ft]
    status = old_links.get(aid, ("", "MISSING", ""))[1]
    ok = ok and within
    print(f"   [{ft:13}] {aid}  len={n:2} {'OK ' if within else 'OVER'}  old-link={status}")
    print(f"        new: {new_text}")
if not ok:
    print("\n  Aborting — a replacement is over the char limit.\n")
    raise SystemExit(1)

# --- 1) create new text assets ---
asset_svc = client.get_service("AssetService")
asset_ops, order = [], []
for aid, (ft, new_text) in REPLACEMENTS.items():
    op = client.get_type("AssetOperation")
    op.create.text_asset.text = new_text
    asset_ops.append(op)
    order.append(aid)
created = asset_svc.mutate_assets(customer_id=cid, operations=asset_ops)
new_asset_res = {order[i]: created.results[i].resource_name for i in range(len(order))}
print("\n  Created 7 new text assets.")

# --- 2) link new + 3) remove old ENABLED links (partial_failure tolerant) ---
aga_svc = client.get_service("AssetGroupAssetService")
link_ops, n_create, n_remove = [], 0, 0
for aid, (ft, _) in REPLACEMENTS.items():
    op = client.get_type("AssetGroupAssetOperation")
    op.create.asset_group = ag_res
    op.create.asset = new_asset_res[aid]
    op.create.field_type = client.enums.AssetFieldTypeEnum[ft]
    link_ops.append(op); n_create += 1
for aid in REPLACEMENTS:
    rn, status, _ = old_links.get(aid, (None, "MISSING", ""))
    if status == "ENABLED":
        op = client.get_type("AssetGroupAssetOperation")
        op.remove = rn
        link_ops.append(op); n_remove += 1
    else:
        print(f"  Skipping remove for {aid} (status={status}).")

req = client.get_type("MutateAssetGroupAssetsRequest")
req.customer_id = cid
req.operations = link_ops
req.partial_failure = True
resp = aga_svc.mutate_asset_group_assets(request=req)
err = resp.partial_failure_error
if err and err.message:
    print(f"\n  Partial-failure note: {err.message}")
applied = sum(1 for r in resp.results if r.resource_name)
print(f"\n  Attempted {n_create} link-adds + {n_remove} link-removes; {applied} ops succeeded.\n")
print("  DONE. New assets enter editorial review; recheck status in a few hours.\n")
