# EdgeRail

The edge rail is an optional macOS working surface on the screen's right edge: hovering a thin zone opens a column of section tiles with a peek of each section, where the person can glance at its state and act on it without opening the app (NDS-34).

## When to use

- Reaching the product's sections from any app or Space without switching windows: Private AI's tools and balance, Traces' watched folders. On macOS only.
- Off by default; the person turns it on in Settings > General.
- Acting in place: the writes the section's tab offers in a row run from the peek too (Pause or Resume watching, a folder's Submit, its "…" menu, a rule change, a tool launch).
- Not for anything that needs a review or a dialog. A trace's review, Submit as… and a rule change that asks first open the main window at that place.
- Not on iOS, iPadOS, Android, web or Windows/Linux, which have no screen-edge surfaces; use widgets, Live Activities, notifications or a tray menu there.

## Anatomy

1. **Hover zone** `.nr-edge-rail__zone`, closed: 4 by 240 (`space-4` by 5 × `space-48`) on the screen's right edge, centered vertically.
2. **Handle** `.nr-edge-rail__handle`: 3 by 72 (`space-2` + 1 by `space-64` + `space-8`), a `neutral` pill at the edge.
3. **Panel** `.nr-edge-rail`, open: the peek, 16 apart (`space-16`), then the rail, 12 from the screen edge (`space-12`); at most 680 tall; 484 wide with 20 of room for the peek's shadow.
4. **Rail** `.nr-edge-rail__rail` on a `.nr-pane`: 56 wide (44 + 2 × 6), 6 padding, 2 between tiles.
5. **Tile** `.nr-edge-rail__tile`: 44 square (`size-control-touch`), radius `radius-card-quiet` (concentric: the pane's 20 minus its 6 padding), glyph 20. One tile per section (Gateway: Private AI, then Traces with the four-node T glyph), a rule, then the app's tile.
6. **Rule** `.nr-edge-rail__rule`: 28 by 1 (`size-control-large`) of `rule` between the section tiles and the app's tile.
7. **App tile**: the Near AI N in `brand-blue` at 20, the size of the tiles' glyphs (NDS-26). Clicking it opens the app; it has no peek.
8. **Peek** `.nr-edge-rail__peek` on a `.nr-pane`: 380 wide (`size-panel-width`), 12 padding, 10 between parts. It is the section's tab in miniature, in the tab's own cards and words:
   - **Header** `.nr-edge-rail__head`: the section's title, then its state word (Private AI: On or Off, as a dot and a word); trailing, the menu-bar panel's round `IconButton`s (Traces: Watching, Settings, Quit; Private AI: Settings, Quit). Settings opens Settings at the section's own page.
   - **Body**: what the tab shows first. Private AI: a launch button per tool that can be started (while signed in), the Credit and Balance tiles, a small Private AI map. Traces: every watched folder as the tree draws it, in a list that scrolls past seven rows, each with its disclosure chevron, its Submit split button and its "…" menu; then the shared and kept graph.
   - No footer: no "Open …" link and no line about what was sent.

## Sizes by density

| | compact (macOS) | regular, touch, dense |
|---|---|---|
| Zone | 4 × 240 | not used |
| Handle | 3 × 72 | |
| Rail | 56 wide, 44 tiles | |
| Peek | 380 wide, `mac-heading` title, `mac-body` and `mac-caption` content; the folder list scrolls past 7 rows | |
| Panel | at most 680 tall | |

## Variants

- **Closed**: the zone and the handle only.
- **Open**: the rail and the peek of the hovered or selected tile. Gateway opens on Private AI.
- **Fixed** (`--fixed`): pins the panel to the viewport's right edge, for documentation pages that show it live.

## States

| State | Treatment |
|---|---|
| Tile default | no fill, glyph `text-primary` |
| Tile hover | `control-hover`; the tile's peek shows |
| Tile pressed | `filter: brightness(0.92)` |
| Tile selected (`aria-current="true"`) | `selection` fill, glyph `text-on-accent` |
| Selected, pressed | `accent-pressed` |
| Focus | 2px `focus-ring`, 2px outside (NDS-5) |
| Window not key | Drawn as focused: the rail never takes `inactive-dim` |
| Sending from a row | The row dims with a `Spinner` in its Submit pill, as in the tab |
| Peek values | unknown values show a dash; a value never reads "on" until the product confirms it; a control whose state is not known yet is hidden (NDS-41) |

## Behavior

- **Pointer**: entering the zone opens the rail. Leaving the panel starts a 300 ms grace (`duration-slow`) before it closes. Hovering or clicking a section tile switches the peek; clicking the app's tile opens the app.
- **Writes**: what a row offers in the tab, it offers here, applied at once with the tab's own rules (a folder's Submit sends at once for a folder set to share, NDS-31). Anything that needs a review or a confirmation opens the main window at that place and puts the rail away.
- **Data**: the rail reads only while it is open; a closed rail reads nothing.
- **Size**: rail content never animates its size. Expanding a folder applies at once. The panel grows its window before the rail slides in and shrinks it only after the rail has slid out; only the rail's controller sets the window's size.
- **Menus**: a row's "…" menu and Submit menu float over the list, never cut off at its foot (see `Menu`).
- **Keyboard**: the handle exposes an Open action to assistive tech, and a Show edge rail command focuses the first tile. When open, Tab moves through tiles and the peek; Escape closes. The panel never takes focus from the app the person is using.
- **Motion**: the panel slides in on `duration-slide` with `ease-standard`. Under Reduce Motion it fades only.

