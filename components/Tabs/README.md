# Tabs

Tabs switch between the top-level views of one pane, drawn as the Ember Rule: equal-width titles over a hairline rule, with a glowing ember under the selected title.

## When to use

- Two to five peer views that share one pane and each keep their own state, such as Home, Private AI, Traces and Insights in Gateway's main pane.
- Use `SegmentedControl` for a mode or a filter inside a card or over a map (Traces · Private AI).
- Use `Sidebar`, `NavigationRail` or `TabBar` for app-level destinations, and `StepProgress` for a sequence the person reaches in order.
- Keep to five tabs. HIG tab views stop at six and M3 fixed tabs crowd past four. Never disable or hide a tab; show the view's empty state inside it.

## Anatomy

1. **Container** `.nr-tabs`: the full width of its pane. `--bleed` runs the rule to the pane's edges from inside `pane-padding` and clips the ember there.
2. **Tab list** `.nr-tabs__list` (`role="tablist"`): equal-width columns.
3. **Tab** `.nr-tabs__tab`: the title, then one mark, `inline-gap` 6 after it, 8 side padding. The mark is a count pill (14 tall) when there is a count, otherwise a status dot (6, `space-6`); never both (NDS-37).
4. **Rule**: 1px of `rule` along the bottom edge.
5. **Ember** `.nr-tabs__ember`: a 2px line of `tab-ember` that fades to transparent at both ends and spans 160% of the tab (30% past each side), centered on the rule; and a halo of `tab-ember-halo`, an ellipse 110% of the tab wide rising 26 (`size-control`) from the rule, gone before the tab's edges. Both percentages are derived from the source's `emberReach` 0.3.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Height | 34 (`--nr-h-bar`, the 30 track + 4) | 34 | 48 (`--nr-target`) | 48 | 28 |
| Title | `mac-body` | `web-body` | `ios-label` | `android-label` | `mac-label` |
| Weight | medium, semibold selected | same | same | same | same |
| Badge | `mac-micro`, 14 tall | `web-micro` | `ios-micro` | `android-micro` | none |
| Halo | 26 | 26 | 26 | 26 | 26 |

## Variants

- **Default**: the rule spans the tabs and the ember is clipped 4 past the rule's ends.
- **Bleed** (`--bleed`): inside a pane, the rule meets the pane's edges (the main pane).
- **Count pill** (`.nr-tabs__badge`): the count in the tab's status tint, the tone's `-tint` ground with its `-text` ink (`--positive`, `--caution`, `--critical`); with no tone, `neutral-tint` with `text-primary`. For counts the person may act on later (decisions owed). A zero draws no pill. A count the product does not know draws a dash, never 0.
- **Alert badge** (`--alert`): `badge-fill` with `text-on-status`, for items that block the person (an agent run waiting for approval).
- **Status dot** (`.nr-tabs__dot--positive | --caution | --critical`, `neutral` by default): beside the title when there is no count, always with words for assistive tech (Private AI: answering).
- **Movable** (`--movable` on `.nr-tabs`): the person can reorder the tabs. A held press lifts a tab (`.nr-tabs__tab--lifted`): scale 1.06, 2 up, on `control` with `radius-control` and `shadow-float`; then it drags. The first tab (Home) is fixed.

## States

| State | Treatment |
|---|---|
| Default | `text-secondary`, medium |
| Hover | `text-primary`; no fill |
| Pressed | no fill on any tab (NDS-37). A click selects at once; the ink change and the ember carry the feedback |
| Lifted (movable tabs) | after a 0.35 s held press: scale 1.06, 2 up, `control` fill, `radius-control`, `shadow-float` |
| Selected | `text-primary`, semibold, the ember. The weight and ink change carry selection; the ember is never the only cue |
| Focus | 2px `focus-ring`, 2px outside, keyboard focus only. A product that turns rings off with `.nr-focus-off` fails WCAG 2.4.7 |
| Disabled | not allowed |
| Unknown badge | a dash |

## Behavior

- **Keyboard**: one tab stop with a roving `tabindex`. Left and Right move and select (automatic activation, because the views are local and switch at once); Home and End go to the first and last tab. On macOS, Cmd-1 to Cmd-4 select Home, Private AI, Traces and Insights in their default order, and the menu bar lists them.
- **Pointer and touch**: a click or tap selects. Swiping the content does not switch tabs.
- **Reordering** (movable): a quick drag moves nothing. A press held 0.35 s within 6 of where it started lifts the tab; dragging past a neighbor's middle trades their places. A held tab released in place opens; a tab that moved never opens. The order is stored per person and kept across launches. Offer the same reorder without a drag, as Move left and Move right accessibility actions and View menu commands.
- **Motion**: the ember glides on `spring-ember` over `duration-spring-ember` (native: response 0.35, damping 0.85). Ink changes use `duration-fast` with `ease-standard`. The lift runs on `spring-spatial-fast` (native: response 0.25, damping 0.8). Under Reduce Motion the ember moves and the tab lifts at once.
- **Wiring**: set `--nr-tabs-count` and `--nr-tabs-index` on `.nr-tabs`; the ember translates by the index.

## Accessibility

- `role="tablist"` with an `aria-label` from the product; each tab is `role="tab"` with `aria-selected` and `aria-controls` pointing at its `role="tabpanel"`.
- The dot and the badge are `aria-hidden`. Their words go in the tab's name as visually hidden text ("3 decisions owed", "Private AI answering"), from the product's copy. In SwiftUI the segment's `accessibilityValue` carries them.
- Titles in `text-secondary` and `text-primary` hold 4.5:1 over the worst-case ground. `tab-ember` holds 3:1 on `pane-opaque` but stays decorative.
- Targets: 34 tall and at least a fifth of the pane wide on desktop; 48 on touch.
- **The product supplies**: the tab list's label, each title, badge counts (or unknown), dot status and the words for both.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| Custom `GlassRuleTabs` (matched-geometry ember) | In-screen views: a segmented `Picker` (native, HIG). The Ember Rule only in an iPad main pane that mirrors the desktop window | `PrimaryTabRow` with a custom indicator that draws the ember (M3 default indicator is 3dp) | Custom: this CSS with `role="tablist"` |

## Do and don't

- Do keep titles to one or two words, nouns, sentence case.
- Do place the tabs at the top of the pane they switch, under its toolbar.
- Don't nest tabs in tabs. Use `SegmentedControl` or `Breadcrumb` for the second level.
- Don't use tabs for steps or for actions.
- Don't scroll the tab row. Past five views, use a `Sidebar`.
- Don't color titles with the accent, and don't draw the ember anywhere but under the selected tab.
- Don't draw a press wash on a tab, and don't put a dot beside a count.

## Source

`GlassRuleTabs` and `GlassSegment` in `macos/Sources/TCDesign/Components/Navigation.swift` (the Ember Rule, owner choice 2026-10-10: `emberReach` 0.3, `emberLine` 2, `haloHeight` 26, `toPaneEdge` bleed, ink primary when selected or hovered; owner 2026-11-02: no press fill on `GlassRuleTabs` or `GlassSegmentedTabs`, `liftDelay` 0.35, `liftSlop` 6, `liftScale` 1.06, `liftRise` 2, a black 18% shadow of radius 8 at y 3 drawn here as `shadow-float`, `dragThreshold` 6, reordering from 2026-10-30, Home fixed); the tab mark as one count pill in the status tint, a dot only without a count (#1460, 2026-10-15); used in the main pane in `Views/MonitorWindowView.swift`. Touch heights and the keyboard model from M3 tabs; the tab ceiling from HIG tab views.
