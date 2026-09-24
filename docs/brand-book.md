# MailerCloud

The design system for every MailerCloud document: sales decks, client reports, proposals and one-pagers. It follows the official brand guide, and adds the pastel colour-first look used in MailerCloud's marketing collateral.

## What this was built from

- **Brand guide** (`Brand-guide-mailercloud.pdf`) and the **Brand Assets** page on mailercloud.com: name, logo, colour codes, typeface. This is the authority where it speaks.
- **The company overview PDF**: pastel full-bleed backgrounds, large bold titles, white cards, the dark API code card.
- **The mailercloud.com homepage** (checked 24 Sep 2026): current proof-point figures and certifications.
- **MailerCloud's client solution deck** and **daily delivery report** (A4 PDF), both built to this look.

Not yet built: product UI components, the flat illustration set, a dark theme. Nothing here is invented beyond these sources; where a rule comes from a document we built rather than from the brand guide, the section says so.

## Official brand foundations

| Element | Official rule (brand guide) | Status here |
| --- | --- | --- |
| Name | "mailercloud" is one word, written in lowercase in the logo (small "m" and "c"), with a cloud icon. The website writes "Mailercloud" in running text. | Existing documents write "MailerCloud". Decision pending, see Known gaps. |
| Primary colour | `#046DFF` | `brand-blue` |
| Secondary colours | `#020A13`, `#091929`, `#22364C`, `#7D8E9F` | `ink`, `navy`, `ink-muted`, `slate` |
| Behaviour colours | Success `#16DB93`, Error `#E63946`, Warning `#FFC300`, Information `#B6D7FF` | `success`, `error`, `warning`, `info` |
| Typeface | Neutrif Pro: Regular, Semi Bold, Bold | Poppins stands in until licensed Neutrif Pro files are added |
| Logo | Standard, icon-only and dark-mode versions, in `mailercloud-assets.zip` | Standard logo only; see `assets/Logos` |

The four behaviour colours are matched to their names by meaning (green success, red error, amber warning, light blue information), because the guide lists names and hex codes in separate blocks.

The pastel grounds (`bg-sky`, `bg-lime`, `bg-mint`, `bg-green`, `bg-pink`, `bg-cream`, `bg-yellow`) come from the company overview, not the brand guide. They are the marketing look for decks and covers; reports and product-facing documents stay on the official palette.

## Principles

1. **One message per page.** A slide or report page makes one point; the title states the topic, the body proves it.
2. **Colour carries the brand.** Decks sit on full-bleed pastel grounds. Reports stay on a near-white page and use the official palette, with pastels in small doses.
3. **White cards, hard shadows.** Content sits on `surface-card` cards with `radius-card` corners and a hard offset shadow (`shadow-card`), never a blurred one.
4. **Numbers first, in plain words.** Lead with the figure and its unit, then one sentence of meaning.
5. **Colour never says it alone.** A highlighted row or card also carries a text label ("Worth a closer look", "Third day running").
6. **Air over ink.** A slide should feel spacious. One idea, few elements, generous margins, and the client's name on every page so the reader knows it is theirs.

## Where to look

| You need | Go to |
| --- | --- |
| Colours, type, spacing, radii, shadows | [`tokens/tokens.json`](../tokens/tokens.json) (three tiers: primitive, semantic, component) and the generated [`dist/tokens.css`](../dist/tokens.css) |
| Which colour pairs are safe | [Accessibility](foundations/accessibility.md) |
| How to draw a chart or a diagram | [Data visualisation](foundations/data-visualisation.md) |
| To build a client deck | [Pattern: client solution deck](patterns/client-solution-deck.md) and the deck kit in [`tools/deck-kit`](../tools/deck-kit) |
| Rules for changing the system, the pre-send checklist, the changelog | [Governance](governance.md) and [`CHANGELOG.md`](../CHANGELOG.md) |
| A building block | Components: [Card](components/Card.md), [Pill](components/Pill.md), [Stat](components/Stat.md), [CodeCard](components/CodeCard.md), [DataTable](components/DataTable.md), [DiagramNode](components/DiagramNode.md), [BarChart](components/BarChart.md), [SlideFrame](components/SlideFrame.md) |

## Content fundamentals

