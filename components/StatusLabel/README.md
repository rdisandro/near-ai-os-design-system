# StatusLabel

A status dot beside its words, for any live state a person reads at a glance (Watching, Paused, Ask, Leaves for an outside model); it is the only way the system shows status.

## When to use

- The current state of a thing: a watcher, a folder's contribution mode, a model route, a connection, an agent run.
- Rows, inspector facts, card heads, legends, picker options and the value of a tab.
- Use `Tag` for a settled verdict about an item (Verified, Contributed). Use `Badge` for a count of decisions owed. Use `Notice` when the state needs a sentence or a fix.
- Never show status as a colored fill, colored words or a dot alone with nothing that names it.

## Anatomy

1. **Dot.** An 8px circle (`space-8`) in the tone's mark color. Hidden from assistive tech.
2. **Gap.** `inline-gap` (6px); 8px on touch.
3. **Words.** The label step in `text-secondary`. Words never take the tone's color.
4. **Sub-line** (lead variant only). Caption step in `text-secondary`, aligned under the words, not under the dot; dot to words `space-10`, line gap `space-2`.

Optional rings on the dot: **halo** is a 2px `hairline` ring that lifts a dot off a busy ground (legend cells); **ring** is a 3px ring in the tone's `-tint` (`space-6 / 2`) for the one status that heads a card.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Dot | 8 | 8 | 8 | 8 | 6 (`space-6`) |
| Dot to words | 6 | 6 | 8 | 8 | 6 |
| Words | `mac-label` | `web-label` | `ios-label` | `android-label` | `mac-caption` |
| Lead line + sub-line | `mac-body-strong` + `mac-caption` | `web-body-strong` + `web-caption` | `ios-body-strong` + `ios-caption` | `android-body-strong` + `android-caption` | `mac-label` + `mac-caption` |

The label takes the height of its row. It is not a control and has no target of its own.

## Variants

| Tone | Mark | Means | Gateway examples |
|---|---|---|---|
| Positive | `positive` | On, working as asked | Watching, Verified, Shared |
| Caution | `caution` | Waits on the person, needs a look | Ask, Pending, Sign-in needed |
| Critical | `critical` | Failed, or data leaves the device | Leaves for an outside model, No proof, Stopped |
| Neutral | `neutral` | Off, paused, not used | Paused, Never, Kept |

- **Strong.** Semibold words. The title of a `Notice`.
- **Lead.** Ringed dot, a body-strong line and a caption sub-line ("Watching" over "3 traces waiting for you"). The head of a status card.
- **Legend.** Halo dots in a row (Shared, Kept) beside a chart or count.
- **Lone dot.** A dot with no visible words, on a tab title or a picker pill. Allowed only when the host's accessible value carries the words and the same words are visible one step away (the inspector, the expanded pill).

## States

- **Known.** Dot plus words.
- **Unknown.** No dot. The product's unknown word ("Unknown") or a dash. Never "On", never zero, never a guessed tone. Unknown is neither on nor off.
- **Stale.** When the source stops answering, fall back to unknown. A dead or unanswered source never draws as healthy.
- **Interactive host.** The label has no hover, pressed or focus state. When the whole row or card is a button, the row owns those states and the label sits inside it.

## Behavior

- The dot and words change together, at once. No pulse, blink or glow to mean "live"; a live state is a word ("Watching").
- Motion: none. Nothing to remove under Reduce Motion.
- Truncate the words only at the end and only in a fixed-width column; give the full words as a tooltip and in the accessible name.

## Accessibility

- One combined element: the row reads "Model route, Leaves for an outside model". The dot is `aria-hidden` on web and `accessibilityHidden` on Apple platforms.
- The consumer supplies the words from the product's copy, including the accessible value of a lone dot. The component authors no words.
- Contrast: tone marks hold 3:1 on `pane-opaque` in every theme; words in `text-secondary` hold 4.5:1 over the worst ground (7:1 in the `-hc` themes). A dot beside words is supplementary; a lone dot must meet 3:1 by itself.
- Announce a change only when it results from something the person started elsewhere (put that label in a `role="status"` region). Do not announce background flips on a timer.
- Forced colors: the dot draws in `CanvasText`; the words still carry the state.

## Platforms

| | SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|---|
| Build | Custom `GlassStatusLabel`: `HStack` of `GlassStatusDot` and `Text`, `.accessibilityElement(children: .combine)` | The same custom view; in a `List` use `LabeledContent` with the label as the value | Custom `Row` of a `Box` dot and `Text`, `Modifier.semantics(mergeDescendants = true)` | `<span class="nr-status-label">` with an `aria-hidden` dot |
| Lone dot | `accessibilityValue` on the tab or picker | `accessibilityValue` | `stateDescription` | `aria-label` or visually hidden text on the host |
| Native control? | No (custom) | No (custom) | No (custom) | No (custom) |

## Do and don't

- Do name the state as people say it: "Paused until 9:00", not "Status: inactive".
- Do use one word per state across every surface of a product.
- Do keep critical for failures and for data leaving the device, so it stays rare.
- Don't color the words, tint the row or add a colored border.
- Don't draw a dot for a value nobody has reported.
- Don't use a tone for emphasis or decoration.

## Source

`GlassStatusDot` and `GlassStatusLabel` in `Components/Indicators.swift` ("A dot and its label: the only way status is shown"); `GlassStatus` tones in `Styling/GlassStyle.swift` (on, ask, off, outside map to positive, caution, neutral, critical); the halo from `GlassLegendCell` in `Components/Containers.swift`; the lead layout from the Home status card in `Views/Monitor/HomeViews.swift`. The unknown and fail-closed rules come from the trace-commons spec ("Appearance") and the R15 plan's global constraints.
