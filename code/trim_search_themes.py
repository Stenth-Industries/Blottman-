"""Re-anchor BMX search themes from 'lawyer' (a profession) to the offence (the problem).

WHY: 10 of the 20 themes contained "lawyer", which points PMAX at people shopping for
legal help in general. That neighbourhood includes legal aid, pro bono, public defenders
and other practice areas, which is precisely what BMX's negative list has spent two months
blocking. The negatives were fighting the themes. Offence-anchored themes describe someone
holding a ticket instead.

NOT an LSO issue: search themes are targeting, invisible to users. Same reasoning as
keeping "paralegal" as a Search keyword (Jun-27). The no-'lawyer' rule is for COPY.

Themes are hints, not targets, and Google weights them below landing page and conversion
history. Expect a nudge, not a turnaround.

REVERT: re-add the three removed themes listed in REMOVE_THEMES, remove the four in
ADD_THEMES.

USAGE:  python code/trim_search_themes.py            (dry run)
        python code/trim_search_themes.py --apply
"""
import os
import sys
import logging

from dotenv import load_dotenv
from google.ads.googleads.client import GoogleAdsClient

logging.getLogger("google.ads.googleads").setLevel(logging.CRITICAL)
load_dotenv()

APPLY = "--apply" in sys.argv
ASSET_GROUP_ID = "6607110351"

REMOVE_THEMES = {
    "how to fight a traffic ticket": "DIY anchor -> pulls the self-help/portal universe "
                                     "(courthouse, pay-a-ticket) that Leslie keeps complaining about",
    "license suspension lawyer": "duplicate of 'driving under suspension lawyer', which matches the .ca page",
    "HOV ticket": "not a listed practice area, negligible volume",
}
ADD_THEMES = [
    "stunt driving charge ontario",
    "careless driving ticket ontario",
    "driving without insurance charge",
    "traffic ticket defence ontario",
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
sig_service = client.get_service("AssetGroupSignalService")
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")

current = {}
for r in ga.search(customer_id=cid, query=f"""
    SELECT asset_group.id, asset_group_signal.search_theme.text,
           asset_group_signal.resource_name, campaign.status
    FROM asset_group_signal WHERE asset_group.id = {ASSET_GROUP_ID}"""):
    t = r.asset_group_signal.search_theme.text
    if t:
        current[t] = r.asset_group_signal.resource_name

print(f"current themes: {len(current)}\n")

if not APPLY:
    print("DRY RUN (pass --apply to execute)\n")
    for t, why in REMOVE_THEMES.items():
        print(f"  REMOVE  {'(found)' if t in current else '(NOT FOUND)'}  {t}\n            {why}")
    for t in ADD_THEMES:
        print(f"  ADD     {'(already present)' if t in current else ''}  {t}")
    print(f"\n  net: {len(current)} -> {len(current) - sum(1 for t in REMOVE_THEMES if t in current) + sum(1 for t in ADD_THEMES if t not in current)} (max 25)")
    sys.exit(0)

# One operation per request: batched asset-group mutates get validated against pre-batch
# state and fail wholesale (learned the hard way on the copy pass in this same session).
for t, why in REMOVE_THEMES.items():
    if t not in current:
        print(f"  skip (not found): {t}")
        continue
    op = client.get_type("AssetGroupSignalOperation")
    op.remove = current[t]
    try:
        sig_service.mutate_asset_group_signals(customer_id=cid, operations=[op])
        print(f"  removed: {t}")
    except Exception as e:
        print(f"  FAILED remove {t}: {str(e)[-110:]}")

for t in ADD_THEMES:
    if t in current:
        print(f"  skip (present): {t}")
        continue
    op = client.get_type("AssetGroupSignalOperation")
    op.create.asset_group = ga.asset_group_path(cid, ASSET_GROUP_ID)
    op.create.search_theme.text = t
    try:
        sig_service.mutate_asset_group_signals(customer_id=cid, operations=[op])
        print(f"  added:   {t}")
    except Exception as e:
        print(f"  FAILED add {t}: {str(e)[-110:]}")

print("\n--- final themes ---")
n = 0
for r in ga.search(customer_id=cid, query=f"""
    SELECT asset_group.id, asset_group_signal.search_theme.text,
           asset_group_signal.audience.audience, campaign.status
    FROM asset_group_signal WHERE asset_group.id = {ASSET_GROUP_ID}"""):
    s = r.asset_group_signal
    if s.search_theme.text:
        n += 1
        print(f"  {n:2}. {s.search_theme.text}")
    if s.audience.audience:
        print(f"  !! AUDIENCE SIGNAL PRESENT: {s.audience.audience}  (this is what caused the Jun-11 policy throttle)")
print(f"  total: {n}")
