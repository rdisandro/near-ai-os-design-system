# Chip

A compact pill, always in a set, that filters a collection, holds a token the person typed, offers a suggested prompt or shows a status.

## When to use

| Kind | Use it to | Example |
|---|---|---|
| Filter | Narrow a list; one or several on | Shared 96, Kept 30, Failed 2 |
| Input | Hold a typed token, such as a prompt scope | @near/nearcore, in: Traces |
| Suggestion | Offer a prompt the product suggests; starts with a verb | Explain the failing test |
| Status | Show a state word beside a title; read-only | Watching, Paused |

- Use a `Button` for the steps of a task, `Tag` for verdicts and `Badge` for counts owed.
- Never show one chip alone.

## Anatomy

1. **Container**: 26 (`size-control`), `radius-pill`, `space-10` padding. Fill `neutral-tint` for filter and status, `control` for suggestion.
2. **Leading mark**: a 12 check on a selected filter, or a 6 dot on a status chip.
3. **Label**: the label step, semibold for filter and suggestion; mono for input and status chips, which hold identifiers and state words.
4. **Count** (filter, optional): tabular, regular weight, `text-tertiary`.
5. **Remove** (input): a round button the chip height − 4, a 12 cross in `text-tertiary`, with its hit area grown to `--nr-target`.

Chips in a set sit `--nr-gap` apart (8 regular, 12 touch).

## Sizes by density

| | Compact (macOS) | Regular (web) | Touch iOS | Touch Android | Dense |
|---|---|---|---|---|---|
| Height | 26 | 26 | 32 in a 44 target | 32 in a 48 target (M3) | 20 |
| Padding | 10 | 10 | 12 | 12 | 6 |
| Label | `mac-label` | `web-label` | `ios-label` | `android-label` | `web-caption` |

## Variants

Filter, input, suggestion and status, as above. Filter sets are single-select or multi-select; never both on one page.

## States

| State | Look | Tokens |
|---|---|---|
| Hover | Fill replaced, label lifts | `control-hover`, `text-primary` |
| Pressed | Darkens | brightness 0.92 |
| Selected filter | Accent tint, accent ink and a leading check | `accent-tint`, `accent-text` |
| Selected input token | Accent tint (Backspace before it selects it) | `accent-tint` |
| Focus | 2px ring | `focus-ring` |
| Disabled | Dimmed, no hover | `opacity-disabled` |
| Status | Dot and ink in the status pair | `positive` / `positive-text`, `caution` / `caution-text`, `critical` / `critical-text`, `neutral` / `text-secondary` |
| Increased contrast | 1px edge | `edge-hc` |

## Behavior

- Filter chips wrap to a second row. Past two rows, scroll the set sideways with a leading "Show all", or move the filters to a side sheet.
- Input chips: Return or a comma turns typed text into a token. Backspace at the start of the text selects the last token and a second Backspace removes it. Clicking a token turns it back into text to edit.
- Suggestion chips insert or send their prompt. The set may change after each answer.
- On compact touch widths, the whole chip does its one action; a separate remove target appears from medium widths.
- Motion: fills change on `duration-fast`. Chips that arrive or leave fade on `duration-fast` and never slide under Reduce Motion.

## Accessibility

- Filter: `<button aria-pressed>` in a `role="group"` named by the consumer; a single-select set is a `radiogroup` of `radio`s.
- Input: the token's text plus a remove button named by the consumer ("Remove @near/nearcore"). With only a remove action, the chip is one focus stop.
- Status: plain text; the dot is hidden.
- Selection never rests on the tint: the check and `aria-pressed` mark it.
- Keep at least 8 between chips on touch so every chip gets its full target.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| Painted capsules (`GlassChip`, filter pills); `NSTokenField` behavior for input tokens | Toggle-style capsule buttons for filters; `searchable(text:tokens:)` tokens for input | `FilterChip`, `InputChip`, `SuggestionChip`, colored from the tokens | `.nr-chip-group` of `.nr-chip` buttons or spans (type class on each) |

## Do and don't

- Do keep labels short, 20 characters or fewer, without articles.
- Do write filter labels as the things they include (Shared, Kept).
- Don't use a chip for the final step of a task.
- Don't mix single-select and multi-select sets on one page.

## Source

`GlassChip` in Indicators.swift (mono pill, 6pt dot, status ink, neutral tint in flat); the History filter pills (`HistoryFilterPill` in HomeViews.swift: label and count, the chosen one lit, wrapping onto a second line); Gateway's redaction chips. The parent draws the selected filter on `accent-tint` with a check (the token's stated use) in place of the source's solid selected fill, widens spacing to 8 for touch targets (M3 chips), and adds input and suggestion chips (HIG token fields, M3 chips).
