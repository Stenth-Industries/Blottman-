# Twilio call screening — setup runbook

**Status: the call flow is built and tested. Nothing is live.** What remains is a
Twilio account, a number, three environment variables, and the two-phase swap in
Google Ads.

## Why this exists

Six consecutive measurement windows put the junk-call rate at 42–53%: 42, 46,
47, 53, 46, 53. Negatives, removing AI Max, retargeting the PMAX themes and a
full copy rewrite have all failed to move it, because PMAX matches semantically
and a negative keyword cannot block a category. This does not try to stop Google
generating those calls. It stops them reaching Leslie.

The second reason matters more in the long run. Twilio logs the **full caller
number**; `call_view` gives us `caller_area_code` and nothing else. That number,
plus the call start time, is exactly the key that call-based offline conversion
import needs, and most of BMX's conversions are calls.

## The call flow

```
Google forwarding number → Twilio number → blottman.ca/api/voice → her line
```

1. Twilio answers immediately and reads Leslie's greeting (her wording, Aug 20):
   *"Thanks for calling Blottman Legal Services. If you have received a traffic
   ticket or summons to court, press 1. To pay a fine or reach a courthouse,
   press 2."*
2. **1** → dials `+1 647 794 7750`, caller's own number passed through as caller
   ID, real ringback in their ear.
3. **2** → *"Please contact the courthouse that issued your ticket for
   assistance in payment or inquiries. Goodbye."* Her phone never rings.
4. **Nothing pressed, or any other key → the call connects anyway.** Failing
   open is deliberate: dropping a confused real client costs far more than
   letting one junk call through.
5. No answer after 25 seconds → a short message pointing at blottman.ca.

Digits are accepted while the greeting is still playing, so a real caller is
through in a few seconds and never experiences it as a phone tree.

Every step is logged as one JSON line with the caller's number, the key pressed,
and — at the end of the call — `DialCallDuration`, the real conversation length.
**That keypress is the first direct measurement of the junk rate we have ever
had.** Everything before it was inferred from duration and area code.

## What you do in the Twilio console

1. Create the account under a Stenth email (not Leslie's — this is our
   infrastructure and needs to survive her staff changes).
2. Buy a **Canadian local number** with Voice capability. A 647 or 416 reads as
   local to a GTA caller. Note it in E.164 form, e.g. `+16475550100`.
3. On that number: **Voice & Fax → A call comes in → Webhook**
   `https://blottman.ca/api/voice`, **HTTP POST**. Leave the status callback
   empty; the flow handles its own logging.
4. Copy the **Auth Token** from the console dashboard.

Rough running cost at this volume is a couple of dollars a month for the number
plus about a cent a minute in each direction. Confirm the current rates in the
console rather than trusting this line.

## Environment variables (Vercel → landing-v2 → Production **and** Preview)

| Variable | Value | Why |
|---|---|---|
| `TWILIO_AUTH_TOKEN` | from the console | Turns on request-signature verification. Until it is set, the endpoints accept anyone's POST. |
| `TWILIO_PUBLIC_BASE_URL` | `https://blottman.ca` | The signature is computed over the URL Twilio called, and behind Vercel's proxy the request URL is the internal one. |
| `TWILIO_FORWARD_TO` | `+16477947750` | Optional. Defaults to that number. |
| `TWILIO_AFTER_HOURS` | `ring` or `message` | Optional, defaults to `ring`. See the open question below. |
| `TWILIO_OPEN_HOUR` / `TWILIO_CLOSE_HOUR` | `9` / `19` | Optional, Toronto time, only consulted when the mode is `message`. |
| `CALL_LOG_WEBHOOK_URL` | n8n webhook | Optional. Without it the call events live only in Vercel's logs, which expire. Worth wiring to a Calls tab on the Lead Tracker before the measurement week starts. |

Redeploy after setting them.

## Test before touching Google Ads

Call the Twilio number from a mobile and check all four paths: press 1 and
confirm her phone rings with **your** number showing, press 2 and confirm the
courthouse message plays and her phone stays silent, say nothing and confirm it
still connects, and call once while her phone is off to hear the no-answer
message.

## Then the Google Ads swap

```bash
python code/twilio_call_swap.py --create +1647XXXXXXX --apply   # phase 1
python code/twilio_call_swap.py --status                        # until APPROVED
python code/twilio_call_swap.py --cutover --apply               # phase 2
```

Phase 1 leaves both the old and the new number serving while the new call asset
clears editorial review, so her ads never lose the call extension — the trap
that stranded the lead form for weeks in June. Some calls bypass the greeting in
the meantime; that is expected. Phase 2 only runs once the asset reads APPROVED,
and the script refuses if it does not.

## Do not raise the stenth threshold on arithmetic

The earlier plan was to move the 45-second threshold to 57 to absorb the
greeting. That is wrong. Google times the call from the moment **Twilio**
answers, so the counted duration is greeting + ringing + conversation, and none
of those are constant: a caller who presses 1 on hearing the option adds about
three seconds, one who listens through adds twelve, and her line then rings for
five to twenty-five more. At 57 a genuine 45-second conversation answered
quickly stops counting.

`/api/voice/complete` logs the real conversation length next to the call Google
is timing. After a week of live calls, set the threshold from that comparison:
`--threshold 55`, or whatever the data says. Until then it stays at 45, which
errs toward counting a slightly short call — the cheaper mistake.

Also expect the baseline to move for a mechanical reason: Twilio answers every
call, so calls that used to log as MISSED will now log as connected-but-short.
Do not compare next week's duration bands to the 46% figure.

## Open questions for Leslie

- **After hours.** She asked whether calls outside 9am–7pm should ring her
  anyway. Default today is yes, they ring. Recommendation: keep it that way. A
  caller at 8pm has a ticket and a deadline, and the alternative is losing a
  lead we already paid for.
- ~~Does `647 794 7750` ring her cell directly?~~ **Answered Aug 25 (Kushagra):
  it is her own number.** So the chain is Google → Twilio → her cell, one hop,
  no CallRail in the path and no risk of the caller ID being rewritten. Safe to
  use as `TWILIO_FORWARD_TO`.

## Known gap: this screens ad calls, not website taps

The screening sits in front of the **call assets** — the call button in her ads.
It does not cover someone who lands on blottman.ca and taps the number on the
page, because that number is her cell and Google's website call-conversion swap
forwards to whatever the page shows.

That gap is not theoretical. The Aug-13 diagnosis found a second pool of junk
calls coming exactly that way: near-zero-intent Display and Discover taps that
landed on the site and tapped the displayed phone number, 24 events in 14 days,
invisible to call reporting. PMAX now points at blottman.ca, so that pool moved
with it.

Closing it means making the Twilio number the number the site displays
(`PHONE_DISPLAY` / `PHONE_TEL` in `lib/content.ts`). Worth doing for the same
reason as everything else here, but it is a business decision, not a technical
one — it changes the number on her public website, and anything printed
elsewhere would eventually want to match. Raise it with Leslie rather than
just shipping it.
