# Accessibility

The floor for every customer-facing document is WCAG 2.2 AA. This page records what the system guarantees, what it does not yet, and how to check.

## Rules

- **Text size.** Slides: nothing under 24px at 1920 × 1080; body copy 26px or larger. Reports: body 10pt or larger, footnotes 8.3pt at the very least.
- **Contrast.** Body text 4.5:1, large text (24px bold or 32px and up) 3:1, graphics and chart marks 3:1. The matrix below is the source of truth; pick pairs from it.
- **Colour never says it alone.** Status, highlight and series colours always come with a word, a value label or a position: "Worth a closer look", "Third day running", "30K" on the bar.
- **Series differ in lightness, not hue alone.** Where two chart colours are close in lightness (`chart-4` and `chart-5`), label the marks directly.
- **Reading order is source order.** In diagrams, number the steps in the caption text and carry each connector's meaning into the node it leads to.
- **Speaker notes carry the argument.** Every slide has notes in full sentences, so a reader who cannot see the diagram still gets the point.
- **Alt text.** The logo has alt text; decorative circles and shapes have none.
- **Motion.** Decks use a fade only. No auto-advance, no build-ins that hide content.
- **Language.** Documents are written in British English and marked en-GB when the format allows.
- **Links** are underlined, because `brand-blue` is 4.4:1 on white.

## Contrast matrix

Ratios are computed from the token values (WCAG relative luminance).

| Foreground | Background | Ratio | Use |
| --- | --- | --- | --- |
| `ink` | `sky` | 9.4:1 | AAA, any text |
| `ink` | `lime` | 15.4:1 | AAA, any text |
| `ink` | `mint` | 11.6:1 | AAA, any text |
| `ink` | `green` | 11.2:1 | AAA, any text |
| `ink` | `pink` | 14.8:1 | AAA, any text |
| `ink` | `cream` | 18.3:1 | AAA, any text |
| `ink` | `yellow` | 16.4:1 | AAA, any text |
| `ink` | `paper` | 19.3:1 | AAA, any text |
| `ink` | `card` | 19.5:1 | AAA, any text |
| `ink` | `zebra` | 18.5:1 | AAA, any text |
| `ink` | `tint` | 17.7:1 | AAA, any text |
| `ink` | `info` | 13.4:1 | AAA, any text |
| `ink` | `warning` | 12.4:1 | AAA, any text |
| `ink` | `success` | 11.0:1 | AAA, any text |
| `ink-muted` | `sky` | 5.9:1 | AA, any text |
| `ink-muted` | `lime` | 9.6:1 | AAA, any text |
| `ink-muted` | `mint` | 7.2:1 | AAA, any text |
| `ink-muted` | `green` | 7.0:1 | AA, any text |
| `ink-muted` | `pink` | 9.2:1 | AAA, any text |
| `ink-muted` | `cream` | 11.3:1 | AAA, any text |
| `ink-muted` | `paper` | 12.0:1 | AAA, any text |
| `ink-muted` | `card` | 12.1:1 | AAA, any text |
| `surface-card` | `navy` | 17.4:1 | AAA, any text |
| `bg-lime` | `navy` | 13.8:1 | AAA, any text |
| `code-key` | `navy` | 8.6:1 | AAA, any text |
| `code-string` | `navy` | 11.5:1 | AAA, any text |
| `code-text` | `navy` | 12.0:1 | AAA, any text |
| `brand-blue` | `card` | 4.4:1 | Large text (24px+ bold or 32px+) and graphics only |
| `brand-blue` | `paper` | 4.4:1 | Large text (24px+ bold or 32px+) and graphics only |
| `brand-blue` | `cream` | 4.2:1 | Large text (24px+ bold or 32px+) and graphics only |
| `brand-blue` | `lime` | 3.5:1 | Large text (24px+ bold or 32px+) and graphics only |
| `brand-blue` | `sky` | 2.1:1 | Fails: do not use for text or graphics |
| `slate` | `surface-card` | 3.3:1 | Large text (24px+ bold or 32px+) and graphics only |
| `white` | `error` | 4.2:1 | Large text (24px+ bold or 32px+) and graphics only |
| `ink` | `error` | 4.8:1 | AA, any text |
| `attention-ink` | `attention-bg` | 6.3:1 | AA, any text |
| `positive-ink` | `positive-bg` | 8.0:1 | AAA, any text |
| `navy` | `bg-sky (arrows, graphics)` | 8.4:1 | AAA, any text |
| `brand-blue` | `bg-cream (graphics)` | 4.2:1 | Large text (24px+ bold or 32px+) and graphics only |

## Known gaps

1. The primary brand blue `#046DFF` is 4.4:1 on white, just under AA for small text. It is the official colour, so use it for the logo, large text and graphics, underline links, and prefer `navy` for small text.
2. The report PDFs are not tagged for screen readers (the generator does not write a tag tree). Provide the same content as the deck or an accessible document on request.
3. Report body text is 9.5pt; move to 10pt at the next issue.

## Checking a document

1. Run the deck kit's lint (font floor, canvas bounds, one section per slide, notes present).
2. Pick every text colour and ground from the matrix above.
3. Page through in presentation mode and read the notes aloud for two slides: if the point is lost, the slide relies on layout alone.
