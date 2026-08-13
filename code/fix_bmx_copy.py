"""BMX copy pass: remove outcome-guarantee + 'Lawyer' assets, add self-filtering copy.

WHY: BMX serves on Display/Discover where negatives do not apply, so the only way to stop
parking/payment/courthouse callers is to make the ad itself say what we do NOT do. Also
removes live LSO risk: Leslie is not a lawyer, and the account still carries "98% Win Rate"
and "100% Representation" callouts (the Jun-17 clickbait claim class).

Google text assets are IMMUTABLE -> the fix is unlink old + create new + link.
Old assets are only UNLINKED, never deleted, so a revert is just re-linking them.

COUNTS AFTER: 14 headlines, 5 long headlines, 5 descriptions, 4 campaign callouts.

USAGE:  python code/fix_bmx_copy.py            (dry run)
        python code/fix_bmx_copy.py --apply    (applies)
"""
import os
import sys
import logging

from dotenv import load_dotenv
from google.ads.googleads.client import GoogleAdsClient

logging.getLogger("google.ads.googleads").setLevel(logging.CRITICAL)
load_dotenv()

APPLY = "--apply" in sys.argv
CAMPAIGN_ID = "22979153470"
ASSET_GROUP_ID = "6607110351"

# ---- assets to UNLINK (id: reason) --------------------------------------------
REMOVE_HEADLINES = {
    "282913940132": "Fight Your Car Ticket & Win        -> outcome guarantee",
    "283878683263": "Beat Your Car Ticket Today         -> outcome guarantee",
    "283878683269": "Ticket Dismissals Start Here       -> outcome guarantee",
    "283882668016": "Fight Car Tickets Now & Win        -> outcome guarantee",
    "338094445045": "Get Your Ticket to Win             -> outcome guarantee",
    "338137632336": "Win your traffic ticket            -> outcome guarantee",
    "338138062593": "Fight Ticket & Win                 -> outcome guarantee",
    "338094444775": "We rep all of Ontario              -> sloppy, we-focused",
    "373352138609": "Experienced Ticket Paralegal       -> client directive: no 'paralegal' in copy",
}
REMOVE_LONG_HEADLINES = {
    "283878683290": "Expert Auto Ticket Lawyer...       -> LSO: not a lawyer",
    "300689359172": "Specialized Traffic Ticket Lawyers -> LSO: not a lawyer",
    "338396769304": "Traffic Ticket Lawyer Near Toronto -> LSO: not a lawyer",
    "338396769307": "Traffic Ticket Lawyer in Ontario   -> LSO: not a lawyer",
    "338138063454": "Fight Ticket & Win With Blottman   -> outcome guarantee",
}
REMOVE_DESCRIPTIONS = {
    "283878683278": "We reduce fines, dismiss tickets.. -> outcome guarantee ('dismiss')",
    "338094445168": "Traffic Ticket Lawyer Toronto ON.. -> LSO + outcome guarantee",
    "373352138615": "...with 24/7 legal help...         -> '24/7' invites all-hours junk calls",
}
REMOVE_CALLOUTS = {
    "283808909594": "98% Win Rate        -> unsubstantiated (the Jun-17 clickbait claim)",
    "283808909600": "100% Representation -> unsubstantiated",
    "283808909591": "24/7 Legal Help     -> invites all-hours calls; line is 9-18",
}

# ---- assets to CREATE ----------------------------------------------------------
NEW_HEADLINES = [
    "Ontario Traffic Tickets Only",   # 28  self-filter
    "Licensed in Ontario",            # 19  trust, LSO-safe (no lawyer/paralegal)
    "Free Case Review Online",        # 23  CTA, matches the .ca form
    "Speeding & Careless Tickets",    # 27  specific offences
    "Serving All of Ontario",         # 22  geo
]
NEW_LONG_HEADLINES = [
    "Ontario traffic ticket defence. We do not handle parking tickets or payments.",  # 77
    "Fighting speeding, careless and stunt driving charges across Ontario",           # 68
]
NEW_DESCRIPTIONS = [
    "Ontario traffic tickets only. We do not handle parking tickets or fine payments.",  # 80
    "Speeding, careless or stunt driving ticket in Ontario? Get a free case review.",    # 78
]
NEW_CALLOUTS = ["Ontario Tickets Only", "Free Case Review", "Licensed in Ontario"]

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
asset_service = client.get_service("AssetService")
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")

