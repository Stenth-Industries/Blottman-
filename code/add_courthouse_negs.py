"""Add courthouse / court-office NAVIGATIONAL negatives to the shared list
'Master Negatives - Blottman (Stenth)' (12109076551).

Trigger: Leslie (Jul 17) "I keep getting calls for courthouse".

DIAGNOSIS (code/courthouse_diag.py, LAST_14_DAYS):
  - Source is SEARCH CONSOLIDATED (23971101309), not PMAX this time.
    64 court-ish search terms / 73 impr / 5 clicks / $29.20 = 10.3% of the
    campaign's 14-day spend ($284.11). PMAX (BMX) has only a trickle
    ("provincial offences court offices" 35 impr/1 clk).
  - ROOT CAUSE: the campaign has ZERO keywords containing 'court' (0 of 76).
    Every one of these queries arrived via AI MAX semantic expansion, enabled
    Jul-6. AI Max is matching "traffic ticket defence" out to the whole
    provincial-offences-court universe: courthouse addresses, court case
    lookup portals, dockets, court dates, Zoom links, prosecutor meetings.
  - These searchers want the GOVERNMENT COURT OFFICE (where is it / when is my
    date / what's my docket), not representation. They click, then phone Leslie
    asking courthouse questions. Same failure family as the Jul-5 'toronto ca
    aps' payment-portal leak.

WHY THE EXISTING NEGATIVES MISSED THEM:
  Only 2 of the 98 negatives were court-related ('[PHR] court services',
  '[PHR] early resolution'). '[PHR] court services' does NOT block
  'www durham courtservices' / 'www haltoncourtservices' because those are
  FUSED single tokens -- the exact same lesson as 'excopper'
  (promote_competitor_negs.py) and 'parkingticketdispute'
  (add_city_services_negs.py). Fused tokens each need their own BROAD negative.

DELIBERATELY NOT ADDED (would clip real hire intent):
  - bare 'court'      -> kills "do i have to go to court for careless driving",
                         "what happens at court for a speeding ticket" = people
                         who HAVE a ticket and are deciding whether to get help.
  - 'traffic court'   -> "brampton traffic court" is ambiguous (could be someone
                         seeking representation at that court); 0 clicks so far,
                         so no spend to save. Revisit if it starts costing.
  - 'phone number'    -> "traffic ticket lawyer phone number" is hire intent.
  - 'driver control'  -> MTO Driver Control suspension reviews are work she can
                         actually take.
  - 'how to fight'    -> historically converts (Jun-12 note). Untouched.

Idempotent -- skips terms already in the list.
Revert: delete these criteria from the shared set in the UI (Tools > Shared
library > Negative keyword lists > Master Negatives - Blottman (Stenth)).
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

SHARED_SET_ID = "12109076551"  # Master Negatives - Blottman (Stenth)
SHARED_SET = f"customers/{cid}/sharedSets/{SHARED_SET_ID}"

NEW_NEGS = [
    # --- the building / the office itself -------------------------------
    ("courthouse", "PHRASE"),        # simcoe/kitchener/pembroke/burlington courthouse
    ("court house", "PHRASE"),       # spaced variant
    ("court office", "PHRASE"),      # whitby court office, provincial court office near me
    ("court offices", "PHRASE"),     # negatives don't stem -- plural needs its own
    # --- record / docket / date lookup portals ---------------------------
    ("docket", "BROAD"),             # dockets ontario, search court docket by name
    ("dockets", "BROAD"),            # plural, again no stemming
    ("lookup", "BROAD"),             # court case/date lookup ontario (no hire query says "lookup")
    ("cacourtcaselookup", "BROAD"),  # www toronto cacourtcaselookup (fused)
    ("court records", "PHRASE"),     # free public court records ontario
    ("court cases", "PHRASE"),       # sudbury court cases, ontario court cases database
    ("check court date", "PHRASE"),  # how to check court date online
    # --- fused government-portal domains ---------------------------------
    ("courtservices", "BROAD"),      # www durham/brampton courtservices
    ("haltoncourtservices", "BROAD"),# www haltoncourtservices ca (fully fused)
    ("ontariocourts", "BROAD"),      # www ontariocourts ca
    ("ontariocourtdates", "BROAD"),  # ontariocourtdates ca
    ("ojpc", "BROAD"),               # https ojpc ca  -- see WARNING in output
    # --- DIY court process -----------------------------------------------
    ("court zoom", "PHRASE"),        # orangeville court zoom links, 2201 finch court zoom
    ("prosecutor", "PHRASE"),        # meeting with prosecutor for traffic ticket ontario
    ("court fine", "PHRASE"),        # pay court fine online
]

rows = ga.search(customer_id=cid, query=f"""
    SELECT shared_criterion.keyword.text, shared_criterion.keyword.match_type
    FROM shared_criterion
    WHERE shared_criterion.shared_set = '{SHARED_SET}'
      AND shared_criterion.type = 'KEYWORD'
""")
existing = {r.shared_criterion.keyword.text.lower() for r in rows}
print(f"  Shared list has {len(existing)} keyword negatives already.")

to_add = [(t, mt) for t, mt in NEW_NEGS if t.lower() not in existing]
for t, mt in NEW_NEGS:
    if t.lower() in existing:
        print(f"    skip (already present): {t}")

if to_add:
    svc = client.get_service("SharedCriterionService")
    ops = []
    for text, mt in to_add:
        op = client.get_type("SharedCriterionOperation")
        sc = op.create
        sc.shared_set = SHARED_SET
        sc.keyword.text = text
        sc.keyword.match_type = client.enums.KeywordMatchTypeEnum[mt]
        ops.append(op)
    res = svc.mutate_shared_criteria(customer_id=cid, operations=ops)
    print(f"\n  Added {len(res.results)} negatives to Master Negatives:")
    for (text, mt), r in zip(to_add, res.results):
        print(f"    [{mt[:3]}] {text}")
else:
    print("  Nothing to add.")

print("\n  WARNING - judgement call to review:")
print("    'ojpc' had 1 conversion ($8.72) in the last 14 days. That conversion is")
print("    almost certainly a junk form-fill from someone hunting the court portal")
print("    (exactly the caller Leslie is complaining about), but it IS a logged")
print("    conversion. Remove this one negative if you disagree.")

rows = ga.search(customer_id=cid, query=f"""
    SELECT campaign.name, campaign.status, campaign.advertising_channel_type
    FROM campaign_shared_set
    WHERE campaign_shared_set.shared_set = '{SHARED_SET}'
      AND campaign_shared_set.status = 'ENABLED'
""")
print("\n  List is attached to (enabled links):")
for r in rows:
    if r.campaign.status.name == "ENABLED":
        print(f"    {r.campaign.status.name:8} {r.campaign.advertising_channel_type.name:16} {r.campaign.name}")
