"""STAGED (read-only): measure the blast radius of candidate informational-intent
negatives against the last 14d of real search terms on Search Consolidated.

WHY: 27 of 34 scored keywords sit at QS<=3 and the campaign loses 72.84% of
impressions to RANK. Cause is phrase keywords matching a flood of zero-click
research queries ("what is stunt driving in ontario"), which drags expected CTR
-> QS -> Ad Rank. These queries cost ~nothing in dollars but are expensive in QS.

This script does NOT mutate anything. It prints, for each candidate negative,
exactly what it would have blocked (impr/clicks/cost/conv) and VETOES any
candidate that would have blocked a converting or healthy-CTR query.
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
ga = client.get_service("GoogleAdsService")
cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
CAMP = 23971101309
MASTER = 12109076551

# Candidate PHRASE negatives: pure-research patterns.
# Deliberately EXCLUDED (these convert or carry hire intent):
#   "how to fight", "dispute", "help", "lawyer", "near me", "cost to fight",
#   "best", "fight a"
CANDIDATES = [
    "how much is", "how much are", "how much does",
    "how many points", "how many demerit", "how many demerits",
    "demerit points for", "points for",
    "what is the fine", "what is the penalty", "what happens if",
    "fine for", "fines for", "penalty for", "penalties for",
    "how long does", "how long do",
    "can you go to jail", "is stunt driving a criminal",
    "laws", "what is stunt driving", "what is careless driving",
]

def toks(s):
    return [t for t in "".join(c if c.isalnum() or c.isspace() else " " for c in s.lower()).split() if t]

def contains_phrase(q_toks, p_toks):
    n = len(p_toks)
    return any(q_toks[i:i + n] == p_toks for i in range(len(q_toks) - n + 1))

# --- pull existing Master Negatives so we don't propose duplicates ---
existing = set()
for r in ga.search(customer_id=cid, query=f"""
    SELECT shared_criterion.keyword.text, shared_criterion.keyword.match_type
    FROM shared_criterion WHERE shared_set.id = {MASTER}"""):
    t = r.shared_criterion.keyword.text
    if t:
        existing.add(t.lower().strip())

# --- pull 14d search terms ---
terms = []
for r in ga.search(customer_id=cid, query=f"""
    SELECT campaign.id, search_term_view.search_term,
           metrics.impressions, metrics.clicks, metrics.cost_micros,
           metrics.conversions, metrics.all_conversions
    FROM search_term_view
    WHERE campaign.id = {CAMP} AND segments.date DURING LAST_14_DAYS"""):
    terms.append({
        "q": r.search_term_view.search_term,
        "impr": r.metrics.impressions,
        "clk": r.metrics.clicks,
        "cost": r.metrics.cost_micros / 1e6,
        "conv": r.metrics.all_conversions,
    })
for t in terms:
    t["toks"] = toks(t["q"])

print("=" * 78)
print(f"14d search terms on Search Consolidated: {len(terms)} distinct")
tot_i = sum(t['impr'] for t in terms); tot_c = sum(t['clk'] for t in terms)
tot_s = sum(t['cost'] for t in terms); tot_v = sum(t['conv'] for t in terms)
print(f"  impr={tot_i}  clicks={tot_c}  cost=${tot_s:.2f}  all_conv={tot_v:.0f}")
print(f"  overall CTR = {100*tot_c/tot_i if tot_i else 0:.2f}%")
print("=" * 78)

approved, vetoed = [], []
for cand in CANDIDATES:
    if cand in existing:
        vetoed.append((cand, "ALREADY in Master Negatives", None))
        continue
    p = toks(cand)
    hits = [t for t in terms if contains_phrase(t["toks"], p)]
    if not hits:
        vetoed.append((cand, "matches nothing in 14d (no evidence)", None))
        continue
    i = sum(h["impr"] for h in hits); c = sum(h["clk"] for h in hits)
    s = sum(h["cost"] for h in hits); v = sum(h["conv"] for h in hits)
    ctr = 100 * c / i if i else 0.0
    if v > 0:
        vetoed.append((cand, f"would block {v:.0f} CONVERSION(S)", (len(hits), i, c, s, v, ctr)))
    elif ctr >= 3.62:                     # >= campaign average CTR: not a QS drag
        vetoed.append((cand, f"CTR {ctr:.2f}% >= campaign avg, not a drag",
                       (len(hits), i, c, s, v, ctr)))
    else:
        approved.append((cand, (len(hits), i, c, s, v, ctr)))

print("\n### APPROVED candidates (zero conversions, below-average CTR = pure QS drag)")
print(f"{'negative':30s} {'terms':>5} {'impr':>6} {'clk':>4} {'cost':>8} {'CTR':>7}")
ai = ac = 0; asum = 0.0
for cand, (n, i, c, s, v, ctr) in sorted(approved, key=lambda x: -x[1][1]):
    print(f"  [PHR] {cand:24s} {n:5d} {i:6d} {c:4d} ${s:7.2f} {ctr:6.2f}%")
    ai += i; ac += c; asum += s
print(f"\n  TOTAL blocked: {ai} impr, {ac} clicks, ${asum:.2f}"
      f"  ({100*ai/tot_i if tot_i else 0:.1f}% of impressions, "
      f"{100*asum/tot_s if tot_s else 0:.1f}% of spend)")
print(f"  CTR of blocked traffic = {100*ac/ai if ai else 0:.2f}% vs campaign {100*tot_c/tot_i if tot_i else 0:.2f}%")

print("\n### VETOED candidates (do NOT add)")
for cand, why, stats in vetoed:
    extra = ""
    if stats:
        n, i, c, s, v, ctr = stats
        extra = f"  [{n} terms, {i} impr, {c} clk, ${s:.2f}, {v:.0f} conv, CTR {ctr:.2f}%]"
    print(f"  [PHR] {cand:24s} -> {why}{extra}")

print("\n### Sample of what the APPROVED set would have blocked (top 25 by impr)")
ap = [toks(c) for c, _ in approved]
blocked = [t for t in terms if any(contains_phrase(t["toks"], p) for p in ap)]
for t in sorted(blocked, key=lambda x: -x["impr"])[:25]:
    print(f"    {t['q'][:56]:58s} impr={t['impr']:4d} clk={t['clk']:3d} ${t['cost']:5.2f}")

print("\n### Converting terms in the period (MUST all survive)")
for t in sorted([t for t in terms if t["conv"] > 0], key=lambda x: -x["conv"]):
    hit = any(contains_phrase(t["toks"], p) for p in ap)
    print(f"    {'BLOCKED!! ' if hit else 'survives  '}{t['q'][:52]:54s} "
          f"conv={t['conv']:.0f} clk={t['clk']} ${t['cost']:.2f}")
