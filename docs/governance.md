# Governance

## Ownership

The system is owned by Technical Operations at MailerCloud (Director of Technical Operations). Anyone building a customer document may propose a change; the owner approves it.

## Token architecture

Three tiers, each referring only to the tier above it:

1. **Primitive.** Raw values with a descriptive name: `ink`, `navy`, `brand-blue`, `bg-sky`, `space-4`, `radius-card`.
2. **Semantic.** A role, not a value: `text-primary`, `text-secondary`, `text-inverse`, `surface-page`, `surface-raised`, `surface-inverse`, `border-subtle`, `border-strong`, `action-primary`, `focus-ring`, `status-*`.
3. **Component.** A decision for one component: `card-bg`, `card-inverse-bg`, `table-header-bg`, `table-row-alt-bg`, `node-line`, `node-inverse-bg`.

Documents and components use semantic or component tokens wherever one exists, and a primitive only for decoration (the pastel grounds, the cover circles). Changing a primitive changes the brand; changing a semantic or component token changes one decision.

Naming: lowercase, hyphen-separated, role first (`text-`, `surface-`, `border-`, `status-`, `chart-`), no numbers in semantic names.

## Versioning

Semantic versioning on the whole system: patch for a corrected value or wording, minor for a new token, component or pattern, major for a change that alters the look of documents already sent. The version is in `tokens.json`; each release has a changelog line below.

## Changing the system

1. Propose the change with the document that needs it.
2. Check it against the accessibility matrix and the brand guide.
3. Update the token, the README or the component guidance, and the changelog, in one change.
4. Rebuild one existing document from the system to prove nothing else moved.

A token is deprecated for one release before removal: the usage note says what replaces it.

## Pre-send checklist for any customer document

- Palette, type and logo come from the system; the logo has clear space and sits on a light or pastel ground.
- Titles follow the rule for their slide type; no line breaks inside a number.
- Contrast pairs are from the matrix; nothing is under the size floor.
- Numbers have units, sources and one digit-grouping convention.
- Client name, dates and figures checked against the client's own words.

## Adoption

Documents built with this system: the client solution deck (18 slides, built from the deck kit) and the daily delivery report (A4).

## Changelog

- **3.0** (24 Sep 2026): the air direction. Client-name eyebrow on every slide; title block at 152px; content centred with at least 60px of air; open layouts (columns, hairline rows) instead of boxed tables; two-part footer; the 2.1 fill rule is withdrawn; data flow trimmed to five steps. Major because slides already sent look different.
- **2.1** (24 Sep 2026): content-fill rule (content reaches the footer safe line); slide recipes for stretched rows, padded tables, numeric cards, mini flows and timeline rows.
- **2.0** (24 Sep 2026): semantic and component token tiers; chart palette; accessibility, data visualisation, governance and deck-blueprint pages; DiagramNode, BarChart and SlideFrame components; action-title rule; three-part slide footer with a section label.
- **1.2**: spacing and layout rules; `space-logo-top`, `space-footer`, `space-card-tight`.
- **1.1**: aligned to the brand guide: official palette, behaviour colours, Neutrif Pro stack, logo rules, approved proof points.
- **1.0**: first release from the company overview, a client deck and a delivery report.
