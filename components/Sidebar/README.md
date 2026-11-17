# Sidebar

A sidebar lists an app's destinations down the leading edge of a desktop, iPad or web window, in groups, two levels deep at most; its section-list variant moves a settings body to a section.

## When to use

- More than five destinations, or destinations in named groups (Workspace, Private AI), on windows 840 and wider.
- The settings window or page: a section list beside one scrolling body (`--sections`).
- Not on phones (use `TabBar`) and not on Android tablets (use the expanded `NavigationRail`). Below 840 the app sidebar hands over to `NavigationRail` (600 to 839) or `TabBar` (under 600).
- Not for views inside one pane (`Tabs`) and not for a pane's sub-pages (`Breadcrumb`).

## Anatomy

1. **Container** `.nr-sidebar` on a `.nr-pane` (navigation layer, glass): 280 wide (`size-sidebar`), 16 between groups.
2. **Group heading** `.nr-sidebar__heading`: eyebrow step, uppercase, `text-tertiary`, 10 side inset.
3. **Row** `.nr-sidebar__item`: glyph 16 (`size-glyph`) in `accent-text`, label, then an optional trailing count or status in `text-tertiary` at the caption step. Radius `radius-control`, 10 side padding, 8 gap, 2 between rows.
4. **Level two** `--nested`: the label lines up under its parent's label (10 + 16 + 8). No third level.
5. **Section list** `--sections`: 180 wide (`size-modal-nav`), label step regular in `text-secondary`, 6 by 10 padding, one line with an ellipsis. `.nr-sidebar__split` places it beside the body.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS (iPad) | touch Android | dense |
|---|---|---|---|---|---|
| Row height | 28 (`--nr-h-control`) | 28 | 44 to 48 (`--nr-target`) | not used | 20 |
| Label | `mac-body` or `mac-label` | `web-label` | `ios-body` | n/a | `mac-label` |
| Glyph | 16 | 16 | 20 | n/a | 16 |
| Width | 280 (180 sections) | 280 | system width | n/a | 280 |

## Variants

- **App sidebar** (default): grouped destinations with glyphs and counts.
- **Section list** (`--sections`): settings sections. Clicking scrolls the body to the section; it selects nothing.
- **Edge** (`--edge`): leading corners squared where the sidebar meets the window edge (macOS and iPadOS 27 run sidebars to the window's edges; 26 floats them as inset panes).
- **Chat panel** (NDS-44, the Near AI chat): an opaque card (`card-on-opaque`) beside the conversation card, opened from an icon rail. Its first row is "New chat"; rows are 36 tall with 20 glyphs in `text-secondary` (the chat glyph is the N inside a speech bubble). The current chat takes `accent-tint` over the panel with its label and glyph unchanged, instead of the solid `selection`, and there is no edge bar. Hover and press are two clearly separate grey steps. This is the chat product's choice; the owner asked for stronger hover and selection contrast and removed the edge bar, and has not ruled on tint versus fill.

## States

| State | App sidebar | Section list |
|---|---|---|
| Default | `text-primary` label, `accent-text` glyph | `text-secondary` |
| Hover | `row-hover` fill | `row-hover` fill, `text-primary` |
| Pressed | `filter: brightness(0.92)` | same |
| Selected | `aria-current="page"`: `selection` fill, `text-on-accent` label, glyph and count, semibold. Chat panel: `accent-tint`, ink unchanged, never an edge bar | the section in view: `text-primary`, semibold, never a fill |
| Selected, pressed | `accent-pressed` | n/a |
| Focus | 2px `focus-ring`, 2px outside (NDS-5) | same |
| Disabled | `opacity-disabled` | a name not loaded yet shows a dash in `text-tertiary` |

## Behavior

- **Keyboard**: rows are links or buttons in tab order; Return or Space activates. With Full Keyboard Access on macOS, arrows move row to row. Show or hide the sidebar from a toolbar button, View > Show Sidebar and Ctrl-Cmd-S; on iPad, an edge swipe. Never hide it by default.
- **Section list**: a click scrolls the body to the section and moves focus to its heading; on web the row of the section in view updates as the body scrolls. Escape closes the settings window.
- **Motion**: fills change on `duration-fast` with `ease-standard`; showing or hiding the sidebar takes `duration-standard`; nothing slides under Reduce Motion.

## Accessibility

- A `nav` with a label from the product. Group headings are headings, and each list is `aria-labelledby` its heading.
- `aria-current="page"` marks the destination; `aria-current="true"` marks the section in view.
- Counts and status are words ("2 waiting", "Running"), never a color alone.
- `text-on-accent` on `selection` holds 4.5:1, and `selection` holds 3:1 against every pane in every theme now that Gateway uses the parent accent (NDS-22). The selected row also turns semibold and carries `aria-current`. A tinted current row (chat panel) is not a state on its own at 3:1, so it keeps `aria-current` and its row stays the only tinted one.
- **The product supplies**: group headings, row labels, glyphs, counts and their words, the navigation label.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| `NavigationSplitView` sidebar with `List(selection:)` (system glass on 26+); custom glass panes follow NDS-7. Glyphs follow the person's system accent on macOS (HIG 2026). Settings: the custom section list | `TabView` with `.tabViewStyle(.sidebarAdaptable)`: a top tab bar that converts to a sidebar; a pure sidebar is a split view | Not used. The expanded `NavigationRail` replaces the drawer (M3 Expressive) | Custom: this CSS on `.nr-pane` |

## Do and don't

- Do keep two levels. For deeper data, add a content list column.
- Do keep group titles short and let people reorder or hide destinations on desktop.
- Don't put critical items at the bottom of a macOS sidebar.
- Don't give section-list rows the accent selection; they scroll, they do not select.
- Don't show a sidebar and a rail or tab bar at the same time.

## Source

Section list: `GlassSectionNavRowStyle` in `macos/Sources/TCDesign/Components/SectionNav.swift` (12pt label, secondary, primary on hover over an 8% ink fill, `Radius.control`, 10 by 6 padding, "never the blue menu selection: the row scrolls a body to its section, it selects nothing"), in the 180-wide Settings list (`Views/Monitor/SettingsModal.swift`). App sidebar: intentional addition. Gateway navigates with tabs in a fixed main pane, but web, iPad and desktop products with more destinations need a leading list (HIG sidebars: floating glass on 26, edge to edge on 27, two levels, accent glyphs; NDS-13).
