# ProgressBar

A thin track that fills from the leading edge as measured work advances, with its value in words and a Stop or Pause beside it; use it for work that can be counted or that takes longer than about 5 seconds.

## When to use

- A known total: bytes of a model download, traces in an upload, steps in an agent run with a known plan ("Step 3 of 7").
- The opening phase of work that will become measured: start indeterminate, then switch the same bar to determinate. Never switch between a ring and a bar.
- Use `Spinner` for short waits with no measure. Use `StepProgress` for steps a person moves through. One bar for a group of tasks, never one per row.

## Anatomy

1. **Label.** Label step in `text-primary`: what is happening, specifically ("Uploading 3 of 8 traces").
2. **Value.** Caption in `text-secondary`, tabular numerals, trailing: a percent, a count of a total, or the step.
3. **Track.** `well`, 4px tall (`space-4`), `radius-pill`.
4. **Fill.** `accent-soft`, same radius. `neutral` when paused, `critical` when failed.
5. **Control** (optional). Stop, Pause or Resume as a glass `Button`, trailing the track, `space-8` from it. Cancel as a link when paused.
6. **Status line** (optional). Caption in `text-secondary`: time left when it is reliable, or why it is waiting.

Parts stack with `space-6`. Place the bar right after the control that started the work, or on the top edge of the container it is filling.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Track | 4 | 4 | 4 | 4 (M3) | 4 |
| Thick track | 8 | 8 | 8 | 8 | n/a |
| Label, value | `mac-label`, `mac-caption` | `web-label`, `web-caption` | `ios-label`, `ios-caption` | `android-label`, `android-caption` | `mac-caption` |
| Control | 28 | 28 | 44 | 40 in a 48 target | 20 |

## Variants

- **Determinate.** The default. The fill is the share of the total done.
- **Indeterminate.** Only before the total is known: a segment half the track's width slides across over `duration-pulse` on `ease-standard`.
- **Thick.** An 8px track (`space-8`) for a large window or a hero moment.
- **Wavy** (Android and web only). M3 Expressive's wavy indicator for one hero moment per product, such as a first contribution: 10dp container, 3dp amplitude, 40dp wavelength (`LinearWavyProgressIndicator`). Flat under Reduce Motion. Never on Apple platforms.

## States

| State | Fill | Words | Controls |
|---|---|---|---|
| Running | `accent-soft`, growing | Label, value, time left if reliable | Stop, or Pause |
| Stalled | Holds its width | Status says why ("Waiting for the network.") | Stop |
| Paused | `neutral` | "Paused. It picks up where it stopped." | Resume, Cancel link |
| Failed | `critical` | `InlineAlert` saying what happened to the partial work | Try again |
| Done | The bar goes | The result appears; a `Toast` with Undo if reversible | |

Under the `-hc` themes the track gets the 1px `edge-hc` inset edge.

## Behavior

- The fill grows on `duration-standard` with `ease-standard` and jumps under Reduce Motion. The indeterminate segment is hidden under Reduce Motion and the words carry the state.
- Pace evenly. Smooth uneven reports; never race to 90% and stall. When work stalls, the fill stops and the words say why.
- Stop when stopping loses nothing. Pause and Cancel when cancelling loses progress, and confirm the loss with a `Modal` ("Cancel the download? The 4.1 GB downloaded so far will be deleted.").
- Escape and `Mod+.` stop a running agent run (NDS-14).
- People can leave. The work continues, the bar is back when they return, and a long job may notify when done.

## Accessibility

- `role="progressbar"` on the track, named by the label (`aria-labelledby`), with `aria-valuemin`, `aria-valuemax`, `aria-valuenow` and an `aria-valuetext` in words ("3 of 8 traces"). Indeterminate omits `aria-valuenow`.
- Announce milestones politely (started, halfway, done, failed), never every percent.
- The value is always in words beside the bar, so the track needs no stop dot. The fill (`accent-soft`) holds 3:1 on `pane-opaque`.
- The consumer supplies the label, value, status and button words from the product's copy.
- Control targets follow the density's floor.

## Platforms

| | SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|---|
| Build | `ProgressView(value:total:)` with `.linear` style, tinted `accent-soft`, or a painted track to match the well | `ProgressView(value:total:)` | `LinearProgressIndicator(progress = { p }, color, trackColor)`; `LinearWavyProgressIndicator` for the hero | `.nr-progress-bar` with `role="progressbar"`, or a styled `<progress>` |
| Native? | Native | Native | Native | Custom |

## Do and don't

- Do say what is moving, with counts and units.
- Do keep the bar in one place for one kind of work.
- Do offer Stop, and Pause when stopping would lose work.
- Don't fake progress or estimates. Show time left only when it is reliable.
- Don't make an indeterminate wait look like measured progress.
- Don't put a bar in every row of a list.

## Source

Intentional addition. trace-commons has no determinate progress component (its research inventory notes "No determinate progress bar component exists"); its only progress shapes are the indeterminate `GlassSpinner` and `GlassStepProgress` for first-run steps. Near AI products need a measured indicator for downloads, uploads and agent plans. The HIG progress indicators page prefers determinate progress, asks for even pacing, specific words and Stop or Pause; M3 uses progress indicators for waits over 5 s and adds the wavy shape for expressive moments; Unity Foundations places the bar after the control that starts the work and uses one bar for a sequence.
