# SearchField

A capsule field with a search glyph, a clear button and optional scope tokens, for finding and filtering content as people type.

Intentional addition. trace-commons has no search component; its search screens reuse `GlassTextField` with a Command-F focus binding. Every platform has its own search idiom (HIG search fields, M3 search, Unity search field), and Near AI products search traces, models and agents, so the parent defines one.

## When to use

- Use it to filter a list or search a collection.
- Use `CommandPalette` to run commands and `PromptComposer` to ask an agent.

## Anatomy

1. **Glyph**: a magnifier at `size-glyph` (16), `text-tertiary`, leading.
2. **Input**: the label step at regular weight (the body step on touch). The prompt names what is searched ("Search traces").
3. **Tokens** (optional): input `Chip`s that scope the search ("in: nearcore", "@near/nearcore"), before the text.
4. **Clear**: a filled-circle glyph at 16, `text-tertiary`, `text-primary` on hover. It shows only while there is text, and its hit area grows to `--nr-target`.
5. **Well**: `field` fill, `radius-pill`, height `--nr-h-control`, `space-10` leading and `space-4` trailing padding.
6. **Results line** (outside, optional): caption `text-tertiary` in a polite live region ("12 traces match").

## Sizes by density

| | Compact (macOS) | Regular (web) | Touch iOS | Touch Android | Dense |
|---|---|---|---|---|---|
| Height | 28 | 28 | 44 (system bar) | 56 (M3 search bar) | 20 |
| Text | `mac-label` | `web-label` | `ios-body` | `android-body` | `web-caption` |
| Minimum width | 150 (about 20 characters) | 150 | full width | full width | 150 |

## Variants

- **Field** (default) in a pane, toolbar or panel.
- **With scope tokens**, for prompt-scoped search.
- **Condensed**: an icon button that expands into the field and focuses it. It collapses on an outside click only while empty (Unity).

| Placement | Where |
|---|---|
| macOS and iPadOS | Trailing end of the toolbar; top of the sidebar when it filters the sidebar. It resizes with the window. |
| iPhone | Bottom toolbar, within reach. It rises above the keyboard on focus and may minimize to a button. Top only when a sheet holds the bottom. |
| Android and web | Top of the screen or pane (M3 search bar), or inline above the list it filters. |
| Dense panels | Inline at the top of the panel. |

## States

| State | Look |
|---|---|
| Empty | Prompt in `text-placeholder`; no clear button |
| Focus | 2px `focus-ring` round the capsule |
| Filled | Clear button shown |
| Searching | The results line says so in the product's words |
| No results | The results line says so and offers a way out ("Clear the filter.") |
| Disabled | `opacity-disabled` |
| Increased contrast | 1px `edge-hc` inset edge |

## Behavior

- Search as people type when results are local and fast. Debounce remote searches. Show recent searches before typing and suggestions while typing. An AI search that cannot run per keystroke runs on Return and shows its suggestions at once.
- Mod+F focuses the field. Esc clears the text; a second Esc leaves the field.
- Return or a comma turns typed scope text into a token. Backspace at the start selects the last token, and a second Backspace removes it.
- Default to the broadest scope. Narrow it with a `SegmentedControl` or filter `Chip`s under the field.
- Keep the query when people open a result and come back.

## Accessibility

- Wrap the field in `role="search"`. The input is `type="search"` with the consumer's name, which matches the prompt.
- The clear button and each token's remove button carry the consumer's names ("Clear search", "Remove in: nearcore").
- Announce the result count politely after typing pauses.
- Contrast as `TextField`. The glyph is decorative.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| `.searchable` or `NSSearchToolbarItem` in the toolbar (system glass); this painted field inside panes | `.searchable` at the bottom with `.searchToolbarBehavior(.minimize)`; tokens with `searchable(text:tokens:)` | `SearchBar` or `DockedSearchBar` at the top, container `field`; `InputChip`s for scope | `.nr-search-field` (type class here) holding the glyph, `<input type="search">` and the clear button |

## Do and don't

- Do name what is searched in the prompt.
- Do keep the clear button visible whenever there is text.
- Don't open an empty results page on focus; show recents instead.
- Don't use search to run commands.

## Source

Intentional addition. Grounded in Gateway's review sheet search (field auto-focused and on Cmd-F, recents, a three-state result label) built from `GlassTextField(focus:)` in Controls.swift; HIG search fields and Liquid Glass search placement (bottom on iPhone, trailing toolbar on iPad and Mac); M3 search; Unity search field (live results, 150 minimum width, condensed variant).
