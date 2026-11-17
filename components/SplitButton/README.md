# SplitButton

A two-part button whose leading part runs an action and whose trailing chevron opens a `Menu` of variants of that same action, such as Submit 3 with Submit as… beside it.

## When to use

- Use it when one action is the usual choice and two to five close variants exist: Submit {count} / Submit as… (NDS-31), Run agent / Run on a schedule….
- Use the glass split inline in cards and rows; use the filled split only when the action is the surface's one primary action.
- Use a `Menu` from a kebab for unrelated actions, and a plain `Button` when there are no variants.
- Keep the leading label to one or two words.

## Anatomy

1. Container: one capsule on `control` (glass), or two `accent` halves with a `space-2` gap (filled).
2. Action part: the label, padding `space-12` leading and `space-8` trailing (filled: `space-16` and `space-12`).
3. Divider (glass only): 1px `rule`, inset `space-6` from the top and bottom, hidden from assistive tech.
4. Menu part: a chevron (`size-glyph`) in `text-secondary`, padding `space-6` leading and `space-8` trailing (filled: `space-8` and `space-10`).
5. Menu: a `Menu` opening `space-4` below the button with trailing edges aligned (`.nr-menu-anchor`).
6. Inner corners of the filled halves: `radius-tile`, the concentric floor (M3 draws 4dp).

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Glass inline | 28, `mac-label` 600 | 28, `web-label` 600 | native pull-down button, 44 | 40 visible in a 48 target | 20, `radius-dense` |
| Bar (`--bar`) | 34, `mac-body-strong` | 34, `web-body-strong` | 44 | 40 in 48 | 28 |
| Menu part width | chevron + 14 | chevron + 14 | at least 44 | at least 48 (`--nr-target`) | chevron + 14 |

## Variants

- **Glass** (default): the inline control-tier pill from the macOS app.
- **Filled** (`--primary`): two `accent` halves with `text-on-accent`; the surface's one primary action (NDS-19).
- **Bar** (`--bar`): CTA height, for a split inside an `ActionBar` (owner ruling D-20).

## States

| State | Rule |
|---|---|
| Hover | Each part takes `control-hover` on its own. Filled parts keep `accent`. |
| Pressed | `filter: brightness(0.92)` on glass; `accent-pressed` on filled. |
| Open | The menu part keeps its hover fill (filled: `accent-pressed`) and the chevron turns 180 degrees on `spring-spatial-fast` (`duration-spring-spatial-fast`). |
| Focus | Each part draws its own 2px `focus-ring`, 2px outside (NDS-5). |
| Disabled | The whole control at `opacity-disabled` when the action has nothing to act on (`aria-disabled` on the container). |
| Increased contrast | 1px `edge-hc` inset edge on the capsule, or on each filled half. |

## Behavior

- The parts are two Tab stops: action, then menu. Order mirrors in right-to-left layouts.
- Click, Space or Return on the action part runs the action. It never opens the menu.
- Click, Space, Return or Down arrow on the menu part opens the menu with focus on its first item. Esc closes it and returns focus to the menu part.
- The menu floats over everything around the button and is never clipped by the card or row it sits in (see `Menu`). At the end of a scrolling card list, room opens under the button and the list scrolls to show the menu.
- In a row, the split button's Submit sends at once for a folder the person has already set to share (NDS-31). A variant that needs a dialog (Submit as…) opens it in the main window, also from the edge rail.
- The chevron turn is the only movement; under Reduce Motion it flips at once.

## Accessibility

- The action part's name is its visible label. The menu part needs its own name from the product's copy that ties it to the action ("More ways to submit"), plus `aria-haspopup="menu"` and `aria-expanded`.
- The menu is labelled by the menu part (`aria-controls` points at it).
- Each part meets the target on its own: 28 pointer height, 44pt or 48dp on touch, and the menu part is at least `--nr-target` wide on touch.
- Contrast follows `Button`: `text-primary` on `control`, `text-on-accent` on `accent`; the chevron holds 3:1 as a mark.

## Platforms

| | SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|---|
| Control | `GlassSplitButton(title, menuLabel:, action:, menu:)` with a native `Menu` for the list; AppKit `NSComboButton` (split style) for stock windows | `Menu(primaryAction:)`: a tap runs the action, a long press opens the menu | `SplitButtonLayout` with leading and trailing buttons (M3 Expressive) | `.nr-split-button` with two `<button>`s |
| Menu | native menu | native menu (Liquid Glass) | `DropdownMenu` aligned to the trailing part | `.nr-menu` in `.nr-menu-anchor` |

## Do and don't

- Do keep the variants close to the action. "Submit as…" belongs; "Delete folder" does not.
- Do keep the chevron as the only trailing glyph; it turns, it is never replaced.
- Don't put a destructive variant first in the menu or make it the leading action.
- Don't use two filled splits on one surface.
- Don't hide the action's only path inside the menu; anything in the menu also lives in the menu bar or command palette (NDS-14).

## Source

`GlassSplitButton` in `macos/Sources/TCDesign/Components/Controls.swift` (owner, 2026-10-10): the inline glass pill split by a hairline, with the chevron opening a native `Menu`. Labels "Submit {count}" and "Submit as…" (owner, 2026-10-08); the Decisions card's menu drawn over the inspector column, not inside the card (owner, 2026-10-29, #1902). The filled variant, the 2dp gap between halves, the rotating chevron and the 4dp menu offset come from the M3 Expressive split button (m3-components-A §3); the Apple mapping from HIG Pull-down buttons.
