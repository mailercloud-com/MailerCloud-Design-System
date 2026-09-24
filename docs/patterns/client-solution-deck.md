# Pattern: client solution deck

A repeatable deck for a client who needs to move a class of outbound email (support replies, order confirmations, alerts, one-to-one mail) off a general-purpose mailbox and onto MailerCloud SMTP or the Email API. First used for a support-email migration off Microsoft 365.

Built by the deck kit (`build_deck.py` plus a client config). The kit reads the tokens in this system, so a design change here reaches every deck the next time it is built.

## When to use it

Use it when: the client sends one-to-one or transactional mail at volume; the current provider throttles or blocks it; a helpdesk or application can send by SMTP or API; the client keeps its inbound mail where it is.

Do not use it for campaign or marketing migrations (different flow: lists, consent, templates) or for clients moving inbound mail.

## The sequence (18 slides)

| # | Slide | Job | Title rule |
| --- | --- | --- | --- |
| 1 | Cover | Name the client and the outcome | Outcome with the number |
| 2 | Executive summary | Problem, solution, outcome and the ask on one slide | Action title with the volume |
| 3 | Why it is blocked | The constraint, with a source | "Why [use case] get blocked today" |
| 4 | Approach | Inbound stays, outbound moves | Short claim |
| 5 | Architecture | The loop, with lanes | Claim, then a subtitle |
| 6 | Data flow | Five numbered steps and what moves | Claim |
| 7 | Integration | SMTP relay vs Email API, with a real payload | Noun phrase |
| 8 | Authentication | The DNS records, MX unchanged | Claim |
| 9 | Capacity and IP | Volume against the limit; shared pool vs dedicated | Noun phrase |
| 10 | Ramp | The daily volume plan | Outcome with the number |
| 11 | Control | Logs, webhooks, suppression, retries, tracking | Claim |
| 12 | Rollout | Five phases and the cut-over banner | Outcome |
| 13 | Risks | Five risks, each with a response | Noun phrase |
| 14 | Proof | Current figures and two case studies | Noun phrase |
| 15 | Security | Six points IT will ask about | Noun phrase |
| 16 | Decisions and next steps | What to agree today, what happens tomorrow | Noun phrase |
| 17 | Appendix | Glossary and assumptions | Noun phrase |
| 18 | Closing | Restate the outcome, offices | "Thank you" |

Every content slide carries an eyebrow with the client name and section, and its content is centred with generous air (see Spacing and layout in the README). The builder writes open layouts, not boxed tables.

Titles are at most 40 characters so they stay on one line at 64px. Argument slides use action titles (a claim); reference slides may use a noun phrase.

## Variables (client config)

Client name and domain; meeting type and date; use case ("support replies"); volume per day and the support window in hours; current provider, its limits and their source; inbound system and note; workspace name; the three situation cards (big number, label, text); the ramp values; rollout phases; risks; decisions and next steps; proof figures and case studies. Everything else, including layout, colour and spacing, comes from the tokens.

## How to reproduce it for a new client

1. Copy `tools/deck-kit/config.example.json`, change the client, provider and volume, and rewrite the five use-case sentences (today, constraint, goal, outcome, ask).
2. If the provider is not Microsoft 365, replace the limits and the source line with the provider's published limits and check that the source is current.
3. Set the ramp to what the client's existing sending history supports.
4. Run `python tools/deck-kit/build_deck.py config.<client>.json out --logo /_blob/<logo asset id>`. The lint must be clean.
5. Publish the output (one HTML file per slide plus `deck.json`, the file format of the Slides artifact in Claude), page through it, and fix anything the lint cannot see (a long client name, a title that wraps).

## Pre-flight before sending

- Every figure has a source or a stated assumption; proof figures re-checked against mailercloud.com the same day.
- The DNS, sending-domain and IP questions are on the decisions slide.
- Notes present on every slide; appendix left out of the live walk-through.
- Client name spelled as the client spells it, on the cover, in the closing and in the deck title.
