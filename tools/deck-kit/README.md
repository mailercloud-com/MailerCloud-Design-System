# Deck kit: client solution deck

Builds an 18-slide customer deck from one JSON config, using the MailerCloud design system tokens. The pattern is "move one-to-one or transactional outbound mail off a general-purpose mailbox and onto MailerCloud SMTP or the Email API, while inbound stays where it is". See `docs/patterns/client-solution-deck.md` for the slide sequence.

## Files

- `build_deck.py`: the builder. Python 3, standard library only.
- `config.example.json`: a fictional example client. Copy it for a real client.

## Build a deck for a new client

1. Copy `config.example.json` to `config.<client>.json` (keep client configs out of this public repository).
2. Change the client name and domain, the meeting and date, the volume and support window, the provider and its published limits (with a source line), the three `situation_cards` (a big number, its label and one sentence each; the last may have no number), and the two sentences `outcome_text` and `ask`.
3. Set `ramp`, `rollout`, `risks`, `decisions`, `next_steps`, `proof_stats` and `cases`. Re-check the proof figures against mailercloud.com, and use only approved case studies.
4. Run `python build_deck.py config.<client>.json out --logo /_blob/<logo asset id>`. The logo asset id is the id of `mailercloud-logo.png` in the Slides artifact you publish to (upload `assets/logos/mailercloud-logo.png` first).
5. Publish `out/project/deck.json` and `out/project/slides/*.html`. The output is the file format of the Slides artifact in Claude (one HTML section per slide on a 1920 × 1080 canvas); publish it there, or adapt the builder to your own slide tool.
6. Page through the deck. The lint cannot see a long client name or a wrapped title.

## What the lint checks

Nothing below 24px, titles at most 40 characters (override with `situation_title` where the use-case wording is long), one section per slide, pinned boxes inside the 1920 × 1080 canvas, no pure black or white, speaker notes on every slide. It exits with an error if any check fails.

## Design rules the builder follows

Every content slide gets an eyebrow with the client name and the section, and its content is centred with generous air (open columns and hairline rows, not boxed tables). Write copy to fit: one line per list row, about 60 words a slide. Keep risks to five rows and rollout phases to five.

## Limits

- Built for one pattern. Campaign or inbound migrations need a different sequence.
- The provider's limits are inputs, not looked up. Cite a current source for every client.
- SMTP host, port and API authentication details are not in the deck; add them from MailerCloud's API documentation once confirmed.
