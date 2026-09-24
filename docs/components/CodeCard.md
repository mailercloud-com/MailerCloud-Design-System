The CodeCard is the navy panel that shows an API request and its response, as on the Email API page of the company overview.

- Fill `navy`, corners `radius-card`, shadow `shadow-card-dark`, padding `space-4` vertical and `space-5` horizontal. Set the code in JetBrains Mono at `t-code` (24px on slides).
- Top row: a `positive-bg` method pill (POST) with `positive-ink` text and `radius-tile` corners, and the endpoint in `code-text`. Then a `navy-line` rule, the payload, another rule, and the response row (`200 OK` pill and "Email accepted"). Secondary text on the card is `text-inverse-muted`.
- Colour the payload with `code-key` for keys, `code-string` for string values and `code-text` for punctuation. Nothing else.
- Use real endpoints and field names from the product documentation; label made-up values (sender address, customer email, message ID) as illustrative in the speaker notes or a caption.
- One card per slide, beside a short explanation on the left. The consumer provides the payload.
