# Changelog

All notable changes to the MailerCloud Design System. Versions follow [semantic versioning](https://semver.org).

## 3.1.0
Consistency pass: the system now enforces itself.

- **The deck kit reads `tokens/tokens.json`.** It used to restate every colour, shadow, type size, radius and spacing step as a Python literal, so a token change reached no deck. It now loads the token file and holds no value of its own.
- **`scripts/check_usage.py`** (new, in CI) fails the build when a component preview or the deck kit writes a colour, type size, radius or spacing step as a literal instead of referencing a token.
- **`scripts/check_contrast.py --coverage`** (new, in CI) fails when a ground has no approved pair. `bg-yellow` had none; nor did `ink-muted` on `surface-zebra` or `surface-tint`.
- **The contrast matrix in `docs/foundations/accessibility.md` is generated** from `scripts/contrast_pairs.json`, so it cannot drift from the values CI checks. It had a duplicate row.
- **The deck kit's lint** now also checks the type, radius and spacing scales, that grounds alternate, that every content slide has an eyebrow, and that no pinned box crosses the content line.
- **Component previews are drawn at slide scale** and use the `.t-*` classes and `var(--space-*)`. They were miniatures with 8–21px type, below the system's own 24px floor, and used no spacing or type token at all. They also gained `<meta charset>`, which is why `·` rendered as `Â·` when a preview was opened on its own.
- **The report scale is tokenised** as `r-title` to `r-kpi-label`; it previously existed only as prose. `r-body` is 10pt, closing the 9.5pt accessibility gap.
- **The DTCG export gained the type scale** as composite `typography` tokens; the README's claim that it held "the same tokens" was not true before.
- **New tokens** for values that were hidden in the deck kit: `slate-light` / `text-inverse-muted` (secondary text on navy), `line-soft` / `border-hairline` (open-row rules on a pastel ground), `surface-card-soft` (the flow-diagram lane wash), `space-6` (48px), `space-7` (56px), `space-pill-y`, `space-pill-x`.
- **Removed:** the boxed `table()` helper, dead since 3.0 replaced tables with open rows, and the two undocumented zebra colours that only it used. The footer's section-label slot, also dead since 3.0, is gone from the code.
- **`focus-ring` is deprecated.** Nothing consumes it; this system ships documents, not interfaces.
- Visible changes when a deck is rebuilt: open-row body text moves 28px → 26px (28 was off the scale), the cover pill moves to `t-lead` with token padding, and a few radii snap to the scale (30px and 36px pills → `radius-pill`, 24px banner → `radius-card`). No layout rule changed.
- Fixes: the logo guidance said the logo sits 44px from the top where the token says 56px; the SlideFrame doc still described 3.0's removed three-part footer and had a malformed bold; the CodeCard doc's padding did not match the kit, and the kit's method pill used an untokenised green instead of `positive-bg`; the deck pattern doc pointed at the README for a section that lives in the brand book; the Stat preview showed the superseded 95% retention figure instead of 98%.

## 3.0.0
The air direction. Client-name eyebrow on every slide; title block at 152px; content centred with at least 60px of air; open layouts (columns, hairline rows) instead of boxed tables; two-part footer; the 2.1 fill rule is withdrawn; data flow trimmed to five steps. Major because slides already sent look different. First release of this repository.

## 2.1
Content-fill rule (content reaches the footer safe line); slide recipes for stretched rows, padded tables, numeric cards, mini flows and timeline rows. Withdrawn in 3.0.

## 2.0
Semantic and component token tiers; chart palette; accessibility, data visualisation, governance and deck-blueprint pages; DiagramNode, BarChart and SlideFrame components; action-title rule; three-part slide footer with a section label.

## 1.2
Spacing and layout rules; `space-logo-top`, `space-footer`, `space-card-tight`.

## 1.1
Aligned to the brand guide: official palette, behaviour colours, Neutrif Pro stack, logo rules, approved proof points.

## 1.0
First release from the company overview, a client deck and a delivery report.