LIMITS = {"HEADLINE": 30, "LONG_HEADLINE": 90, "DESCRIPTION": 90, "CALLOUT": 25}


def validate():
    bad = []
    for label, items in (("HEADLINE", NEW_HEADLINES), ("LONG_HEADLINE", NEW_LONG_HEADLINES),
                         ("DESCRIPTION", NEW_DESCRIPTIONS), ("CALLOUT", NEW_CALLOUTS)):
        for t in items:
            if len(t) > LIMITS[label]:
                bad.append(f"{label} too long ({len(t)}): {t}")
            if "!" in t:
                bad.append(f"{label} has exclamation: {t}")
            for banned in ("lawyer", "98%", "guarantee", "paralegal"):
                if banned in t.lower():
                    bad.append(f"{label} banned term '{banned}': {t}")
    return bad


errs = validate()
if errs:
    print("VALIDATION FAILED:")
    for e in errs:
        print("  " + e)
    sys.exit(1)
print("Validation passed: all new copy within limits, no banned terms.\n")

if not APPLY:
    print("DRY RUN (pass --apply to execute)\n")
    for label, d in (("HEADLINE", REMOVE_HEADLINES), ("LONG_HEADLINE", REMOVE_LONG_HEADLINES),
                     ("DESCRIPTION", REMOVE_DESCRIPTIONS), ("CALLOUT", REMOVE_CALLOUTS)):
        print(f"UNLINK {label}:")
        for aid, why in d.items():
            print(f"  {aid}  {why}")
    print()
    for label, items in (("HEADLINE", NEW_HEADLINES), ("LONG_HEADLINE", NEW_LONG_HEADLINES),
                         ("DESCRIPTION", NEW_DESCRIPTIONS), ("CALLOUT", NEW_CALLOUTS)):
        print(f"CREATE {label}:")
        for t in items:
            print(f"  ({len(t):2}) {t}")
    sys.exit(0)


# Assets are looked up by text before creating. A batch that mixes links and unlinks
# fails validation (NOT_ENOUGH_LONG_HEADLINE_ASSET) but still leaves the created assets
# behind, so a naive re-run would duplicate them.
def _existing(kind):
    found = {}
    field = "text_asset.text" if kind == "TEXT" else "callout_asset.callout_text"
    for r in ga.search(customer_id=cid, query=f"""
        SELECT asset.id, asset.{field}, asset.type FROM asset WHERE asset.type = '{kind}'"""):
        t = r.asset.text_asset.text if kind == "TEXT" else r.asset.callout_asset.callout_text
        if t:
            found.setdefault(t, str(r.asset.id))
    return found


def get_or_create(texts, kind):
    existing = _existing(kind)
    ids = []
    for t in texts:
        if t in existing:
            ids.append(existing[t])
            print(f"  reusing {kind} asset {existing[t]}: {t[:50]}")
            continue
        op = client.get_type("AssetOperation")
        if kind == "TEXT":
            op.create.text_asset.text = t
        else:
            op.create.callout_asset.callout_text = t
        resp = asset_service.mutate_assets(customer_id=cid, operations=[op])
        ids.append(resp.results[0].resource_name.split("/")[-1])
        print(f"  created {kind} asset {ids[-1]}: {t[:50]}")
    return ids


def create_text_assets(texts):
    return get_or_create(texts, "TEXT")


def create_callout_assets(texts):
    return get_or_create(texts, "CALLOUT")


# ---- asset group assets: link new, unlink old ---------------------------------
aga_service = client.get_service("AssetGroupAssetService")
ag_path = ga.asset_group_path(cid, ASSET_GROUP_ID)

# TWO PASSES, REMOVALS FIRST. This order is forced from both sides:
#   - one batch mixing links + unlinks is validated against PRE-batch counts, so the
#     unlinks trip NOT_ENOUGH_LONG_HEADLINE_ASSET
#   - linking first trips RESOURCE_LIMIT, because max long headlines and descriptions is
#     5 each and this (grandfathered) group already sits at 8 and 6
# Removing first lands at 9 headlines / 3 long headlines / 3 descriptions, which clears
# every minimum, and the adds then land at 14 / 5 / 5, which clears every maximum.
def unlink_one(field, aid):
    op = client.get_type("AssetGroupAssetOperation")
    op.remove = f"customers/{cid}/assetGroupAssets/{ASSET_GROUP_ID}~{aid}~{field}"
    try:
        aga_service.mutate_asset_group_assets(customer_id=cid, operations=[op])
        return True, ""
    except Exception as e:
        msg = str(e)
        for token in ("NOT_ENOUGH", "RESOURCE_LIMIT", "NOT_FOUND", "MUTATE_NOT_ALLOWED"):
            if token in msg:
                return False, token
        return False, msg[-90:]


