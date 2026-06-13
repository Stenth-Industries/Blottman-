---
name: generate-ads
description: Generate high-performing, policy-compliant Google Responsive Search Ads (RSAs) plus campaign assets (sitelinks, callouts, structured snippets) for a service business. Use when the user wants to write ad copy, create or refresh RSAs, build a SKAG's ads, fix a low Ad Strength, or generate Google Ads headlines/descriptions/extensions. Generates against the project's ad specs and validates every asset to Google's editorial rules before output. Never publishes without explicit human approval.
---

# Generate Ads

Produce a complete, ready-to-review Responsive Search Ad (15 headlines + 4 descriptions) and the campaign assets that wrap it (sitelinks, callouts, structured snippets), built to convert and guaranteed to pass Google's automated editorial review.

## Authoritative specs — READ THESE FIRST every run

Before generating anything, read both spec files from the project root (locate with Glob if the path differs):

1. **`anatomy-of-a-good-ad.md`** — the RSA rubric: the 6 headline patterns, description angles, pinning decision tree, editorial hard rules, Quality Score factors, and the self-review checklist.
2. **`ad-assets-best-practices.md`** — sitelinks, callouts, structured snippets, business name/logo specs and the CTR math.

Those files are the source of truth. The rules embedded below are the non-negotiable safety floor — if the specs and this file ever disagree, the specs win on *strategy*, this file wins on *what gets an ad rejected*.

## Workflow

### Step 1 — Gather inputs (ask only for what's missing)

Collect, then echo back before generating:

- **Business / brand name** (≤25 chars, must match domain or legal entity)
- **Service / practice area** for this ad group
- **Target keyword / SKAG theme** (the exact search term to win) + **city/geo**
- **Landing page URL** (must be the real LP the ad points to)
- **Phone number** (for the call asset — never in headlines)
- **Verified trust signals**: years in business, real case/client counts, real ratings + review counts, awards, licensing. **Only what the user confirms is true.**
- **Offers / differentiators**: free consult, no-win-no-fee (only if real & permitted), response time, etc.

> For the **Blottman Law** project, auto-fill from `CLAUDE.md` / memory where possible: brand "Blottman Law"; practice areas careless/speeding/stunt driving, cell phone, suspended license (**NOT parking, NOT DUI** unless told); converting geos Toronto/Brampton/Mississauga/Hamilton; phone (647) 794-7750; known real claim "500+ car ticket cases handled". Still confirm anything you'd put a number on.

**Never invent data.** No fabricated star ratings, review counts, years, or guarantees. If a high-value slot wants a number you don't have, insert a clearly-marked `‹VERIFY: …›` placeholder and list it for the human instead of making one up.

### Step 2 — Generate the RSA

Per `anatomy-of-a-good-ad.md`:

- **15 headlines (fill all 15)**, each **≤30 chars**:
  - **3 keyword headlines** using the target keyword + city → mark these **PIN → Slot 1** (the only slot to pin).
  - **12 unpinned headlines** covering **≥5 of the 6 patterns**: offer/USP, trust/social proof, urgency, guarantee, CTA, brand. Variety is mandatory — no two headlines nearly identical.
- **4 descriptions (fill all 4)**, each **≤90 chars (aim 61–70)**, in **4 distinct angles**: (1) service+speed, (2) trust+price, (3) differentiator, (4) direct CTA.
- **Display URL** path1 + path2, each **≤15 chars**.

Label every headline with its pattern and pin status so the human can see the coverage.

### Step 3 — Generate the wrapping assets

Per `ad-assets-best-practices.md` (default everything to **campaign level** for a single SKAG):

- **6–8 sitelinks** — titles 12–15 chars, each to a distinct real page, specific (no "Learn More"), with two ≤35-char description lines.
- **8–12 callouts** — ≤25 chars, differentiated (not table-stakes), no repetition of headline content, covering speed/trust/value/guarantee.
- **2 structured snippet headers** (e.g. `Services` + `Types`), 4–10 values each, ≤25 chars, every value actually offered.
- Note business name + logo requirements if not already set.

### Step 4 — Validate (run the full checklist, show the result)

Count characters exactly. Reject-and-regenerate anything that fails. Confirm each item from the spec checklists, and especially the **hard rules** below.

### Step 5 — Output

Produce two things:
1. **Human-readable review block** — headlines (with pin/pattern tags + char counts), descriptions (with char counts), assets, and a **`‹VERIFY›` list** of any claim needing confirmation.
2. **Machine-readable YAML** mirroring the format in `ad-assets-best-practices.md` §6, ready to hand to a build/upload script.

### Step 6 — Human review gate (hard stop)

**Do NOT publish to the live account from this skill.** End with the review block and ask the human to approve. Only if they explicitly say "publish/upload" do you proceed to an upload step — and that's a separate, confirmed action on a live client account.

## Hard rules — an ad violating any of these gets auto-rejected

- Headlines **≤30 chars**; descriptions **≤90 chars**.
- **No exclamation marks in headlines.** Max **1** exclamation mark across the whole ad (descriptions only).
- **No ALL-CAPS words** (`FREE`, `BEST`, `#1`), no gimmicky spacing (`F R E E`), no repeated punctuation.
- **No symbols/emoji for emphasis** — only `·` and `&` are safe; a single `★` is OK only attached to a real rating (`4.9★`).
- **No phone numbers in display copy** — phone goes in the call asset only.
- **No unsubstantiated superlatives** (`#1`, `best`, `cheapest`, `guaranteed`) without third-party proof.
- **No competitor/trademark names** in copy.
- **Pin slot 1 only** (the 3 keyword headlines). Never pin slot 2/3 — it cuts combinations and costs 10–15% performance.
- **Talk about the customer, not "we/our/us."** No "Click here."

## Regulated verticals (legal, medical, finance) — extra caution

For **legal** (e.g. Blottman Law):
- **No outcome guarantees** ("Win Your Case", "Charges Dropped Guaranteed") and no banned legality claims ("Legal Solution", "Lawyer Approved").
- Avoid phrasing that **assumes/asserts the searcher committed a crime** — beyond being distasteful it interacts with Google's personalized-ads "criminal record" policy that has already throttled this account's PMAX. Frame around *fighting/defending the ticket*, not the person's guilt.
- Prefer real, provable signals ("500+ car ticket cases handled", "Free case review") over vague superlatives.
- Keep to the client's actual practice areas; don't generate ads for services they don't offer.

## Quality bar

Aim for **Ad Strength "Excellent"**: all 15 headlines filled, ≥5 of 6 patterns, keyword in the 3 pinned headlines, 4 distinct descriptions, zero near-duplicates. Remind the human that Ad Strength ≠ Quality Score — the landing page H1 should match the pinned keyword headline word-for-word.
