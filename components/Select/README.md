# Select

A pill that shows the current value and opens a menu of values, for choosing one of a known set such as a folder's mode (Ask, Automatic or Never).

## When to use

- Use it for three to about ten values. With fewer that all fit in view, use `RadioGroup` or `SegmentedControl`. With more, use a searchable list.
- Use it for values. Put actions in a `Menu`.
- Use the icon menu when the control must be small and its meaning is clear from a glyph and tooltip (sort order, a view option).

## Anatomy

1. **Pill**: `control` fill, `radius-pill`, height `--nr-h-control`, `space-10` padding.
2. **Status dot** (optional): 7 (`space-6` + 1px, the source's dot), the option's status mark, `inline-gap` from the words. Words always carry the status.
3. **Value**: the label step, semibold, `text-primary`. With nothing chosen, the consumer's placeholder ("Choose…") in `text-placeholder`.
4. **Chevron**: 10 (`space-10`), `text-tertiary`.
5. **Menu**: `menu` fill on the floating layer (`blur-floating`, `shadow-float`), `radius-card-quiet`, `space-4` inset, at least `size-menu-min-width` (220) wide. Options are `--nr-target` tall with a concentric radius (14 − 4 = 10), a 12 check column leading the chosen one, and `menu-hover` with `text-on-accent` on the highlighted one.

## Sizes by density

| | Compact (macOS) | Regular (web) | Touch iOS | Touch Android | Dense |
|---|---|---|---|---|---|
| Pill height | 28 | 28 | 44 (row, value trailing) | 56 (exposed dropdown) | 20, radius 3 |
| Option height | 28 | 28 | 44 | 48 | 20 |
| Value | `mac-label` semibold | `web-label` semibold | `ios-body` | `android-label` | `web-caption` |
| Target | 28 | 28 | 44 | 48 | 20 |

## Variants

- **Select**: always has a value.
- **Picker**: optional; shows the consumer's placeholder until something is chosen.
- **Icon menu**: a round icon-only button at the control height. The chosen option is its value, shown with a check in the menu.
- **With status dots**: Ask `caution`, Automatic `positive`, Never `neutral`.

## States

| State | Look | Tokens |
|---|---|---|
| Hover | Fill replaced | `control-hover` |
| Pressed | Fill darkened | brightness 0.92 |
| Open | Hover fill held while the menu is open | `control-hover` |
| Focus | 2px ring, 2px outside | `focus-ring` |
| Invalid | 1px ring inside the pill and the reason under it | `critical`, `critical-text` |
| Disabled | Whole pill dimmed, no hover | `opacity-disabled` |
| Mixed | "—" in `text-secondary`; the consumer's "Mixed" is announced | `text-secondary` |
| Unknown | The product's word or "—"; never a guessed value | `text-secondary` |

## Behavior

- Click or press opens it, never hover. Space, Enter or Down opens it from the keyboard. Arrows move, typing jumps to a match, Enter chooses and Esc closes with no change.
- The menu stays attached to the pill and never covers the label beside it. The native macOS pop-up may open over the pill with the chosen value aligned, as the system draws it.
- Use separators to group values and at most one submenu level.
- Choosing applies at once unless the pill sits in a form with a Save. A value that grants something (Automatic) can ask for a confirmation first.
- Mixed: choosing applies the value to every selected item; Esc keeps them mixed.
- Motion: the menu fades in on `duration-standard`; nothing moves under Reduce Motion.

## Accessibility

- Web: a button with `aria-haspopup="listbox"` and `aria-expanded` opening a `listbox` of `option`s with `aria-selected`. A native `<select>` with these classes works when no dots are needed.
- The consumer supplies the name, often the row's subject plus what it sets ("Mode for near-agents"), and every value's words. The value is the chosen option's words.
- Dots are hidden from assistive tech. The icon menu takes its name and tooltip from the consumer.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| `GlassSelect` and `GlassPicker`: a native `Menu` in `.button` style holding an inline `Picker`, so the system draws the check; `GlassIconMenu` | `Picker` in `.menu` style in a `Form` row with the value trailing, or a `Menu` | `ExposedDropdownMenuBox` with a read-only `OutlinedTextField` and `DropdownMenu`, colored from the tokens | `<button class="nr-select">` (type class here) and `.nr-select__listbox` |

## Do and don't

- Do keep values short and parallel.
- Do show a dot only beside words.
- Don't preselect a value for the person when the choice grants something; use the picker with a placeholder.
- Don't put actions and values in the same menu.

## Source

`GlassPicker`, `GlassPickerPill`, `GlassPickerOption` and `GlassIconMenu` in Controls.swift; `GlassSelect` in Forms.swift; `GlassMenu` in Surfaces.swift. The folder modes Ask / Automatic / Never ("Ask" since 2026-10-12, NDS-30) and the confirmation before Automatic come from Gateway's Rules step. Added by the parent: the mixed and unknown values (Unity gap), dense size (Unity dropdown), and the web listbox.
