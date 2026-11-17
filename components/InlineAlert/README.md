# InlineAlert

One line of `critical-text` caption, unboxed, directly under the control it is about, saying why a request the person just made failed and what to do next.

## When to use

- An action that failed or was refused: Submit didn't go through, an undo was refused, a write to a row was rejected.
- A field's invalid reason, under the field whose `TextField` invalid ring it explains.
- Inside a `Notice` or `Toast`, under their buttons, when their own action fails.
- Use `Notice` when the failure belongs to a whole section. Never use a `Toast` or a `Modal` for a failure people can fix in place.

## Anatomy

1. **Line.** The caption step in `critical-text`, left aligned, as wide as the control's column, wrapping freely. No frame, no fill, no icon.
2. **Dismiss** (optional). A `Button` link after the words, baseline aligned, `space-8` from them.

Place it in the same column as the control, directly under the row of buttons or the field, at the column's own gap (`space-6` to `space-8`). Keep it under about 200 characters.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Words | `mac-caption` | `web-caption` | `ios-caption` | `android-caption` | `mac-caption` |
| Gap above | `space-6` | `space-8` | `space-8` | `space-8` | `space-4` |
| Dismiss target | 28 | 28 | 44 | 48 | 20 |

## Variants

- **Under actions.** The failed request's line, under the row of buttons it is about.
- **Under a field.** The invalid reason; the field shows its 1px `critical` ring.
- **With dismiss.** For a failure that stays relevant until the person reads it.
- **Nested.** Inside a `Notice` or `Toast`, under that component's buttons.

## States

- **Shown.** Appears when the failure arrives and pushes the content below it down.
- **Replaced.** The next result of the same control replaces it: a new reason, or nothing on success.
- **Cleared.** On success, on Dismiss, or as soon as the person edits the field it explains.
- Never keep an alert after its condition changed. An old failure next to a working control reads as a new one.

## Behavior

- No motion. The line is in the flow, so it moves content down rather than covering it.
- Focus stays on the control. Pressing the control again is the retry; add a separate Retry only when the original control is gone.
- One alert per control. When two requests fail, each says so under its own control.

## Accessibility

- Web: render into a container that exists before the message does. For a failure of the action just taken, use `role="alert"` so it is read once at once; for a field validated on blur, use `aria-live="polite"` and set `aria-invalid` on the field. Link the control to the line with `aria-describedby` so focusing the control reads the reason again.
- Apple platforms: post the words as an announcement (`AccessibilityNotification.Announcement`, `UIAccessibility.post(.announcement)`). Compose: `semantics { liveRegion = LiveRegionMode.Polite }`, or `isError` with `supportingText` on a text field.
- The consumer supplies the words from the product's copy. The words, not the color, say that something failed.
- Contrast: `critical-text` holds 4.5:1 over the worst ground behind glass and 7:1 in the `-hc` themes.

## Platforms

| | SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|---|
| Build | Custom `GlassAlert`: `Text` in caption, `critical-text`, full width | `Text` in a `Section` footer or under the buttons | `Text` under the buttons; `supportingText` with `isError` for fields | `<p class="nr-inline-alert" role="alert">` |
| Native? | No (a native alert is a modal) | No | Native for fields, custom otherwise | No |

## Do and don't

- Do say what failed, why, and what to do: "Submit didn't go through. The watcher isn't answering, so nothing was sent. Try again once it's back."
- Do state what happened to the data.
- Do put the line under the exact control that failed.
- Don't box the line or put it in a well; a boxed line reads as a disabled text field.
- Don't prefix "Error:" or use codes as the message.
- Don't blame the person ("You entered an invalid value").

## Source

`GlassAlert` in `Components/StatCard.swift` (a failed request's line in caption text and the critical text color, with no frame, under the buttons it is about; a boxed line "read as a disabled text field", owner ruling 2026-10-09). The failed-action line with a Dismiss link after it comes from `Views/Monitor/InspectorPrompts.swift`; action ordering is trace-commons cross-screen pattern 10 (the action, then the links, then the failure line under both). The 200-character limit, the place under the control and the Problem, cause, solution formula come from Unity Foundations' help box.
