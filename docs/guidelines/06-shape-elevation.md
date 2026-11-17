# Shape and elevation

Shapes come in three kinds: capsules for controls, fixed radii for containers, and concentric radii for anything nested. Elevation is a layer, not a shadow stack.

## Radii

| Token | Value | For |
|---|---|---|
| `radius-pill` | 999 (capsule) | Buttons, segments and their wells, switches, chips, tags, badges, search fields on touch, floating toolbars |
| `radius-pane` | 20 | Panes, modals, the edge rail, the chat shell's cards and composer |
| `radius-card` | 16 | Cards, popovers, node cards, popover notices |
| `radius-card-quiet` | 14 | Quiet cards, menus |
| `radius-control` | 11 | Text fields, text areas, selects on desktop, large tool tiles, rail tiles |
| `radius-tile` | 6 | Small tiles, menu items, chips inside dense tables; the floor for concentric radii |
| `radius-checkbox` | 5 | Checkboxes |
| `radius-dense` | 3 | Buttons and fields in dense pro-tool panels |
| `radius-state-pill` | 22 | The 44pt menu-bar state pill |
| `radius-window` | 22 | A window the app draws itself (web, Windows, Linux) |
| `radius-sheet` | 28 | The top corners of bottom sheets and the leading corners of side sheets on touch |

Classic (expressive) radii are smaller: pane 16, card 14, quiet card 12, control 8.

## Concentricity

A nested corner shares its parent's center: inner radius = outer radius minus the padding between them, never less than `radius-tile`. Apple calls this concentricity and Material calls it optical roundness; both use the same formula.

| Outer | Padding | Inner |
|---|---|---|
| Pane 20 | `pane-padding` 12 | 8 (a card flush to the pane edge), raised to 16 where the card is the pane's main content |
| Card 16 | `card-padding-x` 14 | 6 (`radius-tile`) for a tile inside the card |
| Modal 20 | 14 body padding | 6 |
| Sheet 28 | 16 | 12 |
| Phone screen (about 55) | `margin-compact` 16 | about 39 for an edge-anchored floating bar |

Where the formula would give a corner that looks pinched (an inner card at 8 inside a pane at 20 with generous content), use the token radius and add padding until the gap reads even; never let an inner corner flare beyond its parent. On Apple, use `ConcentricRectangle` or `containerShape` for shapes anchored to a container or the device edge. On the web and Android, compute `calc(var(--radius-pane) - var(--pane-padding))` with `max()` against `radius-tile`.

All corners on Apple platforms are continuous (squircle). On the web use `border-radius` (circular arcs); the difference is invisible at these sizes.

**Marketing pages** (NDS-45) draw squircles on the web with `corner-shape: squircle` where the browser supports it. A squircle of the same radius cuts the corner about half as deep, so the radii grow to read like the app's, and fall back to circular values elsewhere:

| Marketing radius | Squircle | Circular fallback | For |
|---|---|---|---|
| Check | 7 | 4 | Checkbox, segment, copy icon |
| Tile | 11 | 6 | Tool tiles, tags |
| Control | 18 | 10 | Buttons, the menu button |
| Window | 22 | 12 | Terminal windows |
| Card | 28 | 16 | Plates, notes, callouts, the phone menu |
| Pane | 36 | 20 | The header bar, the CTA panel, the tour frame |

Marketing buttons are rounded rectangles at the control radius, not capsules; app buttons stay capsules. Any alternate app theme keeps the flat squircle radii (NDS-46).

**The Near AI chat composer** uses `radius-pane` 20 rather than `radius-card` 16, so it matches the cards of the chat shell it docks into (NDS-44).

## Shape rules

- Controls are capsules on every platform. Material 3 Expressive's square button shapes and its shape morph on press are allowed on Android and the web only, and only for buttons outside glass chrome.
- Containers never become capsules; a capsule is a control. A refresh control is a capsule pill with its word (NDS-36).
- The 35 Material Expressive shapes (cookies, bursts, pills) are for content-layer hero moments only: an avatar mask, an empty-state illustration, the Android loading indicator. Never for glass chrome, never for status.
- Selected and unselected shapes are the same on Apple; selection changes fill and tint only.

## Elevation

Elevation is the layer an element lives in (see Glass and materials). Only two layers cast shadows.

| Level | Layer | Shadow | z-index (web) |
|---|---|---|---|
| 0 | Scene, page content | none | `z-base` 0 |
| 1 | Panes, bars | `shadow-float` (panes); bars use the scroll-edge treatment instead | `z-base`, `z-sticky` 100 for sticky bars |
| 2 | Painted content inside a pane | none, ever | |
| 3 | Floating: popovers, menus, node cards, floating toolbars, tooltips, popover notices | `shadow-float` | `z-floating` 1000, `z-tooltip` 4000 |
| 4 | Scrims | none | `z-scrim` 2000 |
| 5 | Modals and sheets | `shadow-modal` | `z-modal` 2001 |
| | Toasts | `shadow-float` | `z-toast` 3000 |

`shadow-float` is 0 18 36 at 60% of #02030a in dark and 0 14 30 at 12% black in light; `shadow-modal` is 0 24 60 at 50% (dark) and about 22% (light). Hover never adds a shadow; it replaces the fill. Material's surface tones are rendered here as translucent fills on the pane, and its "+1 on hover" rule becomes the hover fill.

## Lines

- `hairline`: one device pixel (0.5pt on Retina, never thinner) between rows inside a list or table; never around a container.
- `rule`: 1pt under a modal header, over its footer, under a tab row, beside a settings section title.
- `edge-hc`: 1pt solid around every painted surface in the `-hc` themes.
- Invalid fields: a 1pt inside ring in `critical`.
- Never draw solid borders around cards, panes or controls in the standard themes; fills separate them. Marketing pages, which have no fills to separate on the void ground, draw a 1px slate edge on plates, notes and the CTA panel (NDS-45).
- A menu-bar panel follows the system window's corner (it is a system window), which may differ from `radius-pane`.