- **Voice:** direct, plain, present tense. British spelling (London HQ): "authorises", "centres", "programme".
- **Every content slide carries an eyebrow** above the title: the client name and the section ("Client Name · Design"), in 24px uppercase. It tells the reader whose document this is and where they are.
- **Titles:** at most 40 characters, so they stay on one line at 64px. Argument slides use an action title, a claim the slide then proves ("Inbound stays put, outbound moves"); reference slides may use a noun phrase ("Security and compliance"). No questions, no exclamation marks, no emoji.
- **Numbers:** always with the unit ("30,000 replies a day", "96.46% delivered"). Ranges use an en dash ("10–20%"). State assumptions next to the figure ("about 63 a minute across an 8-hour support day").
- **Digit grouping follows the reader.** India-facing operational reports use lakh grouping (30,39,776); global material uses 3,039,776. Do not mix within one document.
- **Third-party claims get a source line** ("Source: Microsoft Exchange Online sending limits"). Never invent a statistic or a quote; use a bracketed placeholder such as `[€__]` instead.
- **Recommendations are labelled** "Suggested action" or "Suggested next steps", and phrased as offers unless a commitment was made.

### Approved proof points

Use these figures as published on mailercloud.com (homepage, checked 24 Sep 2026). Re-check the page before each new document; the company overview PDF is older and differs on retention.

| Claim | Figure |
| --- | --- |
| Emails delivered every month | 6 Billion+ |
| Monthly campaigns | 50K+ |
| Client retention | 98% (the overview PDF says 95%) |
| Opens | 900 Million+ |
| Businesses | 35,000+ |
| Security and compliance | ISO/IEC 27001:2022, GDPR compliant, VAPT certified |
| Free plan | Free forever, 12,000 emails a month |

Case studies (Turtle, RedBus) come from the company overview and keep their own wording of the result.

## Visual foundations

### Documents at a glance

| Document | Format | Ground | Type | Chrome |
| --- | --- | --- | --- | --- |
| Deck | 1920 × 1080 slides | One `bg-*` pastel per slide; alternate, never the same ground twice in a row; `bg-paper` for text-heavy slides | Slide scale below | Logo top-left at 128px from the left and `space-logo-top` (56px) from the top, 220 × 45px; an eyebrow line ("Client · Section") above every title; two-part footer, 24px `ink-muted`, `space-footer` (64px) from the bottom: `www.mailercloud.com` left, `05 / 18` right |
| Report | A4 portrait | White page, `bg-paper` allowed | Report scale below | Header: logo left, title and date right, 1.6pt `brand-blue` rule; footer: hairline in `line`, "MailerCloud \| www.mailercloud.com \| Confidential: prepared for [client]", "Page x of y" |
| Proposal | A4 portrait | White page | Report scale | Same header and footer as a report; cover with the client name in the largest size |

### Colour use

- Text is `ink` on every light surface and `surface-card` (or white) on `navy`. Secondary text is `ink-muted`. `slate` is for rules, icons and chart neutrals, never text.
- `navy` is for dark cards, the MailerCloud node in a diagram, emphasis pills and report table headers.
- `brand-blue` is the primary colour: the logo cloud, the report header rule, links, the one highlighted chart bar and the new-route arrows. Use it on cream, lime, paper or white grounds; on `bg-sky` its contrast is only 2.1:1, so use `navy` there.
- Status uses the behaviour colours: `success`, `warning`, `error`, `info`. Report panels use their soft tints (`attention-bg` with `attention-ink`, `positive-bg` with `positive-ink`). Always add words.
- One pastel ground per slide. Two pastels may share a slide only as card fills on a `bg-paper` ground (see the security slide).

### Type

The official face is Neutrif Pro (Regular, Semi Bold, Bold). Poppins stands in everywhere until licensed Neutrif Pro files are available; the token font stack already lists Neutrif Pro first, so switching needs only the font files. JetBrains Mono carries code.

Slide scale (px, 1920 × 1080): `t-display` 88, `t-title` 64, `t-heading` 40, `t-lead` 32, `t-body` 26, `t-label` 24 (the floor). Emphasise with weight or colour, not a new size.

Report scale (pt, A4): document title 26 bold; section heading 14 bold; sub-heading 10.5 bold; body 9.5 on 13.5 leading; table text 8.8; footnotes 8.3; KPI figure 19 bold with a 7.6 bold uppercase label.

### Shape, cards and shadows

- Cards: `surface-card`, `radius-card`, `shadow-card` on pastel grounds; padding `space-4` (dense) or `space-5` (sparse); `space-4` between side-by-side cards.
- Pills: `radius-pill`, `t-label` weight 600, padding 6–8px by 18–22px; fill `bg-lime`, `bg-sky`, `bg-green` or `navy` (with `bg-lime` text).
- Decorative circles (`radius-round`) in `bg-lime`, `bg-green` and `surface-card` sit off the text column on covers, as on the company overview.
- One deliberate hard shadow per object; no blur, no gradients, no glows.

### Spacing and layout

Reviewed on a built client deck three times on 24 Sep 2026. The second pass filled every slide to the footer and the deck then felt crowded; the third pass replaced that rule with the air rule below.

**Slides (1920 × 1080)**

