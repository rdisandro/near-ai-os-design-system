# Expander

A disclosure row (a chevron that turns, a label, an optional count) that shows or hides the content under it, for reasoning, tool calls, inspector sections and foldouts.

## When to use

- Secondary detail most people skip: Show reasoning, Tool calls (3), Sources (12), Not offered.
- Inspector sections that people collapse (Decisions, Model, Limits) and dense foldouts in a `PropertyInspector`.
- Do not hide what people use often, warnings, or the only way to an action. For whole views use `Tabs` or `SegmentedControl`.

## Anatomy

1. **Header**: the whole row is the control. Padding 6 above and 2 on the other sides (`space-6`, `space-2`), radius `radius-tile` for the hover fill.
2. **Chevron**: 12 (`space-12`) in `text-tertiary`, pointing to the trailing side when closed and down when open (a 90 degree turn). Dense: 9 (`dense-indent` - `space-6`).
3. **Label**: label step for inline expanders, body-strong for inspector sections, `text-primary`; `space-8` after the chevron (dense `space-4`).
4. **Meta** (optional): a count or duration at the trailing edge, caption step, `text-tertiary`, tabular.
5. **Content**: starts under the label (chevron column + gap + 2: 22 regular, 15 dense), `space-4` below the header, in `text-secondary` unless the content sets its own colors.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Header height | about 28 | about 28 | 44 minimum | 48 minimum | 20 (`size-control-dense`) |
| Chevron | 12 | 12 | 12 | 12 (M3 expand icon 20 allowed) | 9 |
| Label type | `mac-label` / `mac-body-strong` | `web-label` / `web-body-strong` | `ios-body` | `android-body` | `web-caption` or `web-label` |
| Content indent | 22 | 22 | 22 | 22 | 15 per level, at most 6 levels |

## Variants

- **Inline**: in a message or card (Show reasoning, Tool calls). Closed by default.
- **Section**: the header of an inspector section on a quiet card; open or closed by the product, remembered per section.
- **Foldout**: dense, no container, arrow in the panel gutter (Unity). Nested foldouts indent one level each.
- **Static section**: the same header without a chevron when a section cannot collapse.
- An exclusive group (accordion) is allowed only when the sections are alternatives; by default several may be open.

## States

| State | Treatment |
|---|---|
| Closed | chevron points to the trailing side |
| Open | chevron turned 90 degrees on `spring-spatial-fast`; content shown with a fade on `duration-reveal` |
| Hover | `row-hover` behind the header (foldouts tint only on hover) |
| Pressed | `brightness(0.92)` on the header |
| Focus | 2px `focus-ring`, 2px outside the header |
| Empty | an expander with nothing inside is not drawn |
| Disabled | not used: hide an expander that has nothing to show |

## Behavior

- Click, Return or Space toggles. In a tree row the arrow expands and the label selects (`ListRow`); in an expander the whole header toggles.
- Option-click (Alt-click) on a foldout toggles its nested foldouts too.
- Expansion state persists per section and per window.
- A streaming agent answer keeps Tool calls closed while it runs and updates the count in the meta; it never opens itself.
- Native platforms animate the content's height on `spring-spatial`; web shows the content in place with a short fade. Under Reduce Motion the chevron turns and the content appears with no motion.

## Accessibility

- Web: `<details>` and `<summary>`, so the expanded state and keyboard come from the browser. Custom builds use a button with `aria-expanded` and `aria-controls`.
- Apple platforms represent it as a native `DisclosureGroup`, so the system speaks "expanded" and "collapsed" in the person's language.
- The chevron is decorative. The label names the content ("Tool calls"), and the count is part of the name when shown.
- The consumer supplies the label, meta and content.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| `GlassExpander` (a "›" that turns, a semibold label, accessibility represented as `DisclosureGroup`), or `DisclosureGroup` with a custom style | `DisclosureGroup`, header at least 44 tall | A `ListItem` header with a trailing expand icon and `AnimatedVisibility` content; `Modifier.semantics { stateDescription }` from the platform strings | `<details class="nr-expander">` with `.nr-expander__summary` and `.nr-expander__content` |

## Do and don't

- Do name what is inside ("Sources", "Tool calls (3)"). Don't write "More" or "Details", except as the label of a notice's own detail expander, where "Details" is the fixed word for "everything this decision does not need" (NDS-25).
- Do keep reasoning and tool calls closed by default. Don't open them on their own.
- Do use foldouts for groups of five or more properties. Don't hide a single high-traffic control.
- Don't nest more than six levels, and don't put a foldout inside a container in a dense panel.

## Source

`GlassExpander` in Controls.swift (the "›" turning 90 degrees on `fast`, semibold label, 6/2/2/2 padding, native disclosure for assistive tech) and the inspector section pattern (quiet card + expander) in TracesInspectorHost.swift [trace-commons §4.2, §5.4]. Foldout rules from Unity Foundations; triangle direction and the AI uses from HIG disclosure controls.
