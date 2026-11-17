# Slider

A track and thumb for setting a value in a fixed range where the rough position matters more than the exact number, such as an agent's temperature; pair it with a `NumberField` when the exact value matters too.

Intentional addition. trace-commons has no slider. Near AI agent and model settings (temperature, top P, steps per run) are bounded ranges that people tune by feel, and HIG, M3 and Unity all define one.

## When to use

- Use it for a bounded value with immediate feedback.
- Use a `NumberField` alone for unbounded or exact values, and a `SegmentedControl` for two to five named stops.
- On iOS, never use it for volume; use the system's volume view.

## Anatomy

1. **Label and value**: the label in the label step, `text-secondary`; the value trailing in `text-primary` with tabular figures, or a paired `NumberField` on the right (Unity).
2. **Track**: 4 (`space-4`) tall, `radius-pill`. The part from the minimum to the thumb is `accent`; the rest is `well`.
3. **Thumb**: 18 (the switch knob, `size-toggle-height` − `space-6`), round, `accent` with a 2px `text-on-accent` ring so it reads on any track.
4. **End labels**: caption, `text-tertiary`. The minimum leads and the maximum trails, in words that say what each end means (Precise, Creative) or as numbers. They also serve as the 3:1 end marks M3 asks for.

The input's box is `--nr-target` tall, so the whole height is the hit area.

## Sizes by density

| | Compact (macOS) | Regular (web) | Touch iOS | Touch Android | Dense |
|---|---|---|---|---|---|
| Thumb | 18 | 18 | system; 22 on touch web | 4 x 44 handle (M3 XS) | 12 |
| Track | 4 | 4 | system | 16 (M3 XS) | 2 |
| Target | 28 | 28 | 44 | 48 | 20 |
| Label | `mac-label` | `web-label` | `ios-body` | `android-label` | `web-caption` |

## Variants

- **Standard**: continuous.
- **Stops**: a step; the thumb snaps to the nearest stop. Keep stops few enough to tell apart.
- **With field**: a `NumberField` on the right, two-way synced and next in tab order.

## States

| State | Look | Tokens |
|---|---|---|
| Default | Accent fill to the thumb | `accent`, `well` |
| Dragging | Thumb takes the pressed accent; the value updates live | `accent-pressed` |
| Focus | 2px ring round the slider | `focus-ring` |
| Disabled | Track and thumb dimmed; the value stays visible | `opacity-disabled` |
| Mixed | Show the paired field with "—"; set a value before showing a thumb | `text-secondary` |
| Increased contrast | 1px edge on the track | `edge-hc` |

## Behavior

- Dragging changes the value live, as a preview. Clicking the track jumps there, or to the nearest stop.
- Arrow keys move one step; Shift with an arrow, or Page Up and Page Down, move ten. Home and End go to the minimum and maximum.
- Release, or the end of a key press, commits the value: one undo entry per commit.
- On macOS, hovering the thumb shows the value in a tooltip.
- Motion: the thumb follows the pointer directly. Keyboard steps may glide on `spring-spatial-fast`. Nothing animates under Reduce Motion.

## Accessibility

- A native range input (`role="slider"`) named by its label. `aria-valuetext` carries the value in the consumer's words, with any unit.
- `aria-describedby` points at the end labels.
- The consumer supplies the label, end labels and value text.
- The `accent` fill and thumb hold 3:1 on the pane except in Gateway dark (1.09:1, flagged), where the thumb's light ring carries the position.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| `Slider` tinted `accent`, ticks with `step`, value tooltip on hover | `Slider` tinted `accent` | `Slider` (XS) with `activeTrackColor = accent`, `inactiveTrackColor = well` | `<input type="range" class="nr-slider__input">`; script sets `--nr-slider-ratio` from the value |

## Do and don't

- Do put the minimum on the leading side.
- Do label both ends with what they mean.
- Do pair it with a field when people need exact values.
- Don't use it for position, rotation or unbounded values.
- Don't vary track lengths between sliders in one panel (Unity).

## Source

Intentional addition. HIG sliders (minimum leading, live feedback, pair with a field for wide ranges, labeled ends, a value tooltip on macOS), M3 sliders (stops, end marks at 3:1, keyboard map), Unity Foundations slider (label, groove and field, consistent groove lengths, disabled sliders still show their value). The temperature pattern (slider, field and labeled ends) applies the HIG's advice to pair a wide-range slider with a field.
