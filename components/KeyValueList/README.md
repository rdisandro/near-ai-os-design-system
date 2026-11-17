# KeyValueList

Read-only label and value pairs with the labels end-aligned in a narrow column, for the facts about one thing: a folder's path, a model's provider, a trace's size.

## When to use

- Facts in an inspector or a card: Path, Traces, Mode, User; Model, Provider, Attestation.
- A detail page's summary on touch (stacked form).
- Use `PropertyInspector` when the values can be edited, `DataTable` when several records are compared, and `StatCard` for one headline figure.

## Anatomy

1. **List**: a `<dl>` laid out as a two-column grid, inset `space-6` on each side.
2. **Label column**: 70 wide (`space-64` + `space-6`), labels end-aligned against the value, `text-tertiary`, wrapping inside the column when long.
3. **Gap**: `space-10` between label and value; `space-6` between pairs.
4. **Value**: `text-primary`, selectable, wrapping anywhere for long paths and hashes. Paths, hashes, sizes and figures that describe what leaves the device use the mono step.
5. Both columns share one type step (the label step on desktop and web), so baselines line up.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Layout | label column 70 | label column 70 | stacked | stacked | label column 70, or 40% in a `PropertyInspector` |
| Type | `mac-label` | `web-label` | label `ios-caption`, value `ios-body` | label `android-caption`, value `android-body` | `web-caption` |
| Mono values | `mac-mono` | `web-mono` | `ios-mono` | `android-mono` | `mac-mono` |
| Pair gap | 6 | 6 | 10 | 10 | 2 |

## Variants

- **Columns** (default): Gateway's inspector facts.
- **Leading** (Gateway's current form, #1387): labels start-aligned with no fixed column, the value after a `space-10` gap, so short labels don't leave a gutter. The parent keeps the 70 column as its default; a product may choose this form for every list it draws.
- **Stacked** (`.nr-key-value-list--stacked`): the label over its value, start-aligned, `space-10` between pairs. For phones and for any column narrower than about 220.
- **Copyable value**: a value people will paste elsewhere (an attestation hash, a request ID) may add a copy `IconButton` after it; the value stays selectable either way.

## States

| State | Treatment |
|---|---|
| Default | label `text-tertiary`, value `text-primary` |
| Unknown | "—" or the product's unknown word, never 0 and never blank |
| Loading | the product's line in place of the list; held values stay until new ones arrive |
| Stale | the value stays and the caption above the list says when it was read ("Last checked 2 min ago") |
| Increased contrast | no change: the list draws no surface of its own |

## Behavior

- Static: no tab stops of its own; text selection works on values.
- A value that links somewhere is a link inside the value (accent text), never the whole row.
- Long values wrap; nothing truncates silently. A path may wrap at its separators.
- Nothing moves.

## Accessibility

- Use `<dl>`, `<dt>` and `<dd>`; each label and value pair reads as one item. On Apple platforms each pair is one combined element.
- Labels are nouns without colons. Values carry their units ("212 KB").
- `text-tertiary` labels hold 4.5:1 on panes, cards and quiet cards over the worst ground.
- The consumer supplies every label and value.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| `GlassKeyValueList` (a `Grid` with a 70pt trailing-aligned label column and `.textSelection(.enabled)`), or `LabeledContent` in a `Form` | `LabeledContent` rows in a `List` section (label leading, value trailing) or the stacked form in a card | `ListItem(headlineContent = value, overlineContent = label)` for stacked; a `Row` with a fixed label width for columns; `SelectionContainer` | `<dl class="nr-key-value-list">` with `.nr-key-value-list__row` wrappers |

## Do and don't

- Do keep labels short (one or two words). Don't end them with a colon.
- Do use the mono step for paths and hashes. Don't use it for words.
- Do show "—" for an unknown value. Don't drop the pair.
- Don't use a key-value list for values people edit.

## Source

`GlassKeyValueList` in Containers.swift (70pt end-aligned label column, 10 by 6 grid spacing, 6 inset, selectable values, optional mono) [trace-commons §4.5]; the stacked form follows HIG lists on iOS and M3 list overlines.
