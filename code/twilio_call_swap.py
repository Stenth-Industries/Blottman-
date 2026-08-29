"""Route all Google Ads calls through the Twilio whisper-greeting number.

WHY: 3 months of measurement (5 windows) show the junk-call rate is FLAT at
42-52% regardless of negatives, AI Max removal, or ad copy. PMAX matches
payment/courthouse queries semantically on the SEARCH network (93% of BMX
spend) and negatives cannot block a semantic category. So we stop trying to
stop Google generating them and stop them REACHING Leslie: an ~12s greeting on
a Twilio number in front of her carrier line.

  Google forwarding number -> Twilio number -> greeting -> (647) 794-7750

This does NOT add leads or save spend (the click is already paid for). It ends
the junk-call complaint cycle and, more importantly, Twilio logs FULL CALLER
NUMBERS - the missing half of call-based Offline Conversion Import, which
call_view cannot give us (it exposes caller_area_code only).

LIVE CALL ASSETS TODAY (code/call_assets_inventory.py, Aug-19):
  380047681148  campaign-level on Search Consolidated (23971101309)
  370129419278  ACCOUNT-level  -> this is what serves on BMX, whose own
                campaign-level call assets were removed Aug-11 (unlogged)
Both are (647) 794-7750, both scheduled 9:00-18:00 daily.

TWO PHASES - do not collapse them. Call assets are immutable like text assets,
so the number cannot be edited in place; a new asset must clear editorial
review before the old one is unlinked, or her ads lose the call extension for
days (the trap that stranded the lead form for weeks in June).

  python code/twilio_call_swap.py --create +1647XXXXXXX     # phase 1
  python code/twilio_call_swap.py --status                  # check review
  python code/twilio_call_swap.py --cutover                 # phase 2, after APPROVED

Add --apply to any phase to actually write. Default is a dry run.

THE stenth THRESHOLD IS NOT CHANGED AUTOMATICALLY, AND THE EARLIER 45 -> 57
PLAN WAS WRONG. Google measures duration from the moment TWILIO answers, so
the counted duration is greeting + ringing + conversation. None of those are
fixed: DTMF is accepted during playback, so a caller who presses 1 on hearing
the option adds about three seconds while one who listens through adds twelve,
and her line then rings for anywhere between five and twenty-five more. The
overhead is a distribution, not a constant, so any hardcoded number either
inflates counts (too low) or silently drops real conversions (too high). At 57
a genuine 45-second conversation answered on the second ring does not count.

Measure it instead. /api/voice/complete logs DialCallDuration, the real
conversation length, next to the call Google is timing. After a week of live
calls, compare the two and set the threshold from the data:

    python code/twilio_call_swap.py --cutover --apply --threshold 55

Until then it stays at 45. That errs toward counting a slightly short call,
which is the cheaper mistake.

REVERT: to roll back, relink 380047681148 to campaign 23971101309 and
370129419278 at account level. If --threshold was used, set stenth (7638369752)
phone_call_duration_seconds back to 45.
"""
import argparse
import logging
import os
import sys

from dotenv import load_dotenv
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

logging.getLogger("google.ads.googleads").setLevel(logging.WARNING)
load_dotenv("E:/Blottman-law/.env")
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

SEARCH_CAMPAIGN = "23971101309"
OLD_CAMPAIGN_ASSET = 380047681148     # Search Consolidated, campaign level
OLD_ACCOUNT_ASSET = 370129419278      # account level -> serves BMX
STENTH = 7638369752
DEFAULT_THRESHOLD = 45                # unchanged unless --threshold says so
ASSET_NAME = "Call - Twilio whisper (Stenth)"


def find_new_asset():
    """The Twilio-numbered call asset, if phase 1 already ran."""
    rows = ga.search(customer_id=cid, query="""
        SELECT asset.id, asset.name, asset.call_asset.phone_number,
               asset.policy_summary.approval_status
        FROM asset WHERE asset.type = 'CALL' """)
    return [r for r in rows if r.asset.name == ASSET_NAME]


