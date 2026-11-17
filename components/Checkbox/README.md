# Checkbox

A box that turns one option on or off, or shows that some of its children are on, for options applied together, consent rows and multi-select lists.

## When to use

- Use it for related options that can each be on, such as the ways contributed traces may be used.
- Use it for a consent, with the full sentence beside the box. A consent checkbox can gate a confirmation's action.
- Use it for hierarchies: a parent over indented children shows mixed when they differ.
- On macOS, ordinary settings use checkboxes. Use a `Switch` for a setting that turns a feature on or controls a group, and never swap existing checkboxes for switches.
- Use `RadioGroup` or `Select` for opposing choices, and a `Switch` for an on/off that acts at once on touch.

## Anatomy

1. **Box**: 15 (`size-checkbox`), `radius-checkbox` (5). Off: `well` with the `shadow-check` ring. On or mixed: `accent` with a check or a dash in `text-on-accent`, about 8 across.
2. **Label**: the label step at regular weight, `text-primary`, `space-8` after the box. It wraps under its own width; the box centers on its first line.
3. **Sub-line** (optional): caption, `text-tertiary`, 1 below.
4. **Children** (optional): indented by the box plus 8, so their boxes sit under the parent's words.

The whole row is the hit area, and the box's own hit area grows to `--nr-target`.

## Sizes by density

| | Compact (macOS) | Regular (web) | Touch iOS | Touch Android | Dense |
|---|---|---|---|---|---|
| Box | 15 | 15 | 22 (`size-control-touch` / 2) | 18 (M3) | 15 |
| Box to words | 8 | 8 | 12 | 12 | 8 |
| Row height | one line | one line | 44 | 48 | 20 |
| Label | `mac-label` regular | `web-label` regular | `ios-body` | `android-body` | `web-caption` |

## Variants

- **Standalone**: a short label.
- **Check row**: a consent sentence that wraps beside the box.
- **Parent and children**: the parent shows on, off or mixed from its children.
- **Read-only mark**: the box drawn for a state the person reads but cannot change here, hidden from assistive tech; the row's words state it.

## States

| State | Look | Tokens |
|---|---|---|
| Off | Well and ring | `well`, `shadow-check` |
| On | Accent fill and check | `accent`, `text-on-accent` |
| Mixed | Accent fill and dash | `accent`, `text-on-accent` |
| Pressed | Off darkens; on and mixed take the pressed accent | brightness 0.92, `accent-pressed` |
| Focus | 2px ring round the box | `focus-ring` |
| Disabled | Box and title dimmed; the sub-line that says why stays readable | `opacity-disabled` |
| Invalid | A required consent left unticked on submit: the reason under the row | `critical-text` |
| Increased contrast | The ring takes the high-contrast edge | `shadow-check` (-hc values) |

## Behavior

- A click or tap anywhere on the row toggles it. Space toggles; Enter submits the form on the web.
- Checking a parent checks every child, and unchecking it clears them. Some children on makes the parent mixed. Checking a mixed parent checks all children.
- In a form, the values apply on submit. In a macOS settings window an ordinary checkbox applies at once and offers Undo when the change matters.
- Motion: the fill changes on `duration-fast`; the check does not animate.

## Accessibility

- A native checkbox: `<input type="checkbox">` with the `indeterminate` property for mixed; a SwiftUI `Toggle` in checkbox style, with `Toggle(sources:isOn:)` for a group so the system says "mixed".
- The sentence is the name. A parent lists its children with `aria-controls`.
- The consumer supplies the words; the platform speaks the state.
- State is never color alone: a check, a dash or an empty box. `text-on-accent` on `accent` holds 4.5:1. In Gateway dark the accent fill sits at 1.09:1 on the pane (flagged), so the white check carries the state there.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| `Toggle` with `GlassCheckboxStyle`; `GlassCheckRow` for consent rows; `GlassCheckMark` for read-only | No system checkbox. Multi-select lists use a trailing checkmark on the row; consent rows use a custom `ToggleStyle` drawing the 22 box | `Checkbox` and `TriStateCheckbox` with `accent`, `well` and `text-on-accent` colors | `<label class="nr-checkbox">` (type class here) with `<input class="nr-checkbox__box">` and `.nr-checkbox__text` |

## Do and don't

- Do write the label as the full statement the person agrees to.
- Do indent children under the parent's words.
- Don't use a checkbox for something that takes effect on touch at once; use a `Switch`.
- Don't use a list of switches for multi-select.
- Don't write labels that turn something off when checked.

## Source

`GlassCheckboxStyle` and `GlassCheckMark` in Controls.swift (15pt box, radius 5, accent fill with an 8pt heavy check or a minus for mixed, well and rim when off); `GlassCheckRow` in Forms.swift (the sentence wrapping beside the box). The source dims a disabled checkbox to 0.7 (`disabledCheck`); the parent uses `opacity-disabled` on the box and title and keeps the reason readable. Parent and child rules follow M3 checkbox, HIG toggles and Unity toggle.
