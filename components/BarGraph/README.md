# BarGraph

A two-series column chart drawn as a tapered dot matrix on an opaque plot: the first series rises above one axis and the second hangs below it, one column per period, with legend cells that read out the column under the pointer.

## When to use

- Two opposing counts per period that people compare at a glance: Shared and Kept traces per day (Gateway), calls answered and calls refused per hour, tokens in and tokens out.
- Small, glanceable plots in a pane footer, an inspector or a menu-bar panel, from 7 to about 42 columns.
- For one series use a single `StatCard` or a plain column chart; for exact values use a `DataTable`; for trends over many points use a line chart.

## Anatomy

1. **Plot ground**: `surface-chart` (opaque, never glass), `radius-card` 16, padding `space-10` by `space-12` (NDS-20).
2. **Axis**: one 1px rule in `chart-grid` across the plot at the column midline. No gridlines, no value axis: the readout carries exact numbers.
3. **Column**: one per bucket, `space-6` apart (`space-2` when thin). Height 97: 7 rows above and 7 below at a `space-6` pitch, `space-6` clear at each end, and the 1px axis (2 x (7 x `space-6` + `space-6`) + 1).
4. **Dots**: 4 (`space-4`) in 3 columns `space-2` apart; thin graphs (more than 14 buckets) use 1 column of 3 (`space-6` / 2). Unlit dots are `chart-grid`. Lit dots above are `data-1`, below `data-2`.
5. **Taper**: a value lights `value / max x 7` dots from the axis out. Each lit dot's opacity is 0.35 + 0.65 x (row + 1) / tip, so dots brighten toward the tip; the last dot carries the remainder as a partial dot (at least 0.35), so 9 and 11 still differ. A count of one always lights a dot. The scale is the largest bucket, never below the product's floor (5 in Gateway), so small counts stay short.
6. **Labels**: under each column, caption step (micro when thin), `text-tertiary`, never wrapped or cut; centred on the column and free to run past it. A thin graph labels a few columns only, and its first and last labels hug the outer edges.
7. **Legend and readout**: a row of two `StatCard` legend cells above the plot (dot, series name, value). They show the totals at rest and the hovered or focused column's values while it is read.
8. **Range line**: caption, `text-secondary`, under the plot: the window ("Oct 3 – Oct 13") or the column being read ("Sun, Oct 11").

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Plot height | 97 + labels | 97 + labels | 97 + labels | 97 + labels | 97, thin |
| Column gap | 6 (2 thin) | 6 (2 thin) | 6 (2 thin) | 6 (2 thin) | 2 |
| Labels | `mac-caption` (`mac-micro` thin) | `web-caption` (`web-micro`) | `ios-caption` (`ios-micro`) | `android-caption` (`android-micro`) | `web-micro` |
| Readout target | the column | the column | the whole plot (scrub) | the whole plot (scrub) | the column |

## Variants

- **Regular**: up to 14 buckets, 3 dot columns per bucket (a week, 11 days, 24 hours in 2-hour buckets).
- **Thin** (`.nr-bar-graph--thin`): more than 14 buckets, 1 dot column (42 days).
- **Paused or unreadable**: when data could not be read, draw unlit columns and say so in the range line; never draw missing data as zero activity.

## States

| State | Treatment |
|---|---|
| Rest | legend shows totals; range line shows the window |
| Read (hover, focus, touch) | the column takes a `neutral-tint` wash (never an outline); its label turns `text-primary`; the legend and range line show its values |
| Window change | the new window slides in from the side it lies on over `duration-spring-spatial` with `spring-spatial`, fading in; a zoom swaps in place |
| Loading | unlit columns and the product's line in the range line |
| Unknown total | the legend value is "—" when a total is incomplete, never a partial count shown as a total |
| Increased contrast | the plot's 1px `edge-hc` edge |

## Behavior

- Pointer: hovering a column reads it; leaving the plot returns to totals.
- Keyboard: the plot is one tab stop; Left and Right move between columns, Home and End jump; the column being read is the active descendant. Leaving the plot returns to totals.
- Touch: drag across the plot to scrub; lift to keep the last column read; tap outside to return to totals.
- Window controls (previous, next, zoom, now) sit in a row under the plot and are separate `IconButton`s.
- Under Reduce Motion the window swaps without sliding; the wash and label colors change with no transition.

## Accessibility

- The plot is a group named with a one-sentence summary from the product ("Traces shared and kept per day, October 3 to 13"). Each column is one element whose name is the product's description ("Sun, Oct 11: 9 shared, 4 kept").
- Identity never rests on color: the two series are told apart by position (above or below the axis) and named in the legend. Gateway's Shared and Kept pair (purple #8a3dff over blue #3a7bd5 in dark, its own product colors since NDS-22) measures delta E 7.0 for deuteranopia, legal only with this secondary encoding.
- Series dots at full strength hold 3:1 on `surface-chart`; the fainter dots near the axis are a taper, and the readout and the table view carry exact values.
- Offer a table view (`DataTable`) of the same buckets as the text alternative (NDS-20).
- The consumer supplies bucket labels, descriptions, series names, the summary and the range words.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| `GlassBarGraph` (a `Canvas` per bucket, `GlassBarSlide` transitions); `accessibilityChartDescriptor` for Audio Graphs | The same `Canvas` drawing with a drag gesture for scrubbing; or Swift Charts `PointMark`s on a fixed grid | `Canvas` drawing the matrix; `pointerInput` for hover and drag; `semantics { contentDescription }` per bucket | HTML or SVG built from data (`.nr-bar-graph__bucket`, `__dots`, `__dot--up`, `__dot--down`), the taper set through `--nr-dot-alpha` |

## Do and don't

- Do plot on `surface-chart`. Don't draw the matrix straight on glass.
- Do keep `data-1` above and `data-2` below in that order. Don't swap colors when a filter changes.
- Do keep the readout in the legend. Don't add a value axis or a number on every column.
- Do label only a few columns in a thin graph. Don't wrap or shorten labels.

## Source

`GlassBarGraph`, `GlassBarBucket` and `GlassBarSlide` in Indicators.swift (7 dots per half column, 96pt columns, 6pt matrix ends, 3 columns of r1.9 or 1 of r1.5 above 14 buckets, taper 0.35 + 0.65 x (row + 1) / tip, unlit ink 9%, hover wash never an outline) and the Traces graph footer in MonitorShell.swift (legend cells read out the hovered bucket; scale floor 5) [trace-commons §2.13, §4.9, §5.3]. Plot ground, palette order and the table alternative from NDS-20; HIG charts for scrubbing and accessibility labels.
