The DataTable lays out account or record data in a report or slide: a `navy` header, zebra rows and highlighted attention rows.

- Header: `table-header-bg` fill, `text-inverse` bold text at `r-footnote` (reports) or `t-label` (slides). Never pure white. Numeric columns are right-aligned, text columns left-aligned.
- Rows: alternate `bg-paper` (or white) and `surface-zebra`; rules in `line`. First column is bold `ink`.
- Attention rows use `attention-bg`, with the value that triggered it in bold `attention-ink`. Add a footnote saying what the highlight means, and a "Note" column when a status needs words ("Third day running").
- The Note column pairs a `status-*` dot with the word: `status-success` healthy, `status-info` warming, `status-warning` worth watching, `status-error` failing. The dot never carries the meaning alone.
- On slides keep to five columns or fewer and about six rows; each column at least as wide as its longest word.
- The consumer provides the columns and rows. Percentages are computed from the counts shown; check them before publishing.
