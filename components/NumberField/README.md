# NumberField

A field for an exact number with its unit, stepper buttons and keyboard nudging, for values like max tokens or a timeout; in dense inspectors its label scrubs the value.

Intentional addition. trace-commons has no numeric input, stepper or slider. Near AI agent and inference settings are numbers with units (max tokens, temperature, timeouts, budgets), and Unity's numeric field (units, label scrubbing, expressions, commit and revert) is the benchmark for editing many of them.

## When to use

- Use it for an exact number, with or without bounds.
- Pair it with a `Slider` for a bounded value people tune by feel.
- Use `TextField` for identifiers that happen to be digits (a port, a code).

## Anatomy

1. **Label**: eyebrow above; in dense rows, beside the well, where it is also the scrub handle.
2. **Well**: as `TextField`, with tabular figures.
3. **Value**: formatted for the locale ("4,096") once committed.
4. **Unit**: a word in `text-tertiary` right after the value (tokens, seconds, s).
5. **Steppers** (optional): two square buttons at the trailing end, the control height − 4, with a concentric radius (11 − 2 = 9), a 12 glyph in `text-secondary`, and `control-hover` on hover.
6. **Message** (optional): the reason when the value is out of range.

## Sizes by density

| | Compact (macOS) | Regular (web) | Touch iOS | Touch Android | Dense |
|---|---|---|---|---|---|
| Well | 28 | 28 | 44 | 56 | 20, radius 3 |
| Steppers | 24 | 24 | system `Stepper` beside the value; 40 on touch web | −/+ icon buttons, 48 targets | none (scrub and arrows) |
| Text | `mac-label` regular | `web-label` regular | `ios-body` | `android-body` | `web-caption` |

## Variants

- **With steppers** (default).
- **Plain**: no steppers, beside a `Slider`.
- **Inline** (`--inline`): label column and scrubbing, for inspectors.
- **Mixed**: several items selected with different values.

## States

| State | Look | Tokens |
|---|---|---|
| Focus | 2px ring round the well | `focus-ring` |
| Stepper hover | Fill appears | `control-hover` |
| At a bound | That stepper is disabled | `opacity-disabled` |
| Invalid | 1px ring and the range in words ("Use a number from 1 to 32,768.") | `critical`, `critical-text` |
| Disabled | Well dimmed | `opacity-disabled` |
| Mixed | "—" in `text-secondary`; the consumer's "Mixed" is announced | `text-secondary` |
| Unknown | "—", never 0 | `text-secondary` |

## Behavior

| Input | Effect |
|---|---|
| Typing | Digits and the locale's separators. A math expression (4096*2, 30+15) evaluates on commit. |
| Up / Down | One step. Shift multiplies by 10; Alt (Option) by 0.1. |
| Stepper | One step; Shift-click 10; press and hold repeats. |
| Label scrub | Drag the label left or right; the cursor is `ew-resize`; Shift and Alt as above. |
| Enter or blur | Commits, formats and records one undo entry. |
| Esc | Reverts to the last committed value; a mixed field stays mixed. |

- Stepping and scrubbing send live values that preview the change; only the commit is recorded.
- Text that is not a number reverts to the last valid value on commit. A number out of range stays, marked invalid, until it is fixed; it is never clamped silently.
- Mixed: typing, stepping or scrubbing sets every selected item to the new value.

## Accessibility

- `role="spinbutton"` with `aria-valuenow`, `aria-valuemin`, `aria-valuemax` and an `aria-valuetext` that includes the unit ("4,096 tokens"). Mixed sets `aria-valuetext` to the consumer's word.
- Steppers are not tab stops; arrow keys do their job. Their names come from the consumer ("Increase max tokens").
- The consumer supplies the label, unit, range message and mixed word.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| `TextField(value:format:)` in the painted well with steppers in it, or a native `Stepper` beside it | `TextField` with a decimal keyboard and a native `Stepper` beside the value | `OutlinedTextField` with a decimal keyboard and `suffix` for the unit, plus −/+ `IconButton`s | `.nr-number-field__well` (type class here) with `<input role="spinbutton">`, the unit and `.nr-number-field__step` buttons |

## Do and don't

- Do show the unit as a word.
- Do give the range in the reason when a value falls outside it.
- Don't show 0 for a value that is unknown or mixed.
- Don't clamp an out-of-range value without telling the person.

## Source

Intentional addition. Unity Foundations numeric field (label scrub, Enter commits, Esc reverts, invalid input reverts) and App UI `NumericalField` (unit, scrubbing, expressions, live versus committed change events); HIG steppers (Shift-click for bigger steps) and text fields (number formatters, locale); the mixed value fills a gap both Unity sources leave open.