def link_one(field, aid):
    op = client.get_type("AssetGroupAssetOperation")
    op.create.asset_group = ag_path
    op.create.asset = asset_service.asset_path(cid, aid)
    op.create.field_type = getattr(client.enums.AssetFieldTypeEnum, field)
    try:
        aga_service.mutate_asset_group_assets(customer_id=cid, operations=[op])
        return True, ""
    except Exception as e:
        msg = str(e)
        for token in ("NOT_ENOUGH", "RESOURCE_LIMIT", "DUPLICATE"):
            if token in msg:
                return False, token
        return False, msg[-90:]


# One operation per request. Batches are rejected wholesale here: a mixed batch is
# validated against pre-batch counts, and a removals-only batch is evaluated against its
# own end state. Going one at a time applies each change against live counts and shows
# exactly where the asset group's real floor is.
for field, removes, adds in (
        ("LONG_HEADLINE", REMOVE_LONG_HEADLINES, NEW_LONG_HEADLINES),
        ("DESCRIPTION", REMOVE_DESCRIPTIONS, NEW_DESCRIPTIONS),
        ("HEADLINE", REMOVE_HEADLINES, NEW_HEADLINES)):
    print(f"\n--- {field} ---")
    for aid, why in removes.items():
        ok, err = unlink_one(field, aid)
        print(f"  {'unlinked' if ok else 'SKIPPED '} {aid}  {why}" + (f"   [{err}]" if err else ""))
    for aid in create_text_assets(adds):
        ok, err = link_one(field, aid)
        print(f"  {'linked  ' if ok else 'FAILED  '} {aid}" + (f"   [{err}]" if err else ""))

# ---- campaign callouts (same two-pass pattern) --------------------------------
ca_service = client.get_service("CampaignAssetService")
new_callouts = create_callout_assets(NEW_CALLOUTS)
ops = []
for aid in new_callouts:
    op = client.get_type("CampaignAssetOperation")
    op.create.campaign = ga.campaign_path(cid, CAMPAIGN_ID)
    op.create.asset = asset_service.asset_path(cid, aid)
    op.create.field_type = client.enums.AssetFieldTypeEnum.CALLOUT
    ops.append(op)
ca_service.mutate_campaign_assets(customer_id=cid, operations=ops)
ops = []
for aid in REMOVE_CALLOUTS:
    op = client.get_type("CampaignAssetOperation")
    op.remove = f"customers/{cid}/campaignAssets/{CAMPAIGN_ID}~{aid}~CALLOUT"
    ops.append(op)
ca_service.mutate_campaign_assets(customer_id=cid, operations=ops)
print("campaign callouts updated")

# ---- account-level callouts: remove claims we cannot support -------------------
# "Meet Our Lawyer": Leslie is not a lawyer (LSO).
# "Chat Support Available": blottman.ca has no chat widget -- the FloatingActions chat
# icon is a button that scrolls to the quote form. Verified in landing-v2 source.
cust_asset_service = client.get_service("CustomerAssetService")
REMOVE_ACCOUNT_CALLOUTS = {
    "324611694826": "Meet Our Lawyer",         # LSO: not a lawyer
    "324611694820": "Chat Support Available",  # no chat exists on blottman.ca
}   # 324611694823 "Get A Free Consultation" is true -> KEPT
ops = []
for aid in REMOVE_ACCOUNT_CALLOUTS:
    op = client.get_type("CustomerAssetOperation")
    op.remove = f"customers/{cid}/customerAssets/{aid}~CALLOUT"
    ops.append(op)
cust_asset_service.mutate_customer_assets(customer_id=cid, operations=ops)
print("account-level callouts removed: Meet Our Lawyer, Chat Support Available")

print("\nDone. New assets enter editorial review; the asset group keeps serving on the rest meanwhile.")