def phase_create(number, apply):
    print("\n=== PHASE 1: create call asset for %s ===" % number)
    src = list(ga.search(customer_id=cid, query="""
        SELECT asset.id, asset.call_asset.phone_number, asset.call_asset.country_code,
               asset.call_asset.call_conversion_reporting_state,
               asset.call_asset.call_conversion_action
        FROM asset WHERE asset.id = %d """ % OLD_ACCOUNT_ASSET))
    if not src:
        sys.exit("  could not read source asset %d" % OLD_ACCOUNT_ASSET)
    s = src[0].asset.call_asset
    print("  cloning config from %d: country=%s reporting=%s"
          % (OLD_ACCOUNT_ASSET, s.country_code,
             s.call_conversion_reporting_state.name))
    print("  conversion action: %s" % (s.call_conversion_action or "(account default)"))

    op = client.get_type("AssetOperation")
    a = op.create
    a.name = ASSET_NAME
    a.call_asset.phone_number = number
    a.call_asset.country_code = s.country_code or "CA"
    a.call_asset.call_conversion_reporting_state = s.call_conversion_reporting_state
    if s.call_conversion_action:
        a.call_asset.call_conversion_action = s.call_conversion_action
    # same 9:00-18:00 daily schedule as the assets it replaces - change ONE thing
    for day in ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY",
                "SATURDAY", "SUNDAY"]:
        sch = client.get_type("AdScheduleInfo")
        sch.day_of_week = client.enums.DayOfWeekEnum[day]
        sch.start_hour = 9
        sch.end_hour = 18
        sch.start_minute = client.enums.MinuteOfHourEnum.ZERO
        sch.end_minute = client.enums.MinuteOfHourEnum.ZERO
        a.call_asset.ad_schedule_targets.append(sch)

    if not apply:
        print("  DRY RUN - would create the asset, then link it to:")
        print("    campaign %s (Search Consolidated)" % SEARCH_CAMPAIGN)
        print("    account level (serves BMX)")
        return

    res = client.get_service("AssetService").mutate_assets(
        customer_id=cid, operations=[op])
    rn = res.results[0].resource_name
    print("  created asset %s" % rn.split("/")[-1])

    cop = client.get_type("CampaignAssetOperation")
    cop.create.campaign = ga.campaign_path(cid, SEARCH_CAMPAIGN)
    cop.create.asset = rn
    cop.create.field_type = client.enums.AssetFieldTypeEnum.CALL
    client.get_service("CampaignAssetService").mutate_campaign_assets(
        customer_id=cid, operations=[cop])
    print("  linked to campaign %s" % SEARCH_CAMPAIGN)

    uop = client.get_type("CustomerAssetOperation")
    uop.create.asset = rn
    uop.create.field_type = client.enums.AssetFieldTypeEnum.CALL
    client.get_service("CustomerAssetService").mutate_customer_assets(
        customer_id=cid, operations=[uop])
    print("  linked at account level")
    print("\n  Both old and new now serve (Google rotates) until --cutover.")
    print("  Some calls bypass Twilio in the meantime. That is expected.")
    print("  Run --status until the new asset reads APPROVED, then --cutover.")


def phase_status():
    got = find_new_asset()
    if not got:
        sys.exit("  no Twilio call asset found - run --create first")
    for r in got:
        print("\n  asset %s | %s | %s"
              % (r.asset.id, r.asset.call_asset.phone_number,
                 r.asset.policy_summary.approval_status.name))
    print("\n  APPROVED -> safe to run --cutover")


