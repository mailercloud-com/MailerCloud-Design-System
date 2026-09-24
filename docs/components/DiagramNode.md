The DiagramNode is a card used as a box in an architecture or flow diagram, with connectors, numbered captions and lane labels around it.

**Anatomy:** node (icon, title, one or two lines of text), connector with arrowhead, caption with a step number, lane label.

**Variants**
- Standard node: `card-bg` fill, 3px `node-line` outline, `radius-card`, `shadow-small`.
- Inverse node: `node-inverse-bg` fill and light text; used once per diagram for the MailerCloud node.
- Lane label: an uppercase Pill above the node; `surface-raised` for "unchanged", `navy` with `bg-lime` text for "new".

**Rules**
- Same kind of thing, same size; at least 32px between nodes; a grid, not a scatter.
- Existing paths are 4px `border-strong`; the new route is 6px `navy` or `brand-blue`; dashed means feedback.
- Captions carry a step number, sit at least 8px from a line and never on it.
- Icons sit top-left, 44 to 56px.

**Don't:** run a connector through a node, join a parent's bottom edge to a child's top edge with an elbow, or shrink text below 24px to fit a box (use fewer columns instead).

The consumer provides the labels and the coordinates. Coordinates and connector routing are in the deck kit.
