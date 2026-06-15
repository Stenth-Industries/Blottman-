# Blottman Law — Landing Page v2 (Next.js)

A single, conversion-focused landing page for the Ontario traffic-ticket campaigns.
Built with **Next.js (App Router) + TypeScript + Tailwind**. No site header/footer — it's
one page designed to be skim-read and to capture a quote/case-review lead.

**Design** is modelled on [gardewilson.com.au](https://www.gardewilson.com.au/): a
**black + gold** palette, **heavy condensed display headlines** (Google **Anton** ≈ their
"Thunder" font) paired with **Poppins** for body, all-caps eyebrows, two-tone headlines
(one word in metallic gold), and their strong numbered patterns (Expertise grid + How-it-works
process). Colours/fonts live in `tailwind.config.ts` and `app/layout.tsx`.

## Run it
```bash
cd landing-v2
npm install        # already done
npm run dev        # http://localhost:3000
npm run build      # production build check
```

## What's on the page (top → bottom)
1. **Hero** — two-tone condensed headline, skim bullets, gold CTA, 24/7 call link, Trustpilot stars, photo placeholder + "500+" stat badge.
2. **Logo bar** — scrolling "As featured in" marquee, 9 placeholder logos.
3. **Attention banner** — gold "First ticket?" strip (Garde Wilson pattern).
4. **Expertise** — numbered 01–06 practice-area grid on black (Garde Wilson pattern).
5. **How it works** — numbered 01–04 process steps (Garde Wilson "What happens" pattern).
6. **Video testimonials** — 3×3 grid of placeholders.
7. **Portfolio / recent results** — outcome cards with image placeholders.
8. **Case studies** — 2 before/after transformations.
9. **Trustpilot widget** — placeholder, 4.7★ over 67 reviews.
10. **Written testimonials** — 3×3 grid (9 reviews, name + location + date).
11. **FAQ** — biggest objections to fighting a ticket.
12. **Quote form** — first name, last name, email, phone.
13. **Sticky CTA** — mobile-only single CTA fixed to the bottom.

## CTAs
- **Desktop:** every major section ends with its own CTA (`components/SectionCta.tsx`).
- **Mobile:** those are hidden; one fixed bottom CTA shows instead (`components/StickyCta.tsx`).
- All CTAs scroll to the `#quote` form.

## Placeholders to replace with real assets
- **Phone number:** currently `(123) 456-7890` in `lib/content.ts` (`PHONE_DISPLAY` / `PHONE_TEL`).
  The real campaign number is `(647) 794-7750` — swap when confirmed.
- **Video testimonials:** real footage in `components/VideoTestimonials.tsx`.
- **Logos:** real images in `components/LogoBar.tsx` (data in `lib/content.ts`).
- **Portfolio / case-study images:** image placeholders in those components.
- **Trustpilot:** swap the placeholder block for the official Trustpilot embed.
- **Form submit:** `components/QuoteForm.tsx` logs to console — wire to Netlify Forms or an
  API route, and add the `gclid` capture + Google Ads conversion (see `../landing/README.md`).

## Edit copy in one place
All text/data lives in **`lib/content.ts`**.
