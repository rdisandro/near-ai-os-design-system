# StatCard

A single figure with its name: an eyebrow label over a bold tabular value on a card, and its compact form, the legend cell, a well pill with a series or status dot used in rows of two or three and as a chart's readout.

## When to use

- A headline count or amount people check at a glance: Waiting 14, Contributed 1,279, Spent this month 4.21 NEAR.
- A row of related totals over a list or chart: Calls 1,284 · Verified 1,279 · Priced 1,284 as three legend cells.
- The legend of a two-series chart that also reads out the bucket under the pointer (`BarGraph`).
- When the story is one number, use a stat card instead of a one-bar chart. For many figures, use a `DataTable`.

## Anatomy

**Stat card**
1. **Card**: `card` fill, `radius-card` 16, padding `space-10` by `space-12`.
2. **Label**: eyebrow step, uppercase, `text-tertiary`; wraps at spaces to at most two lines, never inside a word.
3. **Value**: heading step, bold, tabular figures, `text-primary`, one line, truncated at the end (units stay with the figure: "4.21 NEAR").
4. **Note** (optional): caption, `text-secondary`, `space-2` under the value: the condition behind a figure ("Shown once it is accepted."), a second scope ("{amount} across your account" under this Mac's figure) or a change in words ("12 more than last week").
5. **Watermark** (optional): the card's glyph at 58, −12°, 55% `accent-soft`, bleeding off the trailing bottom corner behind the words and clipped by the card (see `Card`). Gateway's Home tiles use it in place of an icon column.

**Legend cell** (`.nr-stat-card--legend`)
1. **Well**: `well` fill, `radius-pill`, height `size-control-large` 28, padding `space-10`.
2. **Dot**: 8, with a 2px `neutral-tint` halo; a series color (`data-1`, `data-2`, `data-3`) or a status mark (`positive`, `caution`, `critical`).
3. **Label**: `text-secondary`, one line, truncated at the end; `inline-gap` 6 after the dot.
4. **Value**: semibold, tabular, `text-primary`, never truncated.
Rows: `.nr-stat-card-row` lays cards in equal columns at least 128 wide (2 x `space-64`), `card-gap` apart; `.nr-stat-card-row--legend` gives each cell an equal share, `space-6` apart.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Card padding | 10 / 12 | 10 / 12 | 12 / 16 | 12 / 16 | use legend cells |
| Label | `mac-eyebrow` | `web-eyebrow` | `ios-eyebrow` | `android-eyebrow` | - |
| Value | `mac-heading` bold | `web-heading` | `ios-heading` | `android-heading` | - |
| Legend cell height | 28 | 28 | 28 visible, 44 target when tappable | 28 visible, 48 target when tappable | 20 (`size-control-dense`) |
| Legend type | `mac-label` | `web-body` / `web-body-strong` | `ios-label` | `android-label` | `web-caption` |

One hero figure per screen may use `hero-figure` (web and tablet) instead of a stat card.

## Variants

- **Stat card**, with or without a note.
- **Legend cell** with a series dot (chart legends) or a status dot (Verified, Pending).
- **Interactive stat card**: when the figure opens its list (Waiting opens the queue), the card becomes an interactive `Card` with the same parts.

## States

| State | Treatment |
|---|---|
| Default | as above |
| Unknown | "—" or the product's unknown word, with a note that says why when the product has one; never 0 |
| Loading | "—" until the first read; a later read keeps the last value and the note says when it was read |
| Readout (legend cell in a chart) | the value shows the hovered or focused bucket, then returns to the total |
| Increased contrast | 1px `edge-hc` inset edge on the card and the well |

## Behavior

- Static by default; no tab stop.
- Values update in place without animation; tabular figures keep the width steady while counts tick.
- A change is described in words in the note. The value is never colored to show good or bad. (Gateway's Credit tile has colored its day-over-day change green or red since 2026-10-12; that is a product exception the parent does not adopt, and Gateway later dropped the "since yesterday" line, owner 2026-10-29.)
- An unknown figure reads "—". While the figure waits on sign-in the card is head-only and says so in words (see *Feedback and states*, signed out).
- Nothing moves.

## Accessibility

- Each stat card or legend cell is one element read as "label, value" ("Waiting, 14"; "Verified, 1,279"). The dot is hidden.
- A legend cell used as a chart readout sits outside the plot and is not a live region; the plot's focused bucket carries the spoken value.
- `text-tertiary` labels and `text-secondary` legend labels hold 4.5:1 on `card` and on `well` over the worst ground. Series dots hold 3:1 on their ground and always sit beside words.
- The consumer supplies labels, values (already formatted with units and separators) and notes.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| `GlassStatCard(label, value:)` and `GlassLegendCell(label, value:, status:)`; `.monospacedDigit()`; `.accessibilityElement(children: .combine)` | The same views on the opaque screen pane | A filled `Card` with two `Text`s (`FontFeature` "tnum"); the legend cell as a `Surface(shape = CircleShape)` row; `Modifier.semantics(mergeDescendants = true)` | `.nr-stat-card`, `.nr-stat-card--legend`, `.nr-stat-card-row` |

## Do and don't

- Do let the label wrap to two lines. Don't cut a word ("CREDIT PEN…").
- Do show a dash for an unknown figure with the reason nearby. Don't show 0.
- Do keep the value in text colors. Don't paint it green or red.
- Do keep two or three legend cells per row. Don't use a legend for a single series.

## Source

`GlassStatCard` in StatCard.swift (eyebrow label wrapping at spaces over a heading-bold tabular value, 10 by 12 padding, card tier) and `GlassLegendCell` in Containers.swift (28pt well pill, haloed 8pt dot, label shrinking then truncating, tabular semibold value); Home's three stat cards and the Private AI ledger's Calls / Verified / Priced cells [trace-commons §4.8, §5.5, §5.6]; the watermark and the account-wide Credit note from #1460 and #1888. Tabular figures are kept for stat values because they update live.
