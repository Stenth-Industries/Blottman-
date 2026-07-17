"""Recalibrate the stenth call tracker per Leslie (Jul-17, via Kushagra):
  - a conversion = a call of >= 45 SECONDS (was 30s) - her confirmation proxy
  - her average revenue per conversion = $400 (action had $150; originally $500)

Three changes, applied together because they interact:

  1. ConversionAction `Inbound call - Blottman (stenth)` (7638369752):
     phone_call_duration_seconds 30 -> 45, default_value $150 -> $400
     (always_use_default_value stays True).

  2. BMX (22979153470) tCPA $60 -> $95. REQUIRED, not optional: 14 of the last
     30d's 31 qualifying BMX calls are 30-44s, so the 45s threshold cuts ~45%
     of counted conversions. BMX 30d = $1,583.69 / 17 calls >=45s = $93.16 true
     CPA under the new definition. Leaving tCPA at $60 (set earlier today
     against the 30s definition) recreates the Jul 6-17 throttle. At Leslie's
     $400/conv, $95 CPA = 4.2x return.

  3. (context, no mutation) Dashboard for Leslie is ON HOLD (user decision) ->
     the Retained?-driven Offline Conversion Import plan is parked; the 45s
     threshold is the interim quality gate. When OCI revives, $400 is the
     value to upload, and value-based bidding targets ~400% tROAS.

REVERT VALUES: duration 30, default_value 150.0, BMX tCPA 60_000_000.
NOTE: values do NOT affect current bidding (tCPA/MaxConv are count-based);
$400 matters for reporting honesty + the future tROAS switch. The DURATION
change is the behavioral one - fewer, better conversions from today forward
(not retroactive).
"""
from dotenv import load_dotenv
import os, logging
from google.ads.googleads.client import GoogleAdsClient
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

STENTH = 7638369752
BMX = "22979153470"

print("--- 1. stenth action: 45s threshold + $400 value ---")
casvc = client.get_service("ConversionActionService")
op = client.get_type("ConversionActionOperation")
ca = op.update
ca.resource_name = casvc.conversion_action_path(cid, STENTH)
ca.phone_call_duration_seconds = 45
ca.value_settings.default_value = 400.0
ca.value_settings.always_use_default_value = True
op.update_mask.paths.extend([
    "phone_call_duration_seconds",
    "value_settings.default_value",
    "value_settings.always_use_default_value",
])
try:
    res = casvc.mutate_conversion_actions(customer_id=cid, operations=[op])
    print(f"  OK: {res.results[0].resource_name}")
except Exception as e:
    print(f"  FAILED: {str(e)[:400]}")
    print("  (if MUTATE_NOT_ALLOWED: do it in UI - Goals > Conversions > stenth action)")

print("\n--- 2. BMX tCPA $60 -> $95 (match the 45s-definition CPA of $93.16) ---")
csvc = client.get_service("CampaignService")
op = client.get_type("CampaignOperation")
camp = op.update
camp.resource_name = csvc.campaign_path(cid, BMX)
camp.maximize_conversions.target_cpa_micros = 95_000_000
op.update_mask.paths.append("maximize_conversions.target_cpa_micros")
try:
    res = csvc.mutate_campaigns(customer_id=cid, operations=[op])
    print(f"  OK: {res.results[0].resource_name}")
except Exception as e:
    print(f"  FAILED: {str(e)[:400]}")

print("\n--- verify ---")
for r in ga.search(customer_id=cid, query=f"""
 SELECT conversion_action.phone_call_duration_seconds,
        conversion_action.value_settings.default_value,
        conversion_action.value_settings.always_use_default_value
 FROM conversion_action WHERE conversion_action.id = {STENTH}"""):
    c = r.conversion_action
    print(f"  stenth: duration={c.phone_call_duration_seconds}s "
          f"value=${c.value_settings.default_value:.2f} always_use={c.value_settings.always_use_default_value}")
for r in ga.search(customer_id=cid, query=f"""
 SELECT campaign.maximize_conversions.target_cpa_micros
 FROM campaign WHERE campaign.id = {BMX}"""):
    print(f"  BMX tCPA=${r.campaign.maximize_conversions.target_cpa_micros/1e6:.2f}")
