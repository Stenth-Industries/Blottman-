"""STAGED — informational-intent negatives to lift Quality Score on Search
Consolidated. Does NOTHING unless run with --apply.

    python code/add_qs_drag_negs.py            # dry run, prints plan
    python code/add_qs_drag_negs.py --apply    # actually adds to Master Negatives

WHY (2026-08-09 audit, code/search_eligibility.py):
  Search Consolidated is ELIGIBLE and all 10 RSAs APPROVED (9/10 GOOD strength),
  but it loses 72.84% of impressions to RANK at only 20.37% impression share,
  and 27 of 34 scored keywords sit at QS<=3. Cause: phrase keywords match a
  flood of zero-click research queries, dragging expected CTR -> QS -> Ad Rank.

EVIDENCE (code/draft_informational_negs.py, LAST_14_DAYS, 1267 distinct terms):
  The 10 negatives below matched 489 impressions / 7 clicks (CTR ~1.4%) against
  a campaign average of 3.67%. Blocking them lifts measured CTR
  3.67% -> ~4.0% (a ~10% relative lift). This is a NUDGE, not a cure for the
  rank problem - see the honest caveat at the bottom.

VETOED by the data (do NOT add these, they out-perform the campaign average):
  how many points (CTR 17.14%), how long does (15.79%), how much does (20.00%),
  what is the fine (5.77%), penalty for (4.41%), points for (5.00%),
  can you go to jail (5.88%).
  -> People researching demerit points and penalties DO click. Leave them.

DROPPED for insufficient evidence (<10 impr in 14d, statistical noise):
  how many demerits (5), how much are (4), penalties for (3), how long do (3),
  how many demerit (1).

DELIBERATELY NOT TOUCHED (these convert / carry hire intent):
  "how to fight" (converted 2x on Jun-11), "dispute", "help", "lawyer",
  "near me", "cost to fight", "best".
  Verified: the period's only converting term, "stunt driving lawyer cost",
  survives this whole set.

REVERT: remove these 10 from shared set 12109076551 (Master Negatives).
"""
import sys
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
ga = client.get_service("GoogleAdsService")
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
MASTER = 12109076551

# (text, 14d impressions it would have blocked) — all PHRASE match
NEGATIVES = [
    ("fine for",                    171),
    ("how much is",                  78),
    ("what is stunt driving",        69),
    ("demerit points for",           44),
    ("what happens if",              31),   # borderline: CTR 3.23% vs 3.67% avg
    ("what is the penalty",          28),   # borderline: CTR 3.57% vs 3.67% avg
    ("fines for",                    20),
    ("is stunt driving a criminal",  18),
    ("what is careless driving",     16),
    ("laws",                         14),   # broadest of the set — watch it
]

APPLY = "--apply" in sys.argv

existing = set()
for r in ga.search(customer_id=cid, query=f"""
    SELECT shared_criterion.keyword.text FROM shared_criterion
    WHERE shared_set.id = {MASTER}"""):
    if r.shared_criterion.keyword.text:
        existing.add(r.shared_criterion.keyword.text.lower().strip())
print(f"Master Negatives currently holds {len(existing)} keywords.")

todo = [(t, i) for t, i in NEGATIVES if t.lower() not in existing]
skip = [t for t, _ in NEGATIVES if t.lower() in existing]
for t in skip:
    print(f"  skip (already present): {t}")

print(f"\nWould add {len(todo)} PHRASE negatives "
      f"(blocking ~{sum(i for _, i in todo)} impr / 14d):")
for t, i in todo:
    print(f"  [PHR] {t:30s}  ~{i} impr")

if not APPLY:
    print("\nDRY RUN — nothing changed. Re-run with --apply to commit.")
    raise SystemExit(0)

svc = client.get_service("SharedCriterionService")
ops = []
for t, _ in todo:
    op = client.get_type("SharedCriterionOperation")
    c = op.create
    c.shared_set = client.get_service("SharedSetService").shared_set_path(cid, MASTER)
    c.keyword.text = t
    c.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
    ops.append(op)
if ops:
    res = svc.mutate_shared_criteria(customer_id=cid, operations=ops)
    print(f"\nAdded {len(res.results)} negatives.")

n = sum(1 for _ in ga.search(customer_id=cid, query=f"""
    SELECT shared_criterion.keyword.text FROM shared_criterion
    WHERE shared_set.id = {MASTER}"""))
print(f"Master Negatives now holds {n} keywords.")
print("\nNOTE: this list is attached to BOTH enabled campaigns (BMX + Search),")
print("so it affects PMAX too. That is intended — same junk, both surfaces.")
