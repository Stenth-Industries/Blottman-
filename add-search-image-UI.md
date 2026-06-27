# Attach the Leslie image + business name to Search (UI-only — 2026-06-27)

Two visual-identity items can NOT be set via the Google Ads API for a **Search**
campaign. Both are quick manual steps in the UI. (The business **logo** is already
attached via API; only these two remain.)

## 1. Leslie photo as a Search image asset

The API rejects image assets on Search (`FIELD_TYPE_INCOMPATIBLE_WITH_CAMPAIGN_TYPE`)
— image extensions for Search are UI-only. The cropped, ready-to-upload file is in
the repo: **`ad-images/leslie_square_1200.png`** (1200×1200, 1:1).

Steps:
1. Google Ads → **Campaigns** → open **Search - Ontario Traffic Tickets (Consolidated)**.
2. Left nav → **Assets** → **Images** (or **+ → Image asset**).
3. Scope = this campaign. **Upload** `ad-images/leslie_square_1200.png`.
4. Crop tool: keep the 1:1 (already framed). Save.
5. It enters review (hours → ~1 day); shows on mobile search next to the ad.

> Only the SQUARE (1:1) was used — a 1.91:1 landscape crop of a portrait headshot
> cut her head / risked a framing disapproval. Square is the primary format and
> valid on its own.

## 2. Business name "Blottman Legal Services"

`business_name_asset` isn't an API-creatable field — business name is tied to
**Advertiser Verification / Account-level brand**, set in the UI. The correct
business name is **Blottman Legal Services** (matches the logo + legal entity),
NOT "Blottman Law".

Steps:
1. Google Ads → **Admin** (or **Tools**) → **Business identity / Advertiser
   verification** → set/confirm the verified business name = **Blottman Legal Services**.
2. The business **logo** is already linked (`ad-images/blottman_logo_black_1200.png` —
   the gold scales-of-justice mark from landing-v2 on brand-black). Once the verified
   business name is set, the name + logo render together on the ad.
3. NOTE: the account's old account-level "logo" was literally `fb ad.jpg` (a random
   image) — the proper square logo is now linked at the campaign level and overrides it.

After both: the Search ad shows business name + logo + Leslie's photo = the rich,
trustworthy look (closer to X-Copper).
