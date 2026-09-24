The Card is the basic content container: a `surface-card` panel with `radius-card` corners and a hard offset shadow that sits on a pastel ground.

- **Light card:** fill `surface-card`, text `ink`, shadow `shadow-card`. Use for most content.
- **Dark card:** fill `navy`, text `surface-card`, shadow `shadow-card-dark`. Use once per slide for the point to remember (next steps, the new route, an API example).
- Padding is `space-4` when the slide is dense and `space-5` when it is sparse. Cards side by side are `space-4` apart; stacked cards are `space-3` apart.
- Heading uses `t-heading` (40px, bold); body uses `t-lead` in sparse cards and `t-body` in dense ones. Do not put more than about five lines of body in one card; split the slide instead.
- The consumer provides the heading and the body text. Do not add a left border stripe or a gradient.
