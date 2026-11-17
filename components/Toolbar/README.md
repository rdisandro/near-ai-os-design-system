# Toolbar

A toolbar holds a screen's frequent commands in at most three groups along the top or bottom edge, with at most one prominent action at the trailing end.

## When to use

- The top row of a window's main pane: pane toggles and Settings (desktop). Options that belong to one list live in that list's own menu, not in the toolbar.
- A page header on web and tablet: back, title, tools, the one primary action (Run agent).
- A floating or docked bar on phones for a screen below the top level (reviewing a trace: Look inside, Keep, Submit).
- Not for app destinations (`Sidebar`, `NavigationRail`, `TabBar`), not for a form's Cancel and submit row (`ActionBar`), and never together with a `TabBar` on a phone.

## Anatomy

1. **Bar** `.nr-toolbar`: at least `--nr-h-bar` tall (34, 44 on touch), `--nr-gap` between parts. Leading: back and title. Then a spacer. Trailing: groups, then the prominent action.
2. **Window-controls clearance** `.nr-toolbar__window-controls`: 78 by 30 (`space-64` + `space-14` by `space-24` + `space-6`) for the macOS traffic lights inside the main pane.
3. **Title** `.nr-toolbar__title`: the title step, one line, truncating. Under 15 characters, never the app's name.
4. **Group** `.nr-toolbar__group`: a `control` capsule, 2 padding (`space-2`), 2 between buttons.
5. **Button** `.nr-toolbar__button`: 28 by 24 (`--nr-h-control` minus 2 × `space-2` tall), glyph 16 (`size-glyph`, the source's 13pt symbol), `toolbar-glyph`. Its fill sits behind the glyph so a press darkens the fill only. The hit area grows to `--nr-target`.
6. **Round button** `--round`: a 28 circle with its own `control` fill (Settings).
7. **Text button** `--text`: its own capsule, label semibold; never inside an icon group.
8. **Prominent action** `.nr-toolbar__prominent`: an `accent` pill, `text-on-accent`, semibold label, 14 side padding, `--nr-h-control` tall. One per toolbar.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Bar height | 34 | 34 | 44; floating 52 | 64 docked; floating 52 | 28 |
| Button | 28 × 24 | 28 × 24 | 44 × 40, 48 target | 44 × 40, 48 target | 20 × 16, 20 target |
| Glyph | 16 | 16 | 20 | 20 | 16 |
| Prominent | 28, `mac-label` | 28, `web-label` | 44, `ios-body-strong` | 44, `android-label` | 20 |

## Variants

- **Pane row** (default): no surface of its own; the pane is the glass.
- **Floating** (`--floating`): a glass capsule over content (`blur-bar`, `shadow-float`), 8 side padding and 4 above and below: the iPhone bottom toolbar and the M3 floating toolbar.
- **Docked** (`--docked`): a full-width glass bar, 64 tall, 16 side padding: the M3 docked toolbar, which replaced the bottom app bar.

## States

| State | Treatment |
|---|---|
| Default | glyph `toolbar-glyph`, no fill |
| Hover | `control-hover` behind the glyph |
| Pressed | the fill at `filter: brightness(0.92)`; the glyph keeps its contrast |
| Toggle on (`aria-pressed="true"`) | `toolbar-glyph` |
| Toggle off (`aria-pressed="false"`, its pane hidden) | `toolbar-glyph-off`, 3:1 on `control` in every theme (NDS-50) |
| Menu open (`aria-expanded="true"`) | `toolbar-expanded` fill |
| Prominent pressed | `accent-pressed` |
| Disabled | `opacity-disabled`, no hover; explain why nearby |
| Focus | 2px `focus-ring`, 2px outside (NDS-5) |

## Behavior

- **Keyboard**: on web, `role="toolbar"` is one tab stop; Left and Right move between controls. On macOS every toolbar command is also a menu-bar command with a shortcut, and on web and Windows/Linux it is in the command palette (NDS-14).
- **Overflow**: commands that do not fit move into a More menu at the trailing end. macOS and iPadOS add their own overflow menu, so never add one there. Hide whole items, never empty their contents.
- **Prominent action**: never answers Return when it sends something that cannot be undone (Submit); it is drawn prominent and needs a click or tap (NDS-15).
- **Scroll**: a floating toolbar may slide away on scroll down and return on scroll up, never while VoiceOver or TalkBack runs.
- **Motion**: fills change on `duration-fast`; showing and hiding run on `spring-spatial`; nothing moves under Reduce Motion.

## Accessibility

- `role="toolbar"` with a label from the product. Every icon-only button has a name and a tooltip from the product's copy.
- Pane toggles use `aria-pressed` with a fixed name ("Inspector"); menu buttons use `aria-haspopup` and `aria-expanded`.
- Glyphs are icon-only controls and hold 3:1 on `control`.
- Targets: 28 on desktop (24 visible, the hit area 2 above and below), 44 iOS, 48 Android and touch web.
- **The product supplies**: the title, every command's name and glyph, toggle and menu state, the prominent action's label.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| Standard windows: `.toolbar` with `ToolbarItemGroup` (system glass groups). The glass three-pane window: the custom pane row (`GlassToolbarGroup`) | `.toolbar` with `ToolbarItemGroup`, `ToolbarSpacer` and `.bottomBar`; the navigation bar is part of the toolbar; `.buttonStyle(.glassProminent)` for the one prominent action | `HorizontalFloatingToolbar` (floating) or `FlexibleBottomAppBar` (docked); `TopAppBar` for title and back | Custom: this CSS |

## Do and don't

- Do group by function and frequency: navigation leading, tools trailing.
- Do keep one prominent action, trailing, and Cancel leading when both appear (NDS-19).
- Don't use more than three groups.
- Don't mix text buttons and icons in one capsule.
- Don't put a toolbar alongside a `TabBar` on a phone.
- Don't use outlined-circle glyphs inside a group; the group is the container.

## Source

`GlassToolbarButton` (28 × 24, symbol 13, `toolbarGlyph` and `toolbarGlyphHidden`, `toolbarExpanded` while its menu is open, `controlHover` under the pointer, a pressed wash that never darkens the glyph) and `GlassToolbarGroup` (control capsule, 2 padding, 2 spacing) in `macos/Sources/TCDesign/Components/Controls.swift`; the main pane's top row in `Views/MonitorWindowView.swift` (78 clearance for the traffic lights, a 28 round Settings button; the View button removed in #1490, its one item moved to the Traces filter menu). The floating and docked variants are an intentional addition for web, tablet and phone: HIG toolbars (at most three groups, one prominent action trailing, navigation bars folded into toolbars) and M3 Expressive toolbars (docked 64, floating pill, never with a navigation bar).
