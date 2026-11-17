# NavigationRail

A navigation rail holds three to seven app destinations on the leading edge of a tablet or web window, collapsed to icons over labels at 96 wide or expanded to a labelled list at 220.

## When to use

- Medium windows (600 to 839) and expanded windows (840 to 1199) on Android, web and Windows/Linux shells: the collapsed rail.
- Large windows (1200 and wider): the expanded rail beside the content, or the collapsed rail when the panes need the room.
- Compact windows with more than five destinations: the modal expanded rail, opened from a menu button.
- Not on phones in portrait (`TabBar`), not on iPad (the system tab bar that adapts to a sidebar), and not on macOS (`Sidebar` or the three-pane window). Never with a `TabBar` on screen; M3 dropped the navigation drawer, so the expanded rail replaces it.

## Anatomy

1. **Container** `.nr-rail`: 96 (`size-rail-collapsed`) or 220 (`size-rail-expanded`, up to 360). On web it sits on a `.nr-pane`; on an Android tablet it shares the opaque screen pane.
2. **Menu button** `.nr-rail__menu`: 56 by 48, top-aligned, toggles collapsed and expanded.
3. **Primary action** (optional): one `Button`, top-aligned under the menu; it gains its label when the rail expands.
4. **Item** `.nr-rail__item`, collapsed: 64 tall (`space-64`), a 56 by 32 pill indicator (`space-48` + `space-8` by `space-32`) holding a 24 icon, the label 4 below, 4 between items, 6 above and 4 below.
5. **Item**, expanded: 56 tall, the pill spans the rail with the icon and label inside, 8 apart, 16 side padding, no gap between items.
6. **Badge** `.nr-rail__badge`: 16 tall, `badge-fill` with `text-on-status`, on the icon's upper right when collapsed and after the label when expanded.

## Sizes by density

| | regular (web) | touch Android | touch iOS | compact (macOS) | dense |
|---|---|---|---|---|---|
| Width | 96 / 220 | 96 / 220 dp | not used | not used | not used |
| Item height | 64 / 56 | 64 / 56 dp | | | |
| Indicator | 56 by 32 | 56 by 32 dp | | | |
| Label | `web-caption` collapsed, `web-label` expanded, medium | `android-caption` / `android-label` | | | |
| Icon | 24 | 24 dp | | | |

## Variants

- **Collapsed** (default): icons over labels.
- **Expanded, standard** (`--expanded`): beside the content, which resizes.
- **Expanded, modal**: over the content with `scrim`, `shadow-float` and `radius-pane` trailing corners; closes on Escape, a scrim tap, back, or a selection.
- **Hidden when collapsed**: for immersive screens, only when the menu button stays reachable.

## States

| State | Collapsed | Expanded |
|---|---|---|
| Default | icon and label `text-secondary` | same |
| Hover | `control-hover` on the indicator, label `text-primary` | `control-hover` on the whole pill |
| Pressed | indicator `filter: brightness(0.92)` | pill `brightness(0.92)` |
| Selected | `aria-current="page"`: indicator `selection` with a `text-on-accent` icon; label `accent-text`, semibold | pill `selection`, icon and label `text-on-accent` |
| Selected, pressed | `accent-pressed` | `accent-pressed` |
| Focus | 2px `focus-ring`, 2px outside (NDS-5) | same |
| Disabled | never; a destination with nothing in it shows its empty state | same |

## Behavior

- **Keyboard**: Tab reaches the menu button, then the items; Up and Down move between items; Return or Space selects. Re-selecting the current destination scrolls it to the top.
- **Expand and collapse**: the menu button swaps the variant. A standard rail resizes the content beside it on `spring-spatial` over `duration-spring-spatial`; a modal rail slides in on the same spring. Under Reduce Motion both change at once.
- **Scroll**: the rail never scrolls with the content.
- **Adaptive**: below 600 the rail becomes a `TabBar`; at 840 and wider it may expand by default on large windows.

## Accessibility

- A `nav` with a label from the product; items are links with `aria-current="page"`.
- The menu button has `aria-expanded` and a name from the product ("Show labels", "Hide labels").
- Badge counts are hidden; their words ride in the item's name ("2 need your approval").
- Labels never truncate or shrink. At 200% text the items grow taller and labels wrap.
- The whole item, full rail width, is the target (at least 48).
- `text-on-accent` on `selection` holds 4.5:1. In Gateway dark the `selection` fill is 1.09:1 against the pane (flagged, kept from the source), so the label also turns semibold.
- **The product supplies**: destinations, icons, labels, badge counts and their words, the menu button's names.

## Platforms

| Jetpack Compose M3 | Web | SwiftUI/UIKit (iOS/iPadOS) | SwiftUI/AppKit (macOS) |
|---|---|---|---|
| `NavigationRail` (collapsed) and `WideNavigationRail` / `ModalWideNavigationRail` (expanded); `NavigationSuiteScaffold` switches bar and rail by window size class | Custom: this CSS | Not used: `TabView` `.sidebarAdaptable` | Not used: `Sidebar` |

## Do and don't

- Do keep three to seven destinations with one-word labels.
- Do top-align the menu button and the primary action above the items.
- Don't put actions among the destinations; actions belong in a `Toolbar`.
- Don't use the logo as the menu button.
- Don't show the active indicator on more than one item, and don't lay the rail out horizontally.

## Source

Intentional addition. trace-commons ships only on macOS and has no tablet navigation. Measures follow the M3 Expressive navigation rail (collapsed 96, expanded 220 to 360, 64 items, 56 by 32 indicator, 44 top space, replaces the navigation drawer; `m3-components-B.md` §4) and NDS-13. Selection maps M3's secondary-container indicator onto the parent's `selection` and `text-on-accent`, so every selected state uses the accent (NDS-1). Hover and selected fills echo `GlassRailTile` in `macos/Sources/TCDesign/Components/EdgeRail.swift`.
