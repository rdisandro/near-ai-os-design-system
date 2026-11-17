# Button

A capsule that starts one action now, in six kinds (primary, secondary, glass, destructive, link, submit) plus the Refresh pill, and four heights (submit 24, inline 28, small 30, bar 34), so each surface shows one primary action and quieter alternatives.

## When to use

- Use a button for an action that happens when pressed: Submit, Look inside, Turn on, Withdraw.
- Give each surface at most one `primary` button (NDS-19). Draw the other actions as `glass` and the lowest-priority choice as `link`.
- Use `destructive` for an action that loses data and cannot be undone. A reversible action acts at once and offers Undo instead (NDS-15).
- Use `IconButton` when a glyph names the action, `SplitButton` when one action has close variants, and `Menu` for three or more related actions.
- Do not use a button to move between views. Use `Tabs`, `Sidebar` or a link.

## Anatomy

1. Container: a capsule (`radius-pill`) filled by the kind. When the capsule is shorter than `--nr-target`, an invisible hit area extends it to the target height.
2. Label: the consumer's words on one line. The height is a minimum, so the label grows with the system text size.
3. Optional leading glyph (`size-glyph`, `inline-gap` from the label) or, while busy, a 12px spinner (`space-12`).

## Sizes by density

| Size | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Bar and primary (`--bar`) | 34, padding 16, `mac-body-strong` | 34, padding 16, `web-body-strong` | 44, padding 16, `ios-body-strong` | 40 visible in a 48 target, `android-label` | 28, padding 16, `web-label` |
| Small (modal action bar) (`--small`) | 30, padding 14, `mac-label` | 30, padding 14, `web-label` | 44 | 40 in 48 | 28, padding 12 |
| Inline glass and destructive | 28, padding 12, `mac-label` | 28, padding 12, `web-label` | 44, `ios-label` | 40 in 48 | 20, `web-caption` |
| Submit pill (`--submit`) | 24, padding 10, `mac-caption` | 24, padding 10, `web-caption` | 24 visible, 44 hit area | 24 visible, 48 hit area | 24 |
| Link | text height, 28 hit area | same | 44 hit area | 48 hit area | 20 hit area |

Heights come from `--nr-h-bar` (34 / 44 / 28) and `--nr-h-control` (28 / 44 / 20); small uses `size-cta-small`, submit `size-submit-pill`. Weight is 700 for primary, secondary and submit, 600 for the rest. Every size is a capsule except dense, which uses `radius-dense` (Unity Editor). M3 Expressive sizes M, L and XL (56, 96, 136) are for hero moments only.

## Variants

- **Primary**: `accent` fill, `text-on-accent` label. The one action of the surface.
- **Secondary**: `accent-tint` fill, `accent-text` label. A strong action that is not the surface's one, used sparingly. Download and install buttons are not secondary: they are glass, never colored (NDS-42). In the owner's rulings, "secondary" means the glass kind.
- **Glass**: `control` fill, `text-primary` label. Every other action, including Download and Choose folder. With `aria-pressed="true"` it is the chosen one of a set and takes the `accent` fill.
- **Destructive**: `control` fill, `destructive-text` label. Never the default action.
- **Link**: no container, `accent-text`. The lowest-priority choice ("Not this one").
- **Submit**: the 24 pill on tree rows ("Submit 3" on a folder, "Submit" on a trace). On a trace row it sends at once and the row dims with a spinner while it sends (NDS-31). `data-done` turns the label `positive-text` ("Sent").
- **Refresh** (`--refresh`): a glass capsule at the height of the round button it replaces (26 small, 28 inline), padding 8 small or 10, holding the word "Refresh" in label medium and then the `arrow.clockwise` glyph (11 small, 13), 4 apart. The glyph turns while the re-read runs and holds still under Reduce Motion. Every re-read uses it, including the ones that said Retry (NDS-36).
- **On another ground** (NDS-38): a glass or submit pill on a selected row takes `control-on-selection` (hover `control-on-selection-hover`) and its label and glyph take `text-on-accent`; on a menu or popover it takes `control-on-menu` (hover `control-on-menu-hover`), so the pill never vanishes into the surface under it.
- **Classic treatment** (optional, NDS-2): primary adds `edge-classic-cta`, glass and destructive add `edge-classic-control`. Flat glass draws no edges.

## States

