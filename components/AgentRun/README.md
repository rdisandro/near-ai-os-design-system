# AgentRun

A long-running agent task people can watch, pause and stop: its title, state, progress, the step it is on and the steps so far, with a compact form for sidebars, the menu bar and Live Activities.

## When to use

- Agent work that takes longer than about five seconds and keeps going when people look away: running tests, indexing a folder, a multi-step change.
- For a short wait inside an answer, use the status line in `Message`. A step that needs permission shows "Needs you" here and opens a `ToolCall`.
- For a file transfer or other measured work with no steps, use `ProgressBar`.

## Anatomy

1. **Card** (`Card`), `card-gap` 10 between parts.
2. **Head**: agent tile (`size-tool-tile` 22, `accent-tint`, `accent-text`), title (body strong, one line, truncates), meta line (status dot + state words + folder), elapsed time trailing (caption, `text-tertiary`, tabular, counts up).
3. **Progress**: a 4 (`space-4`) track on `well`, `radius-pill`. The fill is `accent-soft`, a 3:1 mark. Determinate width is the done fraction; indeterminate is a segment a third of the track wide sliding across on `duration-pulse` (derived).
4. **Now line**: 12 spinner and the step in words, "Step 3 of 6 · Reading failure log 9 of 14…" (caption, `text-secondary`, one line).
5. **Steps**: an ordered list, `space-6` apart. A 16 mark column: done is a check in `positive`, current a spinner in `accent-soft`, pending a 10 ring in `neutral`, needs you `caution`, failed a cross in `critical`. Step names in label type, an optional detail line (caption, `text-tertiary`), duration trailing (tabular).
6. **Actions**: Stop in the leading (cancel) position, then Pause or Resume. Quiet pills `--nr-h-control` tall on `control`.
7. **Background note** (caption, `text-tertiary`): what happens when the window closes.

**Compact**: one row on a quiet card: title, then the bar and now line, or the meta line; one control trailing.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Title | `mac-body-strong` 13 | `web-body-strong` 14 | `ios-body-strong` 17 | `android-body-strong` 16 | `mac-label` 12 |
| Steps | `mac-label` 12 | `web-label` 13 | `ios-label` 15 | `android-label` 14 | `mac-caption` 11 |
| Now line, times | `mac-caption` 11 | `web-caption` 12 | `ios-caption` 13 | `android-caption` 12 | `mac-micro` 10 |
| Buttons / target | 28 / 28 | 28 / 28 | 44 / 44 | 44 / 48 | 20 / 20 |
| Track | 4 | 4 | 4 | 4 | 4 |

## Variants

- **Card**: in the thread or a run's own view.
- **Compact row** (`nr-agent-run--compact`): a run list, the sidebar, the macOS menu-bar item.
- **Live Activity** (iOS): compact leading is the agent tile, compact trailing "3/6"; minimal shows "3/6"; expanded and Lock Screen show title, now line, bar and one control.
- **Summary**: when the run ends it keeps its steps and durations and adds the outcome.

## States

| State | Dot | Progress | Controls |
|---|---|---|---|
| Starting | `accent-soft` | indeterminate | Stop |
| Running | `accent-soft` | determinate once the step count is known | Stop, Pause |
| Needs you | `caution` | held | Review (opens the `ToolCall`) |
| Paused | `neutral` | held | Stop, Resume |
| Done | `positive` | full | Open |
| Stopped | `neutral` | held | Open, Run again |
| Failed | `critical` | held | Retry step, Open |
| Unknown | none; the product's unknown word | dash in place of the count | Reconnect |

Buttons: hover `control-hover`, pressed `brightness(0.92)`, disabled `opacity-disabled`, focus 2px `focus-ring`. Under `-hc` themes buttons and the track take the 1px `edge-hc` edge; forced colors fill with Highlight.

## Behavior

- **Pace**: start indeterminate and switch to determinate when the step count is known. Never switch between a bar and a circle, never fake an even pace, never show a time estimate you can't measure. Elapsed time counts up from a real start.
- **Stop** ends the run once the current tool call returns, and keeps finished work. If stopping would throw work away, confirm in a `Modal` (Keep running, Stop). Esc and Mod+. stop when the run has focus.
- **Pause** holds after the current step; Resume picks up there.
- **Background**: closing the window doesn't stop the run. It continues in the menu-bar item (macOS), a Live Activity (iOS), an ongoing notification (Android) or the tab title (web). Notify when it needs an answer and when it finishes, not per step. Never send a push for the same update. End the Live Activity at once and keep the summary 15 to 30 minutes.
- **Steps appear** as the agent plans them, entering with `spring-spatial`; the fill moves on `duration-standard` `ease-standard`. Under Reduce Motion nothing slides and the indeterminate segment holds still; the words carry progress.

## Accessibility

- The card is an `article` named by its title. The bar is `role="progressbar"` with `aria-valuemin`, `aria-valuemax` and `aria-valuenow` in steps and `aria-valuetext` in words ("Step 3 of 6, reading the failure logs"). Indeterminate omits `aria-valuenow`.
- The now line is `role="status"`: announce step and state changes, never each elapsed second. The current step has `aria-current="step"`.
- Marks, tile and spinner are hidden from assistive tech; state is always in words.
- In lists, controls name their run ("Stop summarizing this week's traces").
- `accent-soft` holds 3:1 on `pane-opaque`; step text uses text tokens at 4.5:1.
- The consumer supplies every word: title, state words, step names and details, times, note and button labels.

## Platforms

| | SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|---|
| In app | custom card, `ProgressView(value:)` restyled | same | custom card, `LinearProgressIndicator` | `div role="progressbar"` |
| Away from the app | `MenuBarExtra` ongoing item; an iPhone Live Activity also mirrors to the menu bar | ActivityKit Live Activity, one control through `LiveActivityIntent`; `BGContinuedProcessingTask` keeps it running | foreground service with an ongoing notification, `Notification.ProgressStyle` (Android 16 Live Updates) or `setProgress` | tab title prefix ("3/6 ·") |
| Needs you, finished | `UNUserNotificationCenter`, interruption level active | same; time sensitive only when an answer is due | notification with one action | Notifications API after permission |
| Start | App Shortcut | App Shortcut | app shortcut | command palette |

## Do and don't

- Do name the step being done and keep finished steps with their durations.
- Do offer Pause as well as Stop when stopping loses work.
- Do keep one control in Live Activities and notifications: Stop, or Review when it needs you.
- Don't show a spinner alone for work longer than five seconds; use the bar.
- Don't approve a step that needs permission on the agent's behalf.
- Don't alert on every step or count down to a deadline you can't see.

## Source

Intentional addition: trace-commons has `GlassSpinner` and `GlassSkeleton` (Feedback.swift) and `GlassStepProgress` (Navigation.swift, where steps "are not chosen, they are reached"), but no determinate progress or long-running task surface, and Near AI agents run for minutes to hours. Built from HIG Progress indicators (prefer determinate; Pause plus Cancel when cancelling loses progress), Live Activities (tasks up to 8 hours, one control, update only on change, end at once), Notifications and App Shortcuts; M3 progress indicators for waits over five seconds and the loading indicator for 200 ms to five seconds; Unity App UI `LinearProgress` (determinate and indeterminate).
