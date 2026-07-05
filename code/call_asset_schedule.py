"""Set an answerable-hours ad schedule (daily 9:00-18:00, account TZ = Toronto)
on the 4 CALL assets serving live surfaces, so the call button only shows when
someone actually picks up — after-hours ad clicks land on the website form
instead of a dead line. Ads themselves keep serving 24/7.

Basis (call_view, last 30d): every >=30s call landed 9:03am-5:15pm (incl. Sunday
mornings); misses/hangups cluster 12:53am, 8:23-8:43am, 7:31pm.

Assets updated (from call_assets_inventory.py):
  370852648512  PMAX - Blottman Max        (had M-F 7-21 / Sat 8-18 / Sun 9-17 -> tightened)
  380047681148  Search Consolidated        (had NO schedule)
  82358852814   Blottman New pM + paused Search campaigns (had NO schedule)
  370129419278  account-level              (had NO schedule)
Repeated-field update REPLACES the whole schedule list. Revert = re-run with the
old values above, or clear ad_schedule_targets."""
from dotenv import load_dotenv
import os, logging
from google.ads.googleads.client import GoogleAdsClient
from google.protobuf import field_mask_pb2
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

ASSET_IDS = [
    "370852648512",  # BMX
    "380047681148",  # Search Consolidated
    "82358852814",   # Blottman New pM (+ paused Search links)
    "370129419278",  # account-level
]
DAYS = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
START_HOUR, END_HOUR = 9, 18

svc = client.get_service("AssetService")
ops = []
for aid in ASSET_IDS:
    op = client.get_type("AssetOperation")
    a = op.update
    a.resource_name = f"customers/{cid}/assets/{aid}"
    for day in DAYS:
        s = client.get_type("AdScheduleInfo")
        s.day_of_week = client.enums.DayOfWeekEnum[day]
        s.start_hour = START_HOUR
        s.start_minute = client.enums.MinuteOfHourEnum.ZERO
        s.end_hour = END_HOUR
        s.end_minute = client.enums.MinuteOfHourEnum.ZERO
        a.call_asset.ad_schedule_targets.append(s)
    client.copy_from(
        op.update_mask,
        field_mask_pb2.FieldMask(paths=["call_asset.ad_schedule_targets"]),
    )
    ops.append(op)

res = svc.mutate_assets(customer_id=cid, operations=ops)
print(f"Updated {len(res.results)} call assets to daily {START_HOUR}:00-{END_HOUR}:00:")
for r in res.results:
    print(f"  {r.resource_name}")

# verify
print("\n=== VERIFY ===")
for r in ga.search(customer_id=cid, query="""
    SELECT asset.id, asset.call_asset.phone_number, asset.call_asset.ad_schedule_targets
    FROM asset WHERE asset.type = 'CALL'
"""):
    if str(r.asset.id) in ASSET_IDS:
        sched = "; ".join(
            f"{s.day_of_week.name[:3]} {s.start_hour}-{s.end_hour}"
            for s in r.asset.call_asset.ad_schedule_targets
        )
        print(f"  asset {r.asset.id}: {sched}")
