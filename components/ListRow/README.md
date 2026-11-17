# ListRow

One row in a list or tree: a leading tile, a title with an optional sub-line, and trailing parts (a row pill, an accessory, a row menu or a chevron), selected with the accent fill.

## When to use

- A tree of folders and traces (Traces), tools and folders, or projects and agent runs.
- A flat single-select list in a sidebar or the main pane of a split view (Mail-style: the selection persists while its detail shows).
- A navigation list on touch, where each row opens a page (chevron).
- Use `DataTable` when people compare values across columns; use `Menu` for commands.

## Anatomy

1. **Disclosure** (tree rows): a 16 column (`size-glyph`) holding a 10 chevron in `text-tertiary`; it turns 90 degrees when expanded. Rows that cannot expand keep the empty column so titles line up.
2. **Tile**: 22 square (`size-tool-tile`), `radius-tile` 6, `neutral-tint` ground with a 12 glyph in `text-secondary`: a tool's mark, a folder, a trace, an agent. Decorative.
3. **Text**: title (body-strong for a parent row, body for a leaf) in `text-primary`; sub-line in caption, `text-tertiary`. Both one line, truncated at the end. A flagged sub-line uses `caution-text` (needs a look) or `positive-text` (done), always as words.
4. **Row pill**: the row's one action ("Submit 3" on a folder, "Submit" on a trace; NDS-31): `size-submit-pill` 24 tall, `radius-pill`, `control` fill, micro type, padding `space-10`. Done turns its label `positive-text`. A pill is removed, not disabled, when the product does not offer it.
5. **Accessory**: a control before the row menu (a folder's mode picker) or a trailing time (`text-tertiary`, tabular).
6. **Row menu**: 22 square, `radius-tile`, a kebab in `text-secondary`, named on its own ("More for near-agents").
7. **Chevron** (navigation rows): 10, `text-tertiary`.
Row: gap `space-8`, padding `space-4` by `space-8` leading and `space-6` trailing, `radius-control` 11, minimum height `--nr-h-row`. Indent: `tree-indent` 18 per level after the 8 inset; a tree without a tool level starts its folders flush.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Min height | 40 (`size-list-row`) | 40 | 44 (`size-control-touch`) | 48 (`target-touch-android`); M3 rows are 56 and 72 for one and two lines | 20 (`size-control-dense`) |
| Title / sub | `mac-body-strong` / `mac-caption` | `web-body-strong` / `web-caption` | `ios-body-strong` / `ios-caption` | `android-body-strong` / `android-caption` | `web-caption`, no sub-line |
| Tile | 22 | 22 | 22 | 22 (M3 leading icon 24 allowed) | 16, `radius-dense` |
| Indent per level | 18 | 18 | 18 | 18 | 15 (`dense-indent`), at most 6 levels |
| Radius | `radius-control` | `radius-control` | `radius-control` | `radius-control` | `radius-dense` |

## Variants

- **Folder row** (parent): disclosure, folder tile, mode word and waiting count in the sub-line, a Submit pill only when offered, row menu.
- **Gateway row** (leaf): trace tile, time as the title, size and state as the sub-line, a Submit pill that sends the trace at once (the row dims with a spinner while it sends), and the row menu, which holds Dismiss. Return and a click on the row still open the review (NDS-31).
- **Off row**: only the tile fades (`opacity-row-off` 0.6); the title steps to `text-secondary` and the sub-line stays `text-tertiary`, so every word keeps 4.5:1.
- **Option row** in a flat list (`role="listbox"`), **navigation row** with a chevron (`role="list"` of links), **multi-select row** with a leading `Checkbox`.
- A row may carry a `Switch` in a fixed 40 column (`size-toggle-width`) when every row has one; never mix rows with and without it in one list. A row whose setting is not yet known keeps the empty column and shows its switch once the answer arrives, never an off switch in the meantime (NDS-41).

## States

| State | Treatment |
|---|---|
| Default | no fill |
| Hover | `row-hover` replaces the fill; never over a selected row |
| Selected | `selection` fill; title, sub-line, disclosure, tile glyph and menu glyph in `text-on-accent`. The sub-line stays solid, never faded, so it keeps 4.5:1. The row pill and the open menu take `control-on-selection` with `text-on-accent` (NDS-38) |
| Expanded | disclosure turned 90 degrees on `spring-spatial-fast` |
| Pressed (pill, menu) | `brightness(0.92)` |
| Focus | the list is one tab stop; the ring (2px `focus-ring`, 2px outside) goes around the list and the selected row is the active one |
| Disabled | `opacity-disabled`, no hover |
| Off | see Variants |
| Loading | the product's line in place of rows ("Reading local queue…"); a reload keeps the rows already shown |
| Empty | the product's sentence, with a glyph in Traces |

Gateway dark's selection fill is a flagged source value (1.09:1 against the worst ground; contrast report). Selection there is also carried by the white title and by the row being the active descendant.

## Behavior

- Keyboard: Tab enters the list once. Up and Down move the selection (selection follows focus). Right expands, or moves to the first child; Left collapses, or moves to the parent. Home and End jump. Return opens the review. Type-ahead matches titles.
- Pointer: a click selects; a click on the disclosure only expands or collapses (the arrow expands, the label selects). Clicking the selected row may clear the selection when the screen has a summary to return to. Right-click opens the row menu.
- The row pill and row menu are reached by pointer, by the row's context menu, and by the selected row's own tab stop (only the selected row's pill is in the tab order).
- Touch: a tap selects or opens; long press opens the row menu; swipe actions always have a menu alternative.
- Expansion state persists per tree. Option-click (Alt-click) expands all descendants.
- Motion: fills on `duration-fast` `ease-standard`; the disclosure turns on `spring-spatial-fast`; children appear in place. Nothing moves under Reduce Motion.

## Accessibility

- Tree: `role="tree"` with `aria-activedescendant`; rows are `treeitem` with `aria-level`, `aria-expanded` (parents only) and `aria-selected`. Flat lists use `listbox` and `option`; navigation lists are links.
- Name = title; description or value = sub-line. Parent rows also read as headings by level on Apple platforms.
- The tile, disclosure glyph and chevron are hidden. The disclosure state is spoken by the platform ("expanded", "collapsed").
- The row menu needs its own name; a row menu with no name is not drawn.
- Targets: the 22 menu and 24 pill grow invisible hit areas to `--nr-target`.
- The consumer supplies every word: titles, sub-lines, flag words, pill labels, menu names.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| Custom `GlassListRow` in a custom single-focus tree (Gateway); or `List` with `OutlineGroup` and a custom row; AppKit `NSOutlineView` for very long trees | `List` with `DisclosureGroup` or `OutlineGroup`, system row height 44, swipe actions plus a context menu | `ListItem` (Expressive list) in a `LazyColumn`; expand with the list's expand tokens; selection via `Modifier.selectable` | `role="tree"` rows with `aria-level`, or `listbox`/`option`; `.nr-list-row-group` + `.nr-list-row` |

## Do and don't

- Do keep columns in the same place on every row. Don't move the pill when a row lacks a switch.
- Do remove a pill the product does not offer. Don't show it disabled without a reason.
- Do fade only the tile on an off row. Don't fade the words.
- Do make the list one tab stop. Don't put every row in the tab order.

## Source

`GlassListRow`, `GlassToolTile` and the tree conventions in ListRow.swift and Indicators.swift; the Traces tree in TracesViews.swift and TracesTree.swift [trace-commons §5.3, §5.16 item 14]. Keyboard model from HIG outline views and M3 lists; dense indent from Unity Foundations (foldout, tree view).
