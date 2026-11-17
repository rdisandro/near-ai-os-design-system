# SegmentedControl

A row of two to five equal-width segments in a well, for choosing one of a few closely related values that apply at once, such as Appearance with Light, Dark and System.

## When to use

- Use it for two to five short values, all visible, that change a setting or a view at once. About five fit on a phone.
- Use `Tabs` for a window's main sections and `TabBar` for an app's.
- Use `Select` for longer lists, `Switch` for on/off and buttons for actions. Never mix action segments with value segments.

## Anatomy

1. **Track**: `well`, `radius-pill`, 30 tall (`size-segmented-track`), 2 padding, 2 between segments.
2. **Segment**: 26 tall, `space-8` padding, `radius-pill`, all as wide as the widest label. The label step; unselected `text-tertiary`, `text-primary` on hover; selected `accent` with `text-on-accent` at semibold.
3. **Dot** (optional): 6 (`space-6`), a status mark after the title. The segment's accessible description carries its words.
4. **Badge** (optional): decisions owed only, as a subtle `Badge`.

## Sizes by density

| | Compact (macOS) | Regular (web) | Touch iOS | Touch Android | Dense |
|---|---|---|---|---|---|
| Track | 30 | 30 | system (`Picker(.segmented)`) | 40 in a 48 target (M3 connected group) | 20 |
| Segment | 26 | 26 | system | 40 | 16 |
| Web touch track | none | none | 44 `size-control-touch` | 44 | none |
| Label | `mac-label` | `web-label` | `ios-label` | `android-label` | `web-caption` |
| Target | 28 | 28 | 44 | 48 | 20 |

## Variants

- **Well** (default): hugs its segments, each as wide as the widest.
- **Fill** (`--fill`): spans its container with equal segments.
- **Floating** (`--floating`): over a map or canvas. The `control` fill with `blur-floating` and `shadow-float`; segments hug their labels with `space-12` padding; unselected labels `text-secondary`.
- **Icon segments**: a glyph per segment with a tooltip and an accessible name. Never mix glyphs and words in one control.

## States

| State | Look | Tokens |
|---|---|---|
| Hover | Label lifts | `text-primary` |
| Pressed | Darkens; selected takes the pressed accent | brightness 0.92, `accent-pressed` |
| Selected | Accent fill, light label, semibold | `accent`, `text-on-accent` |
| Focus | 2px ring round the focused segment | `focus-ring` |
| Disabled segment | Dimmed, skipped by arrows | `opacity-disabled` |
| Increased contrast | 1px edge on the track | `edge-hc` |

## Behavior

- The control is one tab stop. Arrow keys move the selection and apply it; Home and End jump to the ends.
- The choice applies at once (Gateway applies Appearance immediately).
- Motion: this component swaps the fill on `duration-fast`. Native thumbs that slide (iOS, M3) use `spring-spatial-fast`. Nothing moves under Reduce Motion.

## Accessibility

- Web: `role="radiogroup"` with the consumer's name, segments `role="radio"` with `aria-checked` and a roving `tabindex`. For views, use `Tabs` (`tablist`).
- Dots and badges are hidden; their words go in the segment's description, supplied by the consumer.
- The selected segment is marked by its fill, its `text-on-accent` label and its semibold weight. In Gateway dark the accent fill sits at 1.09:1 on the pane (flagged), so the weight and the announced state carry it.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| `GlassSegmentedTabs` in panes; `Picker(.segmented)` in toolbars and inspectors | `Picker(.segmented)` with the system look | A connected `ButtonGroup` of toggle buttons, single select (segmented buttons are deprecated), colored `accent` and `well` | `.nr-segmented-control` with `.nr-segmented-control__segment` buttons (type class on each) |

## Do and don't

- Do keep labels to one or two words of similar length.
- Do pick a default.
- Don't use it to navigate between screens.
- Don't put more than five segments on a phone.

## Source

`GlassSegmentedTabs` and `GlassSegment` in Navigation.swift: a 30 well with 26 segments, the floating variant on the map, ink rules (selected light, hover primary, otherwise tertiary or secondary), badges for decisions owed only, and dots that need words. Settings > General > Appearance is Light / Dark / System, applied immediately. Platform rules follow HIG segmented controls and M3 button groups (connected groups replace segmented buttons).