| Rule | Value |
| --- | --- |
| Side margins | `space-margin` (128px) left and right |
| Logo | 128px from the left, `space-logo-top` (56px) from the top, 220 × 45px |
| Title block | Starts `space-title-top` (152px) from the top: eyebrow (24px, uppercase, 2px tracking, `text-secondary`), 8px gap, title (64px). A 32px subtitle only where it earns its place |
| Content area | From 32px under the title block down to y 880 (`space-content-bottom` 200px). The footer band below stays clear |
| Between blocks | 48px between columns; 24–32px between cards; 56px between a column group and a banner |
| Card padding | `space-card-tight` (28px) for five across; `space-4` (32px) for grids; `space-5` (40px) for two-up cards |
| Inside a card | 12–20px between pill, heading, chips and text |
| Footer | `space-footer` (64px) from the bottom; one 24px row, url left and `05 / 18` right |

**Air over ink**

- The content group is centred vertically in the content area. It should occupy at most about 65% of it, with at least 60px above and below.
- One idea per slide: at most 3 columns, 5 list rows or 6 tiles, and about 60 words of body copy.
- Body text 32px where it fits; 26px only in tiles and captions. Write copy to fit one line per list row.
- Prefer open layouts to boxes: columns with a 4px top rule, rows with hairline rules, a soft highlighted row. Boxed tables and stacks of cards are the exception.
- One focal element per slide: at most one dark card or banner.
- Do not stretch cards or rows to reach the footer. If a slide looks empty, cut words or enlarge type within the scale; do not add boxes.
- Do not let a number split across a line ("8-hour" at a line end): rephrase.

**Recipes**

- *Table* becomes open rows: uppercase 24px labels, hairline rules (`border-subtle`), first column bold, and the "no change" row as a soft `positive-bg` panel.
- *Row of cards* becomes columns with a numeral, heading and 32px text, or two cards with one dark card as the focal point.
- *Timeline* becomes rows: a pill for the time, a bold phase name, one line of text.
- *Grid of tiles*: heading and two lines at most; icon beside the heading, not above it.
- *Big numbers* (64px) lead a column when a figure is the point.

### Diagrams

- Nodes are cards: `surface-card`, 3px `ink` border, `radius-card`, `shadow-small`. The MailerCloud node is `navy` with light text.
- Existing paths are 4px `ink` lines; the new MailerCloud route is 6px `navy` or `brand-blue`. Dashed means feedback (status webhooks).
- Every step is numbered in its caption; labels are at least 24px and sit clear of the lines. Keep a data-flow diagram to five steps or fewer.
- Lane labels are uppercase pills: `surface-card` for "unchanged", `navy` with `bg-lime` text for "new".

### Charts

- Bars use `navy`; the previous period or comparison is `chart-grey`; the one bar to notice is `brand-blue`; a residual segment is `chart-light`.
- Label values directly on the bars; no gridline clutter; axis text `ink-muted`.
- Title the chart with what it compares ("Blocks by receiving servers, 22 vs 23 Sep") and add one sentence underneath.

## Logo and iconography

See `assets/Logos` for the logo and its rules. Icons are simple line glyphs, 40–56px, `navy` on a `surface-card` circle. No emoji, no icon fonts with mixed styles.

## Components

Card, Pill, Stat, CodeCard, DataTable, DiagramNode, BarChart and SlideFrame are the recurring building blocks. Each has a live preview and a short guideline.

## Used in

- The client solution deck (18 slides), built from the deck kit in `tools/deck-kit`.
- The daily delivery report (A4 PDF), issued on the type stack above.

## Known gaps and decisions

1. **Typeface:** documents use Poppins, not the official Neutrif Pro. Needs licensed Neutrif Pro files (Regular, Semi Bold, Bold).
2. **Name casing:** the guide writes "mailercloud" (one lowercase word); the website writes "Mailercloud" in text; our documents write "MailerCloud", which matches neither. Recommendation: "Mailercloud" in running text, the logo for the wordmark. Needs a decision before documents are changed.
3. **Logo variants:** the official dark-mode logo, icon-only logo and SVG are in `mailercloud-assets.zip` but not yet in this system, so the logo cannot go on `navy` grounds.
4. **Pastel palette:** it is in the company overview, not the brand guide. Confirm with the brand owner that it is approved for customer documents.
5. **Retention figure:** 98% on the website, 95% in the company overview.
6. **Proposal template:** still set in Helvetica; should move to the type stack above, tinted panels and a 10pt body.
7. **Accessibility:** brand-blue is 4.4:1 on white; report PDFs are untagged. See Accessibility.
8. **No shipped code library:** components are documented and previewed, and the deck kit generates slides, but there is no React or CSS package yet.
9. **No icon set of our own:** decks use the slide editor's built-in glyphs; the product icons on mailercloud.com are not in this system.
10. **No photography or illustration guidance:** the overview uses flat character illustrations; they are not included.
