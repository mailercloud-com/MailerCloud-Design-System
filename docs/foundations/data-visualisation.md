# Data visualisation

Charts and diagrams exist to make one point quickly. Each has a title that says what it compares and a sentence underneath that says what to notice.

## Choosing the form

| The reader needs to see | Use |
| --- | --- |
| How values compare at one moment | Horizontal bars, sorted by value |
| How one value changes over days or weeks | Vertical bars for a few steps (a ramp), a line for many points |
| What a total is made of | One stacked bar with direct labels; never a pie |
| Where a number sits against a limit | Two bars on one scale, the limit in `chart-3` |
| How a system moves data | A diagram: cards for nodes, connectors for flow, numbered steps |

## Colour

- Default bar `chart-1` (`navy`); the one bar to notice `chart-2` (`brand-blue`); comparison or previous period `chart-3` (`slate`); a residual "all other" segment `chart-light`.
- Categorical series follow `chart-1` to `chart-5` in order. `chart-4` and `chart-5` are close in lightness: label them directly.
- Never encode meaning in colour alone; every mark carries a value label or a word.

## Labelling and axes

- Label values on the marks. Drop gridlines unless the reader must read across; if kept, use `border-subtle`.
- Start bar axes at zero. Axis and label text is `text-secondary`, 24px or larger on slides.
- Use thousands separators that match the document's digit-grouping rule (lakh or western), and units on every figure ("30K a day", "63 a minute").
- A comparison that uses an assumption states it in the caption ("about 63 a minute across a support day of 8 hours").
- Cite third-party data in a source line under the chart.

## Diagrams

- Nodes are DiagramNode cards on a grid: same-size boxes for the same kind of thing, at least 32px apart.
- Existing paths are 4px `border-strong` lines; the new MailerCloud route is 6px `navy` or `brand-blue`; dashed means feedback.
- Number every step in its caption and keep captions at least 8px from any line.
- A lane label names each path ("Inbound · No change", "Outbound · Via MailerCloud").
