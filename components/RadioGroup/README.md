# RadioGroup

A column, or a short row, of options where exactly one can be chosen and all stay in view, for picking one of two to five.

## When to use

- Use it when two to five options need words to tell apart, often with a sub-line each. Above five, use `Select`.
- Use the row variant for a few short, optional answers (Worked / Partly / Failed).
- Use a `Checkbox` or `Switch` for a single on/off, and a `SegmentedControl` for short values that switch a view.

## Anatomy

1. **Group label**: eyebrow, uppercase, `text-tertiary`.
2. **Radio**: 15 (`size-checkbox`), round. Off: `well` with the `shadow-check` ring. On: `accent` with a dot one third of the radio across (5) in `text-on-accent`.
3. **Title**: the label step at regular weight, `text-primary`, `space-8` after the radio, which centers on its first line.
4. **Sub-line** (optional): caption, `text-tertiary`.

Options sit `space-6` apart in a column. In a row they sit `space-12` apart with `space-6` between radio and title.

## Sizes by density

| | Compact (macOS) | Regular (web) | Touch iOS | Touch Android | Dense |
|---|---|---|---|---|---|
| Radio | 15 | 15 | none (checkmark list) | 20 (M3); 22 on touch web | 15 |
| Row height | one line | one line | 44 | 48 | 20 |
| Title | `mac-label` regular | `web-label` regular | `ios-body` | `android-body` | `web-caption` |

## Variants

- **Column** (default): one answer is always chosen; preselect the safest one.
- **Row**: an optional answer. Nothing is chosen until the person picks, and picking the chosen option again clears it.

## States

| State | Look | Tokens |
|---|---|---|
| Unselected | Well and ring | `well`, `shadow-check` |
| Selected | Accent and dot | `accent`, `text-on-accent` |
| Pressed | Darkens; selected takes the pressed accent | brightness 0.92, `accent-pressed` |
| Focus | 2px ring round the focused radio | `focus-ring` |
| Disabled option | Radio and title dimmed; the sub-line can say why | `opacity-disabled` |
| None chosen | Row variant only; every radio empty | `well` |

## Behavior

- The group is one tab stop. Arrow keys move and select, skipping disabled options and wrapping from last to first. Space selects the focused option.
- In the row variant, Space or Return on the chosen option clears it, as a second click does.
- A choice takes effect at once unless the group sits in a form with a Save.
- Motion: fills change on `duration-fast`; nothing moves.

## Accessibility

- `role="radiogroup"` labelled by the group label, holding native radios that share a `name`. Browsers then give one tab stop and arrow keys.
- The row variant offers a way back to no answer: a "none" choice named by the consumer for assistive tech, or a separate Clear.
- The consumer supplies the group label, titles and sub-lines.
- State is never color alone: the dot marks the choice. In Gateway dark the accent fill sits at 1.09:1 on the pane (flagged), and the white dot carries it.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| `GlassRadioGroup`, `GlassRadioRow`; a native `.radioGroup` picker for assistive tech | No radio buttons. A `Picker` in `.inline` style in a `Form`: rows with a trailing checkmark on the chosen one | `RadioButton` rows in a `Modifier.selectableGroup()`, each `selectable(role = Role.RadioButton)`, colored from the tokens | `.nr-radio-group` with `role="radiogroup"`, `<label class="nr-radio-group__option">` (type class here) and `<input type="radio" class="nr-radio-group__radio">` |

## Do and don't

- Do keep options parallel and short; put detail in the sub-line.
- Do order options predictably, safest or most common first.
- Don't nest radio groups.
- Don't use a row of radios for long labels; use a column.

## Source

`GlassRadio`, `GlassRadioGroup`, `GlassRadioOption` and `GlassRadioRow` in Forms.swift: a 15pt radio with a 5pt dot, a column with title and caption, one keyboard stop with wrapping arrows, and the optional row whose chosen answer clears on a second press. The source turns the row's focus ring off (owner, 2026-10-11); the parent keeps the ring on by default. Keyboard rules follow M3 radio and HIG toggles.