| State | Rule |
|---|---|
| Hover | Glass, destructive and Refresh replace the fill with `control-hover` (or the ground's own hover, NDS-38). Link underlines. Primary, secondary and submit keep their fill. |
| Pressed | Accent fills turn `accent-pressed`; neutral fills darken with `filter: brightness(0.92)`. Never a fade, which reads as disabled. |
| Focus | 2px `focus-ring`, 2px outside, keyboard focus only (NDS-5). Gateway turns it off with `.nr-focus-off`, which fails WCAG 2.4.7. |
| Selected | Glass with `aria-pressed="true"`: `accent` fill, `text-on-accent`. |
| Disabled | The whole button at `opacity-disabled`, no hover. Say why nearby or in a `Tooltip` (use `aria-disabled` so the tooltip can show). |
| Busy | `aria-busy="true"`: inert at full strength, a spinner before the consumer's progress label ("Sending…"). Refresh keeps its word and turns its glyph instead. |
| Done | Submit only: `positive-text` label. |
| Increased contrast | A 1px `edge-hc` inset edge on every kind except link. |

## Behavior

- Click, Space and Return activate. In a modal, sheet or form, the default action also answers Return. A destructive action or an irreversible send never answers Return (NDS-15).
- Esc and Mod+. cancel the surface. They never press a button.
- Fills change on `duration-fast` with `ease-standard`. Nothing moves. Android keeps the M3 Expressive press morph that Compose draws natively; web and Apple platforms keep the capsule. Under Reduce Motion the spinner stops and the label carries the state.
- Add a trailing "…" to a label when the action opens something that needs more input ("Run on a schedule…").

## Accessibility

- Use the native button on every platform. The visible label is the accessible name; the consumer supplies it from the product's copy (NDS-16). Labels name the action: a verb, or a verb and an object.
- A selected glass button exposes `aria-pressed` (SwiftUI `.isSelected`). A busy button sets `aria-busy` and changes its label; announce the change politely when focus is elsewhere.
- Contrast: `text-on-accent` on `accent` measures 6.85:1 light, 8.8:1 dark and 7.17:1 light-hc; Gateway uses the parent accent, so the same (NDS-22). `destructive-text` holds 4.5:1 over the worst ground behind glass, and a pill's label on `control-on-selection` holds 4.5:1.
- Refresh: the accessible name and tooltip say what is refreshed ("Refresh your tools"); the visible word stays "Refresh".
- Targets: 28 pointer, 44pt Apple touch, 48dp Android and touch web. The submit pill and link grow their hit area, never their drawing.

## Platforms

| | SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|---|
| Control | `Button` + `GlassButtonStyle(kind, size:, small:)`, custom painted (NDS-7) | `Button` with `.glassProminent` (primary) and `.glass` (glass); `role: .destructive` | `Button` (primary), `FilledTonalButton` (secondary), `OutlinedButton` (glass), `TextButton` (link) on parent colors | `<button class="nr-button nr-button--primary">` |
| Heights | 24 / 28 / 30 / 34 ladder | `.controlSize(.large)`, 44 hit | M3 S (40) in a 48 target | density classes |
| Return | `.keyboardShortcut(.defaultAction)` | same, hardware keyboard | n/a | form submit or the dialog's default |
| Busy | `ProgressView` in the label | `ProgressView` in the label | `CircularProgressIndicator` in the content | `.nr-button__spinner` |

## Do and don't

- Do keep one primary per surface, with Cancel leading as glass (NDS-19). A notice's call to action is primary too (NDS-25).
- Do make every button in an action bar the CTA's height (`ActionBar`, owner ruling D-20).
- Do show preference with the kind. Don't use size to rank buttons in a set.
- Don't make a destructive action primary or the default.
- Don't write words in the component. Labels, progress words and reasons come from the product.
- Don't fade a pressed button or dim a busy one.

## Source

`GlassButtonStyle` with `GlassButtonKind` (primary, secondary, glass, submit, link, destructive), `GlassButtonSize` (inline, bar), `small` and `selected` in `macos/Sources/TCDesign/Components/Controls.swift`; owner ruling D-20 sets bar-sized buttons. The parent maps Gateway's old dark purple secondary gradient to the tonal `accent-tint` fill so product accents can override it (NDS-1), and moves the CTA glow to the Classic treatment; Gateway now draws the parent accent (NDS-22). `GlassRefreshPill` in `Containers.swift` (owner, 2026-11-02, #1888); download buttons neutral (owner, 2026-10-08); ground-aware fills (owner, 2026-10-22, #1585). Busy state from HIG Buttons (activity indicator in the button); touch heights from HIG (44pt) and M3 (40dp in a 48dp target); dense corners from Unity Editor.