## Accessibility

- Tiles are buttons with names and tooltips from the product ("Traces"); the selected tile has `aria-current`.
- The peek is a region labelled by its heading; its rows keep the tab's own keyboard model (one tab stop, the row's chevron and menu are not tab stops).
- Tile glyphs are icon-only controls: `text-primary` and `text-on-accent` hold 3:1 on their grounds. The handle uses `neutral`, 3:1 on `pane-opaque`; the desktop behind it varies.
- Tiles are 44 square, well above the 28 pointer target.
- **The product supplies**: the sections, their glyphs and names, each peek's content, the header's state word and every button's words.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| A borderless, non-activating `NSPanel` at the status-bar level that joins all Spaces, hosting SwiftUI (`GlassRailTile`, `GlassRailHandle`, `GlassRailRule`) and the tabs' own cards and rows | Not available: widgets and Live Activities | Not available: widgets and notifications | Not available; Windows/Linux shells use a tray menu |

## Do and don't

- Do keep it off by default and keep each peek to what the tab shows first.
- Do run a row's own action in place, and open the app for anything that needs a review, a dialog or a decision with consequences.
- Don't add a footer link or a sentence about what was sent; the header and the rows say it.
- Don't animate or pulse the handle to draw attention.
- Don't add tiles beyond the product's top-level sections and the one tile that opens the app.
- Don't animate the rail's size.

## Source

`EdgeRailGeometry`, `GlassRailTile`, `GlassRailHandle` and `GlassRailRule` in `macos/Sources/TCDesign/Components/EdgeRail.swift` (`size.edgeRail*` and `space.edgeRail*` tokens: zone 4 × 240, handle 3 × 72, rail 56, tile 44, rule 28, peek 380, open height 680, gap 16, inset 12); behavior in `Views/EdgeRail/EdgeRailController.swift` and `EdgeRailView.swift` (300 ms grace, slide, opacity only under Reduce Motion; #1381). The working rail is the owner's 2026-10-22 rework (#1585): Home's tile removed; Private AI and Traces peeks with the popover's buttons in their headers; the folder list with Submit and "…"; the T-shaped four-node Traces glyph (`GlassTraceNodesGlyph`); the blue N in place of the app icon; no footer links and no "nothing sent" line. The cuts were confirmed in the 2026-10-29 staging audit (the Private AI calls figures and the Traces counts card removed). Sizing only from the controller, the window grown before the slide-in and shrunk after the slide-out: #1518, #1519. Tile radius: tokens.json lists edge-rail tiles under `radius-control`, but the source uses the quiet-card radius and the concentric rule gives 14, so this spec uses `radius-card-quiet`.
