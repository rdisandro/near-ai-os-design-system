# EmptyState

A centered glyph, sentence and at most one action that explain why a list or region has nothing in it and what will fill it ("Nothing is waiting."); use it only after the source has answered with nothing.

## When to use

| Kind | When | Glyph | Action |
|---|---|---|---|
| Blank | Nothing exists yet | Yes | Optional, one ("Add a folder") |
| Filtered | A filter or search hides everything | No | One: clear the filter |
| Idle | Nothing is selected | No | None ("Select a trace to see what it would send.") |

- Not for loading (`Spinner`, `Skeleton`), not for a failed read (`Notice` with Try again), not for an unknown value (a dash).
- First-run starter content belongs in a `Card` flow, not in an empty state. A surface that has not started yet (Insights before any traces) uses `GetStartedCard` in place of its content (NDS-39); its empty state is for "nothing here" once the surface is running.

## Anatomy

1. **Glyph** (blank only). 22px (`size-tool-tile`) in `text-tertiary`, from the product's glyph set; 40px (`space-40`) on a full screen. Never a warning or error glyph.
2. **Title.** Body-strong in `text-primary`. A full sentence with a period.
3. **Detail** (optional). Caption in `text-secondary`: what will appear and how, and its data consequence ("Nothing is sent unless you say so.").
4. **Action** (optional, one). A `Button`, usually a link or glass.

A centered column, `space-4` between glyph, title and detail, `space-8` above the action. Padding `space-24` on top and `space-16` at the sides, at most `size-panel-width` (380px) wide. The inline variant pads `space-12` inside a card; the screen variant pads `space-40` and uses the 40px glyph.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Glyph | 22 | 22 | 40, or native | 40 | 16 |
| Title | `mac-body-strong` | `web-body-strong` | `ios-body-strong` | `android-body-strong` | `mac-label` |
| Detail | `mac-caption` | `web-caption` | `ios-caption` | `android-caption` | `mac-caption` |
| Padding | 24 x 16 | 24 x 16 | 40 x 16 | 40 x 16 | 12 x 12 |
| Action | 28 | 28 | 44 | 48 | 20 |

## Variants

- **Blank, filtered, idle.** The three kinds above.
- **Inline.** Inside a card or a list's frame (`nr-empty-state--inline`).
- **Screen.** A whole phone screen or pane (`nr-empty-state--screen`).

## States

- **Shown** only when the source has answered and the answer is empty. While the answer is pending, show the loading state; when the read failed, show a `Notice`.
- **Filtered** names the filter and how many items it hides ("No traces match “Failed”." / "12 traces are hidden by this filter.").
- **Increased contrast.** The text tokens step up with the theme; there is no surface of its own to edge.

## Behavior

- No motion.
- The action is the only focus stop. After Clear filter, focus moves to the first row that returns.
- When new items arrive, the list replaces the empty state in place.
- Keep the empty state where the list would be, so the layout around it does not shift.

## Accessibility

- The title is a heading at the region's level, or plain text in a region named by its section heading.
- The glyph is decorative and hidden from assistive tech.
- When a filter or search empties the list, announce the title once in a polite live region.
- The consumer supplies the title, detail and action words from the product's copy.
- Contrast: `text-primary` and `text-secondary` hold 4.5:1 over the worst ground (7:1 in the `-hc` themes); the glyph in `text-tertiary` is supplementary.

## Platforms

| | SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|---|
| Build | Custom `VStack` (glyph, title, caption), as in Traces; `ContentUnavailableView` where glass type is not needed | `ContentUnavailableView(label:description:actions:)`; `ContentUnavailableView.search` for no results | Custom `Column`, centered | `.nr-empty-state` |
| Native? | Custom | Native | Custom | Custom |

## Do and don't

- Do say what will appear here and how it gets here.
- Do state data consequences plainly and without promises.
- Do offer the one action that fills or reveals the list.
- Don't use warning or error glyphs, red, or critical tones.
- Don't merge an empty state with a notice; a notice explains a failure, an empty state explains a condition.
- Don't show counts of zero, illustrations that crowd the words, or more than one action.

## Source

The Traces empty tree (`emptyTree` in `Views/Monitor/TracesViews.swift`): a `tray` glyph at 22 in `textTertiary`, a body-strong title, a caption detail, 4pt gaps, 24pt above, with the core's `nothing_waiting` and `nothing_waiting_detail` words from `shell_words_copy.rs`. The empty, loading, error and unknown ladder is trace-commons cross-screen pattern 12. The blank, idle and day-0 kinds, centered layout, maximum width and the ban on error icons come from Unity Foundations' empty states; `ContentUnavailableView` is the native iOS form.
