# Form Conversion Tracking — Install Guide for blottman.com

**Goal:** make the Google Ads conversion action **"Submit Lead Form"** (id `7173263227`) fire when
a real contact form is submitted. The action has existed in the account for ages but was never
installed on the website — it has fired **0 times**. This guide is for whoever manages blottman.com.

**Why it matters:** today the account only counts a fuzzy auto-detected "Contact Us" signal
(~171/month — we don't fully trust what it measures). A real form conversion gives Google Ads a
clean lead signal to optimize toward, and is the foundation for the booked-consult ($) tracking later.

---

## Step 1 — Check the Google tag is on every page

The site already runs Google tracking (GA4 tag `G-GJSGF3MX1J` — the codeless "Contact Us" action
proves something is firing). Confirm this snippet (or an equivalent GTM container) is in the
`<head>` of **every page**:

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GJSGF3MX1J"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-GJSGF3MX1J');
</script>
```

If it's already there (likely), skip to Step 2 — do NOT add it twice.

## Step 2 — Fire the conversion on form submit

**Option A (preferred): thank-you page.** If submitting the contact form can redirect to a
dedicated page (e.g. `blottman.com/thank-you`), put this on that page only:

```html
<!-- Event snippet for Submit Lead Form conversion page -->
<script>
  gtag('event', 'conversion', {'send_to': 'AW-11165656868/RcgyCPuevdwaEKTOmcwp'});
</script>
```

A thank-you page is the cleanest: it can only be reached by submitting, it's testable, and GA4
can use the same page for its own goal.

**Option B: fire on successful submit (no redirect).** If the form shows an inline success message
instead (common with WordPress form plugins), call this in the form's success callback:

```js
gtag('event', 'conversion', {'send_to': 'AW-11165656868/RcgyCPuevdwaEKTOmcwp'});
```

Most WP form plugins (WPForms, CF7, Gravity) have a "custom JS on success" hook or a GTM
"form submit" trigger that can do this. **Do not** attach it to the submit *button click* —
that fires even when validation fails.

## Step 3 — (small but valuable) capture the gclid in the form

Add a hidden field to the contact form that stores the `gclid` URL parameter (persist it in a
cookie/localStorage so it survives navigation between landing and contact page), and include it
in the lead email / form entry. This is what later lets us tell Google "THIS lead became a booked
consultation" with a real dollar value. One hidden field now saves a project later.

## Step 4 — Test

1. Open the site with `?gclid=test123` appended to the URL.
2. Submit a test form entry (mark it TEST so the client knows).
3. In Google Ads: **Goals → Conversions → Summary → Submit Lead Form** — status should move from
   "Inactive/No recent conversions" to "Recording conversions" within a few hours (the conversion
   itself can take ~3h to appear; "Tag active" status can take up to 24h).
4. Also verify the test entry email arrived — this doubles as the form-delivery check.

---

*Generated 2026-06-12 from the Google Ads API (`code/form_tag_snippet.py`). The
`AW-11165656868/RcgyCPuevdwaEKTOmcwp` send_to label is specific to the "Submit Lead Form" action —
don't reuse it for other events.*
