"""Validate RSA #2 for 'Traffic ticket lawyer broad' against the spec hard rules.
Exact char counts + editorial checks. No API calls."""
import re

FINAL_URL = "https://blottman.com"
PATH1, PATH2 = "traffic-tickets", "free-review"

headlines = [
    ("Traffic Ticket Lawyer Toronto", "HEADLINE_1", "keyword"),
    ("Ontario Traffic Ticket Lawyer", "HEADLINE_1", "keyword"),
    ("Traffic Ticket Lawyer Near You", "HEADLINE_1", "keyword"),
    ("Defend Your Driving Record", None, "offer"),
    ("Fight Demerit Points", None, "offer"),
    ("Protect Your Insurance Rate", None, "offer"),
    ("500+ Car Ticket Cases Handled", None, "trust"),
    ("Licensed Traffic Paralegals", None, "trust"),
    ("Serving Drivers Across the GTA", None, "trust"),
    ("Act Before Your Court Date", None, "urgency"),
    ("Talk to a Paralegal Today", None, "urgency"),
    ("Free, No-Obligation Review", None, "guarantee"),
    ("Upfront, Fair Pricing", None, "guarantee"),
    ("Book Your Free Consult", None, "cta"),
    ("Trust Blottman Law", None, "brand"),
]
descriptions = [
    "Fight your traffic ticket with experienced Ontario paralegals. Free case review.",
    "Licensed, LSO-regulated paralegals. Upfront, fair pricing with no hidden fees.",
    "Keep demerit points off your record and protect your insurance rate. Local team.",
    "Book your free, no-obligation case review today. Don't just pay the fine.",
]

OK_ACRONYMS = {"GTA", "LSO"}
SUPERLATIVES = ("#1", "best", "cheapest", "guaranteed", "guarantee", "no.1", "number one")
fails, warns = [], []

def caps_words(text):
    bad = []
    for w in re.findall(r"[A-Za-z][A-Za-z'+-]*", text):
        core = w.replace("+", "")
        if len(core) > 1 and core.isupper() and core not in OK_ACRONYMS:
            bad.append(w)
    return bad

print("\n  HEADLINES (limit 30)")
print("  " + "-"*52)
for i, (t, pin, pat) in enumerate(headlines, 1):
    n = len(t)
    flags = []
    if n > 30: flags.append(f"OVER {n}")
    if "!" in t: flags.append("has '!'")
    cw = caps_words(t)
    if cw: flags.append(f"ALLCAPS {cw}")
    if re.search(r"\d{3}[-.\s]?\d{3,4}", t): flags.append("phone?")
    for s in SUPERLATIVES:
        if s in t.lower(): flags.append(f"superlative '{s}'")
    for ch in t:
        if ch in "★☆→»>🔥*|~^": flags.append(f"symbol '{ch}'")
    status = "  ".join(flags) if flags else "ok"
    if flags: fails.append(f"H{i}: {status}")
    print(f"  {i:>2}. ({n:>2}) [{(pin or '-'):<10}] {t:<31} {status}")

print("\n  DESCRIPTIONS (limit 90)")
print("  " + "-"*52)
total_excl = 0
for i, d in enumerate(descriptions, 1):
    n = len(d)
    e = d.count("!")
    total_excl += e
    flags = []
    if n > 90: flags.append(f"OVER {n}")
    cw = caps_words(d)
    if cw: flags.append(f"ALLCAPS {cw}")
    if re.search(r"\d{3}[-.\s]?\d{3,4}", d): flags.append("phone?")
    status = "  ".join(flags) if flags else "ok"
    if flags: fails.append(f"D{i}: {status}")
    print(f"  {i}. ({n:>2}) excl={e}  {status}")

print("\n  AD-LEVEL CHECKS")
print("  " + "-"*52)
pinned = [h for h in headlines if h[1] == "HEADLINE_1"]
kw_pinned = all(h[2] == "keyword" for h in pinned)
patterns = {h[2] for h in headlines if h[1] is None}
texts = [h[0].lower() for h in headlines]
dupes = len(texts) != len(set(texts))
checks = [
    (f"15 headlines filled", len(headlines) == 15),
    (f"4 descriptions filled", len(descriptions) == 4),
    (f"exactly 3 pinned to slot 1 (got {len(pinned)})", len(pinned) == 3),
    (f"all pinned are keyword headlines", kw_pinned),
    (f">=5 of 6 unpinned patterns (got {len(patterns)}: {sorted(patterns)})", len(patterns) >= 5),
    (f"<=1 exclamation across ad (got {total_excl})", total_excl <= 1),
    (f"no duplicate headlines", not dupes),
    (f"path1 <=15 ({len(PATH1)})", len(PATH1) <= 15),
    (f"path2 <=15 ({len(PATH2)})", len(PATH2) <= 15),
]
for label, ok in checks:
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    if not ok: fails.append(label)

print("\n  " + ("ALL CHECKS PASSED ✓" if not fails else f"{len(fails)} FAILURES").replace("✓","OK"))
for f in fails: print(f"    - {f}")
print()
