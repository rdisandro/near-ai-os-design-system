# ActionBar

The footer row that holds a surface's primary action, with any text about taking that action set directly above it; every button in the bar is the primary button's height.

## When to use

- Use it at the end of a window, page, pane step or sheet that finishes in an action: Submit, Continue, Turn on.
- Put text about taking the action in its notes: what it sends, what it does not authorize, why it waits. Never put that text in the scrolling content.
- `Modal` draws its own footer with the same rules at the small CTA height (30).
- Don't use it for actions on one item in a list; those belong in the row or its `Menu`.

## Anatomy

1. Notes (optional, up to three): label type in `text-secondary`, full width, left-aligned, `space-4` apart.
2. Gap: `space-20` between the last note and the row, so a note reads as part of the page.
3. Leading actions (optional): Back, or a secondary path, at the start of the row.
4. Trailing group (`.nr-action-bar__end`): Cancel or Dismiss, then the primary, `space-8` apart.
5. Divider (optional, `--divided`): a 1px `rule` and `space-10` above the row, when content scrolls under the bar.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Button height | 34 (`size-cta`) | 34 | 44 (`size-control-touch`) | 40 visible in a 48 target | 28 |
| Button padding | `space-16` | `space-16` | `space-16` | `space-16` | `space-16` |
| Button type | `mac-body-strong` | `web-body-strong` | `ios-body-strong` | `android-label` | `web-label` |
| Note type | `mac-label` | `web-label` | `ios-caption` | `android-caption` | `web-caption` |

Every button in the bar takes `--nr-h-bar` whatever its kind, so Back, Cancel and Dismiss stand as tall as Submit (owner ruling D-20). Each keeps its own fill, ink and weight.

## Variants

- **Default**: leading actions at the start, the trailing group at the end.
- **Divided** (`--divided`): a rule above the row for long scrolling content.
- **Stretch** (`--stretch`): below `bp-medium` the trailing buttons share the row equally, Cancel leading.
- **Stacked** (`--stacked`): when labels do not fit side by side, the primary sits on top and Cancel at the bottom (HIG alerts and M3 dialogs agree).

## States

- The bar has no state of its own; each `Button` keeps its states.
- While the primary is busy, the bar disables any action that would abandon the work in flight (Cancel during a send) and keeps the rest.
- A disabled primary explains itself in a note or a `Tooltip`, never by vanishing.

## Behavior

- Order: Cancel leading, the primary trailing, at most one primary (NDS-19). Mirror in right-to-left layouts.
- Return takes the primary when it is the default. A destructive action or an irreversible send is drawn as it is and never answers Return (NDS-15). Esc takes Cancel.
- Keyboard order follows visual order. Notes are text, not stops.
- On phones the bar stays at the bottom of the screen pane above the safe area, and content scrolls under it.
- Nothing in the bar moves; a note appearing or changing fades on `duration-fast` with `ease-standard`.

## Accessibility

- Notes come before the buttons in reading order, so a screen reader hears what Submit sends before reaching it. Link the primary to its notes with `aria-describedby` when they state a consequence.
- The consumer supplies every note and label from the product's copy (NDS-16). Notes state data consequences ("Submit sends these 14 steps to the server that receives your traces.") and never promise privacy.
- Notes use `text-secondary`, which holds 4.5:1 on every pane (7:1 in the `-hc` themes).
- Touch targets follow `Button`: 44pt on Apple, 48dp on Android and touch web.

## Platforms

| | SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|---|
| Bar | `GlassActionBar(notes:, noteInset:) { HStack { … } }` with `GlassButtonStyle(.glass, size: .bar)` beside `.primary` | `.safeAreaInset(edge: .bottom)` bar; a sheet puts Cancel and Done in its top toolbar instead (HIG, 2026) | a `Row` in `Scaffold(bottomBar = …)`; dialog buttons for dialogs | `.nr-action-bar` |
| Notes | `GlassActionNote` | `Text` above the bar | `Text` above the row | `.nr-action-bar__note` |

## Do and don't

- Do put the action's consequence in a note directly above the bar, one placement for every screen.
- Do keep all bar buttons one height.
- Don't put two primaries in the bar, or draw Cancel as primary.
- Don't place a destructive action where Return reaches it.
- Don't repeat the button's label in the note; say what happens.

## Source

`GlassActionBar` and `GlassActionNote` in `macos/Sources/TCDesign/Components/ActionBar.swift`: owner ruling D-20 (every action-bar button is the CTA's size) and D-21 (text about the action sits directly above the bar, label type in secondary ink, full width, left-aligned, 20 above the bar, 4 between notes), both 2026-10-08. Stretch and stacked layouts come from HIG Alerts (default on top of a stack, Cancel at the bottom) and M3 Dialogs (stacked confirm above dismiss).