def phase_cutover(apply, threshold):
    print("\n=== PHASE 2: unlink old assets + raise stenth threshold ===")
    got = find_new_asset()
    if not got:
        sys.exit("  no Twilio call asset found - run --create first")
    st = got[0].asset.policy_summary.approval_status.name
    print("  new asset %s is %s" % (got[0].asset.id, st))
    if st not in ("APPROVED", "APPROVED_LIMITED") and apply:
        sys.exit("  REFUSING: new asset is not approved. Her ads would lose the "
                 "call extension. Wait, then re-run.")

    print("  unlink campaign asset %d from %s" % (OLD_CAMPAIGN_ASSET, SEARCH_CAMPAIGN))
    print("  unlink account asset  %d" % OLD_ACCOUNT_ASSET)
    if threshold:
        print("  stenth %d: phone_call_duration_seconds -> %d" % (STENTH, threshold))
    else:
        print("  stenth %d: threshold LEFT AT %d - set it from a week of "
              "DialCallDuration logs, not arithmetic (see module docstring)"
              % (STENTH, DEFAULT_THRESHOLD))
    if not apply:
        print("\n  DRY RUN - nothing written.")
        return

    links = list(ga.search(customer_id=cid, query="""
        SELECT campaign.id, campaign_asset.resource_name FROM campaign_asset
        WHERE campaign.id = %s AND campaign_asset.field_type = 'CALL'
        AND campaign_asset.status = 'ENABLED'
        AND campaign_asset.asset = 'customers/%s/assets/%d' """
        % (SEARCH_CAMPAIGN, cid, OLD_CAMPAIGN_ASSET)))
    for link in links:
        op = client.get_type("CampaignAssetOperation")
        op.remove = link.campaign_asset.resource_name
        client.get_service("CampaignAssetService").mutate_campaign_assets(
            customer_id=cid, operations=[op])
        print("  unlinked %s" % link.campaign_asset.resource_name)

    alinks = list(ga.search(customer_id=cid, query="""
        SELECT customer_asset.resource_name FROM customer_asset
        WHERE customer_asset.field_type = 'CALL'
        AND customer_asset.status = 'ENABLED'
        AND customer_asset.asset = 'customers/%s/assets/%d' """
        % (cid, OLD_ACCOUNT_ASSET)))
    for link in alinks:
        op = client.get_type("CustomerAssetOperation")
        op.remove = link.customer_asset.resource_name
        client.get_service("CustomerAssetService").mutate_customer_assets(
            customer_id=cid, operations=[op])
        print("  unlinked %s" % link.customer_asset.resource_name)

    if threshold:
        casvc = client.get_service("ConversionActionService")
        op = client.get_type("ConversionActionOperation")
        op.update.resource_name = casvc.conversion_action_path(cid, STENTH)
        op.update.phone_call_duration_seconds = threshold
        op.update_mask.CopyFrom(protobuf_helpers.field_mask(None, op.update._pb))
        casvc.mutate_conversion_actions(customer_id=cid, operations=[op])
        print("  stenth threshold now %ds" % threshold)
    print("\n  DONE. Every ad call now hits the greeting first.")
    print("  NOTE: junk baseline resets - Twilio answers instantly, so calls that")
    print("  logged MISSED will now log RECEIVED-but-short. Do not compare the")
    print("  next week's duration bands to the 46% pre-change figure.")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--create", metavar="NUMBER",
                   help="Twilio number, E.164 e.g. +16475550100")
    p.add_argument("--status", action="store_true")
    p.add_argument("--cutover", action="store_true")
    p.add_argument("--apply", action="store_true",
                   help="actually write (default: dry run)")
    p.add_argument("--threshold", type=int, default=0,
                   help="cutover only: new stenth call-duration threshold, "
                        "derived from DialCallDuration logs. Omit to leave it "
                        "at %d." % DEFAULT_THRESHOLD)
    args = p.parse_args()
    if args.create:
        phase_create(args.create, args.apply)
    elif args.status:
        phase_status()
    elif args.cutover:
        phase_cutover(args.apply, args.threshold)
    else:
        p.print_help()
