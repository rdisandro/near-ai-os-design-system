# IconButton

A button whose glyph names the action, drawn round, as a pill, as a glyph in a toolbar group, as a row-menu kebab or as a bare glyph; the consumer always supplies the name that assistive tech reads and the tooltip shows.

## When to use

- Use it for frequent actions with a well-known glyph: Close, Add folder, Previous week, Show inspector, Send.
- Refresh is not an icon button: every re-read is the labelled Refresh pill (`Button`, NDS-36).
- Group view toggles in an `IconButton` group on a toolbar (`role="toolbar"`).
- Use the kebab for a row's menu (the `Menu` opens from it).
- Use a text `Button` when no glyph is unmistakable. A glyph never replaces a label for a primary or destructive decision.

## Anatomy

1. Container: a circle or capsule on `control`, or no fill (toolbar, kebab, bare).
2. Glyph: `size-glyph` (16); small buttons draw it at `size-glyph` × 0.75 (12). The glyph is decorative (`aria-hidden`).
3. Hit area: an invisible box at least `--nr-target` square, centred on the button.
4. Group (toolbar only): a `control` capsule with `space-2` padding and `space-2` between buttons. A toolbar button is the control height minus the group padding on each side (28 − 2 × 2 = 24), so the group stands 28 tall.

## Sizes by density

| Variant | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Round (`.nr-icon-button`) | 28 (`size-control-large`) | 28 | 44 | 40 visible in a 48 target | 20, `radius-dense` |
| Small (`--small`) | 26 (`size-control`) | 26 | 44 | 44, 48 hit area | 26 |
| Pill (`--pill`) | 30 × 26 | 30 × 26 | 52 × 44 | 52 × 44, 48 hit area | 30 × 26 |
| Toolbar in a group (`--toolbar`) | 28 × 24 in a 28 group | 28 × 24 | 44 × 40 | 44 × 40, 48 hit area | 20 × 16 |
| Kebab (`--kebab`) | 22 × 24 (`size-tool-tile`), `radius-tile` | 22 × 24 | 44, round | 44 round, 48 hit area | 22 × 16 |
| Bare (`--bare`) | glyph with a 28 hit area | same | 44 hit area | 48 hit area | 20 hit area |

## Variants

- **Round**: `control` fill, `text-primary` glyph. Close in a modal header is the small round button.
- **Primary**: `accent` fill, `text-on-accent` glyph. The one accent icon action: Send in a composer, Done in a sheet.
- **Toggle**: a round button with `aria-pressed`; on, it takes the `accent` fill and `text-on-accent` glyph. In a toolbar its tooltip is the name, then the state on a second line ("3 of 7 folders automatic"), which assistive tech reads as the hint. A toggle whose state is not yet known stays hidden until it is (NDS-41). Gateway's Automatic-sharing eye in the Traces toolbar is one.
- **Pill**: the graph's period steppers (Previous week, Next week).
- **Toolbar**: no fill, `toolbar-glyph` ink. `aria-pressed="false"` dims the glyph to `toolbar-glyph-off` while its pane is hidden. `aria-expanded="true"` fills it with `toolbar-expanded` while its menu is open.
- **Kebab**: three dots in `text-tertiary`. Hover or open lights it: `control-hover` fill, `text-primary` dots. On a selected row it takes `control-on-selection` and `text-on-accent` dots (NDS-38).
- **Bare**: a glyph in `text-secondary` with no container, such as the close X on a `GetStartedCard` (12 glyph in a 20 frame).

## States

| State | Rule |
|---|---|
| Hover | `control-hover` replaces the fill (toolbar and kebab gain it). Bare turns `text-primary`. Primary keeps `accent`. |
| Pressed | `filter: brightness(0.92)`; primary turns `accent-pressed`. |
| Focus | 2px `focus-ring`, 2px outside, keyboard only (NDS-5). Turning it off with `.nr-focus-off` fails WCAG 2.4.7. |
| Selected | Toggle `aria-pressed="true"`: `accent` and `text-on-accent`. Toolbar: normal ink when its pane shows. |
| Expanded | Toolbar `toolbar-expanded` fill; kebab lit. |
| Disabled | `opacity-disabled`, no hover. In a row or card, hide an action that cannot run instead (NDS-41); toolbar toggles keep their place and disable. |
| Increased contrast | Filled variants, groups and an open kebab get a 1px `edge-hc` inset edge. |

## Behavior

- Click, Space and Return activate. A menu trigger opens its `Menu` on press and on Down arrow.
- On pointer platforms every icon button shows its name in a `Tooltip` after 0.4 s, with the shortcut when it has one.
- A toolbar group is one Tab stop; Left and Right move between its buttons.
- Fills change on `duration-fast` with `ease-standard`. Nothing moves; Reduce Motion changes nothing visible.

## Accessibility

- Name every icon button with `aria-label` (SwiftUI `accessibilityLabel`) from the product's copy, naming the action and its object where needed ("More for near-agents"). The same words feed the tooltip.
- Toggles expose `aria-pressed`; menu triggers expose `aria-haspopup="menu"` and `aria-expanded`.
- Glyphs are marks that carry meaning on their own, so they hold 3:1 against their fill (NDS-6). The button's name and `aria-pressed` also carry the state.
- Targets: 28 pointer, 44pt Apple, 48dp Android and touch web, 60pt visionOS. On touch the kebab becomes a full round button.

## Platforms

| | SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|---|
| Round, small | `GlassRoundButton(label, systemImage:, small:)` with `.help(label)` | `Button` + `.buttonStyle(.glass)`, `Label` with `.labelStyle(.iconOnly)` | `FilledTonalIconButton` | `.nr-icon-button` |
| Primary | `GlassRoundButton` on accent | `.buttonStyle(.glassProminent)` | `FilledIconButton` | `--primary` |
| Toggle | `Toggle` with a round style | `Toggle` with `.button` style | `IconToggleButton` | `aria-pressed` |
| Toolbar group | `GlassToolbarGroup` + `GlassToolbarButton` | system toolbar items (Liquid Glass groups) | floating toolbar `IconButton`s | `.nr-icon-button-group` |
| Kebab | `GlassKebab` | `Menu` with `ellipsis.circle` | `IconButton` with `MoreVert` | `--kebab` |

## Do and don't

- Do give every icon button a name, even when the glyph seems obvious.
- Do use one glyph set (SF Symbols on Apple, Material Symbols on Android, the product's set on web) per platform.
- Don't use a toggle style for an action that has no on state.
- Don't put more than about five icon buttons in one group; move the rest to a `Menu`.
- Don't shrink the hit area to fit a dense row; let the invisible area overlap the padding.

## Source

`GlassRoundButton`, `GlassPillIconButton`, `GlassToolbarButton`, `GlassToolbarGroup` and `GlassKebab` in `macos/Sources/TCDesign/Components/Controls.swift`, `GlassRoundButton(isOn:help:)` for the toolbar toggle (owner, 2026-11-02). `GlassRefreshButton` became `GlassRefreshPill` in `Containers.swift` (#1888), so refresh left this component. The kebab's unlit dots move from `statusOff` ink to `text-tertiary` so an icon-only control holds 3:1 (NDS-6). The primary and toggle variants come from M3 icon buttons (filled, toggle) and Liquid Glass prominent buttons; touch sizes from HIG Buttons and M3.
