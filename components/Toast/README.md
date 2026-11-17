# Toast

A card that confirms a reversible action the person just took and offers Undo, counting up from the moment it happened; it floats at the bottom edge on web and phones and docks as the undo bar on the Mac.

## When to use

- After a reversible action that acts at once: approved, archived, moved, a mode changed. Every platform gets this undo surface.
- A passive confirmation with no action, only when the result is out of view. On web, show the change inline too.
- Not for failures (`InlineAlert`, `Notice`), decisions (`Modal`), long work (`ProgressBar`), or anything that happens while the app is in the background (a system notification).

## Anatomy

1. **Surface.** Floating: `popover` over `blur-floating` with `shadow-float`, `radius-card`, padding `card-padding-y` x `card-padding-x`, at most `size-modal-narrow` wide, at `z-toast`. Docked: the `card` fill in the pane, no blur, no shadow, full column width.
2. **Eyebrow** (optional). Eyebrow step in `text-tertiary` (APPROVAL SAVED).
3. **Title.** Body-strong in `text-primary`: what happened, with its object and count ("Approved 1 trace").
4. **Detail** (optional). Caption in `text-secondary`, tabular numerals: the consequence and the count-up ("Approved 12s ago").
5. **Actions.** Undo as a glass `Button`, then Dismiss as a link, `space-8` apart. At most one action besides Dismiss.
6. **Refusal** (optional). An `InlineAlert` under the row when Undo fails.

Text lines sit `space-2` apart; text to actions `space-16`. The floating **region** sits at the bottom center, `margin-compact` from the edges below 600px (`bp-medium`) and `margin-medium` above, always above a tab bar, navigation bar or `PromptComposer`, never over them.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Form | Docked card | Floating, max 450 | Floating, full width minus 16 | Snackbar slot, full width minus 16 | Docked card |
| Title, detail | `mac-body-strong`, `mac-caption` | `web-body-strong`, `web-caption` | `ios-body-strong`, `ios-caption` | `android-body-strong`, `android-caption` | `mac-label`, `mac-caption` |
| Buttons | 28 | 28 | 44 | 40 in a 48 target | 20 |
| Minimum height | Content | 48 | 56 | 48 one line, 68 two lines | Content |

## Variants

- **Undo.** Has Undo. Persists until the person acts, dismisses it, or the product's undo window closes. Never times out.
- **Passive.** No action. Leaves after 4 to 10 seconds scaled to its length (about 4 s plus 1 s per 10 words), paused while hovered or focused.
- **Docked.** The Mac's undo bar: a card at the top of the inspector, or at the foot of the main pane when the inspector is closed.

## States

- **Shown.** Title and detail; the detail counts up once a second.
- **Undoing.** Undo shows the `Button` busy state ("Undoing…"); Dismiss is disabled.
- **Refused.** An `InlineAlert` inside the card; the card stays.
- **Window closed.** When the product says undo is no longer possible, Undo goes away and the detail says why ("Upload may already have started."). The card stays until dismissed.
- **Replaced.** A newer toast replaces it. The older action stays undoable through Edit > Undo and `Mod+Z` while the product allows.

## Behavior

- One toast at a time. Never stack.
- Never take focus. `Mod+Z` undoes the last action while focus is outside a text field. On the Mac, Undo is the window's default button while the bar shows, so Return undoes. It is the app's only Return binding, and it sits on the safe action. A modal or a text field that owns Return keeps it. On web, `F6` moves focus into the toast region and Escape dismisses from inside; focus then returns where it was.
- Count up from the real instant and stop at a ceiling ("Approved 60s+ ago"). Never draw a countdown, a shrinking bar or a deadline the app cannot observe.
- Motion: the floating toast rises from the bottom edge on `spring-spatial` over `duration-spring-spatial` with an opacity fade, and leaves with a `duration-fast` fade on `ease-exit`. Under Reduce Motion it appears and leaves at once. Other elements never move with it.
- In the background: show no toast. Send a system notification at an honest interruption level (a finished run is Active; an approval that blocks work within the hour is Time Sensitive; suggestions are Passive; never Critical).

## Accessibility

- Keep a polite live region (`role="status"`) in the page before any toast arrives; the title and detail are read once. Keep the count-up outside the live region so it is not re-read every second.
- The Undo label names the action when "Undo" alone is ambiguous ("Undo approve"), from the product's copy.
- An actionable toast never times out, which keeps time limits out of the way (WCAG 2.2.1). A passive one repeats what it says somewhere inline.
- Contrast: text tokens over `popover` hold 4.5:1 over the worst ground; the `-hc` themes add the 1px `edge-hc` edge.
- Undo and Dismiss meet the touch floors on phones and tablets.

## Platforms

| | SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|---|
| Build | Docked card in the inspector; Undo with `.keyboardShortcut(.defaultAction)`; Edit > Undo | Custom glass card in `.safeAreaInset(edge: .bottom)`, painted per NDS-7 | `SnackbarHost` with a custom snackbar slot; `showSnackbar(actionLabel, duration = Indefinite)` for Undo | `.nr-toast-region` holding one `.nr-toast` |
| Announce | `AccessibilityNotification.Announcement` | `UIAccessibility.post(.announcement)` | Snackbar's polite announcement | `role="status"` |
| Native? | No (no system toast) | No (no system toast) | Native host, our surface | Custom |

## Do and don't

- Do say what happened with numbers: "Approved 1 trace", "Moved 12 files to Archive". A partial approve says what was withheld and is never drawn as a success.
- Do keep Undo available as long as the product can honor it.
- Don't confirm actions whose result is already in view.
- Don't put a failure, a link or a second action in a toast.
- Don't auto-dismiss a toast that has Undo.
- Don't cover navigation, the composer or a focused control.

## Source

Intentional addition. trace-commons has no transient toast: its undo bar card (`UndoBarCard` in `Views/Monitor/InspectorPrompts.swift`) is a persistent card at the top of the inspector with the core's eyebrow, a title, a detail that counts up through a one-second `TimelineView`, Undo bound to Return as the default action, a Dismiss link and the refusal under the row; "No timer removes it, and no countdown is drawn". Web and phone layouts have no inspector to dock in, and NDS-15 requires an undo toast on every platform, so the parent lifts the bar onto the floating layer there and keeps it docked on the Mac. Timing, one-at-a-time, polite announcement and no focus steal follow the M3 snackbar; the length-scaled passive timeout follows Unity's window banner (4 s by default); the undo stack and Edit menu follow the HIG undo and redo page; interruption levels follow the HIG notifications page.
