# MailerCloud Design System

The shared design system for every MailerCloud document and interface we build for customers: client decks, reports, proposals and one-pagers. Colour-first, one message per page, official brand palette and type.

**Version 3.1.0** · [Changelog](CHANGELOG.md) · [Contributing](CONTRIBUTING.md)

## Start here

| I want to | Go to |
| --- | --- |
| See the colours, type, spacing and components | Open [`index.html`](index.html) in a browser (or enable GitHub Pages on this repository) |
| Read the brand book and layout rules | [`docs/brand-book.md`](docs/brand-book.md) |
| Pick colours that pass accessibility | [`docs/foundations/accessibility.md`](docs/foundations/accessibility.md) |
| Draw a chart or a diagram | [`docs/foundations/data-visualisation.md`](docs/foundations/data-visualisation.md) |
| Build a client solution deck | [`docs/patterns/client-solution-deck.md`](docs/patterns/client-solution-deck.md) and [`tools/deck-kit`](tools/deck-kit) |
| Use a component | [`docs/components/`](docs/components) and [`components/`](components) (live previews) |
| Propose a change | [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`docs/governance.md`](docs/governance.md) |

## Use the tokens

`tokens/tokens.json` is the single source of truth. Everything else is generated from it:

- `dist/tokens.css`: CSS custom properties (`var(--brand-blue)`, `var(--space-4)`, `var(--radius-card)`), the slide type classes (`.t-title`, `.t-body`) and the report type classes (`.r-body`, `.r-kpi`).
- `dist/tokens.dtcg.json`: the same tokens in the W3C Design Tokens format — colour, spacing, radius, shadow, font families and the type scale as composite `typography` tokens — for Style Dictionary, Tokens Studio and other tools.

```html
<link rel="stylesheet" href="dist/tokens.css">
<div style="background: var(--surface-raised); color: var(--text-primary); border-radius: var(--radius-card); box-shadow: var(--shadow-card); padding: var(--space-5)">
  Use semantic tokens (<code>text-*</code>, <code>surface-*</code>, <code>status-*</code>) wherever one exists.
</div>
```

After editing `tokens/tokens.json`, regenerate and check:

```bash
python scripts/build_tokens.py              # rewrites dist/ and index.html
python scripts/check_contrast.py            # every approved colour pair must pass
python scripts/check_contrast.py --coverage # every ground has a pair
python scripts/check_usage.py               # consumers reference tokens, never restate them
```

CI runs all four, plus the deck kit and its lint, on every push and pull request. Nothing that builds a document — the component previews or the deck kit — may write a colour, type size, radius or spacing step as a literal; `check_usage.py` fails the build if one does.

## Repository layout

```
tokens/                 tokens.json (source of truth)
dist/                   generated: tokens.css, tokens.dtcg.json
docs/                   brand book, foundations, patterns, governance, component guidance
components/             live HTML previews for each component and the cover
assets/logos/           the logo and its usage rules
tools/deck-kit/         builds the 18-slide client solution deck from a JSON config
scripts/                token build, contrast check, usage check, approved colour pairs
index.html              generated overview of the whole system
```

## Brand notice

The MailerCloud name, logo and brand assets are owned by MailerCloud and are subject to the brand guidelines at <https://www.mailercloud.com/brand-assets>. This repository does not grant permission to use them outside those guidelines. The repository owner should add a `LICENSE` file for the code and documentation before wider sharing.

## Known gaps

The current gaps (official Neutrif Pro font files, dark-mode logo, name casing, and others) are listed at the end of [`docs/brand-book.md`](docs/brand-book.md). Do not commit client names, client figures or customer decks to this public repository; keep those in private repositories.
