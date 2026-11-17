# Dense and pro-tool patterns

Dense is the fourth density tier (NDS-10). It is for panels people work in for hours with many values in view: an agent's configuration, a model's parameters, the spans of a trace, an evaluation table, a run's log. The benchmark is the Unity Editor (Editor Foundations) and Unity App UI, the most fully documented dense desktop system available: 20px rows, 2px between fields, an 18 / 4 / 8 inspector inset and a 15px indent. This section maps those patterns onto the Near AI tokens and onto Apple and Material where they differ.

Apply `.nr-dense` to a panel's container. Components inside read the density properties: `--nr-h-control` and `--nr-h-row` become `size-control-dense` 20, `--nr-gap` becomes `space-2`, `--nr-target` becomes 20. Colors never change with density.

## When to use dense

Use it:
- In panels where the rows outnumber the window height at compact density, and people compare or tune many values (temperature, max output tokens, tool permissions, retry policy).
- In pointer-and-keyboard windows: macOS, the Windows and Linux shells, desktop web at expanded width and up.
- Inside one pane or panel at a time. The window's navigation, `Tabs`, `Toolbar` and `ActionBar` stay compact.

Never use it:
- On touch-first devices: phones, tablets without a pointer, visionOS. Touch floors never shrink. On the web, `@media (pointer: coarse)` removes `.nr-dense`.
- For first run, consent, settings, sign-in, or anything a person sees once.
- As the only option. Dense rows sit below WCAG 2.5.8's 24px target minimum, so dense is opt-in per panel or per person (View > Density: Compact, Dense) and compact is always one switch away.

| Measure | Compact (macOS default) | Dense | Tokens |
|---|---|---|---|
| Control height | 28 | 20 | `size-control-large`, `size-control-dense` |
| Row height | 40 | 20 | `size-list-row`, `size-control-dense` |
| Between fields | 8 | 2 | `space-8`, `space-2` |
| Between groups | 10 to 20 | 8 | `card-gap`, `space-8` |
| Inspector inset | 16 sides, 18 top and bottom | 18 leading, 4 trailing, 8 top and bottom | `inspector-padding-x`, `inspector-padding-y`; `dense-padding-left`, `space-4`, `space-8` |
| Indent per level | 18 after an 8 inset | 15, six levels at most | `tree-indent`, `dense-indent` |
| Control radius | 11, capsules for buttons | 3 | `radius-control`, `radius-pill`; `radius-dense` |
| Labels and values | `mac-label` 12, `mac-body` 13 | 12 | `mac-label` on macOS; the same 12 step (`web-caption`) in the shells |
| Captions, status bar | `mac-caption` 11 | 11 on macOS, 12 in the shells | `mac-caption`; `web-caption` in the shells |
| Glyph | 16 | 16 | `size-glyph` |
| Pointer target | 28 | 20 visible; the hit area spans the row and its gap | `target-pointer`, `size-control-dense` |
| Tooltip width | 260 | 300 | `size-popover-width` |

A dense panel stays usable at 275 wide with no horizontal scrolling. Below that it collapses to a tab in its pane.

[Unity Foundations: content organization, layout] [Unity App UI: scale context]

## Inspector and property panels

`PropertyInspector` is the dense inspector. It lists the properties of the selection as label and value rows.

1. **Object header.** A tool tile or glyph, the object's name in `mac-body-strong`, its type as a caption in `text-tertiary`, on a `card-quiet` band. Property rows sit directly on the pane, so the band marks the higher level.
2. **Section headers.** Each group is an `Expander` foldout. Header labels are bold; nothing else in the panel is, except overridden values.
3. **Property rows.** 20 high, `space-2` apart. The label column takes 33 to 40 percent of the width, at least 96, left-aligned, with no colon. The value column flexes. Every label has a `Tooltip`.
4. **Help box.** A message sits directly under the property it is about and pushes the rows below it down (see message tiers).
5. **Overridden values.** The label turns bold and gains a small `accent-soft` dot after it. The tooltip names the source ("Set on this run; the agent default is 0.2"), and the row's context menu offers Revert.

- Group in this order of preference: vertical space, a header, a foldout, then a `SegmentedControl` for up to four views at 275 wide. Use a container only when the group shares an interaction (a reorderable list with add and remove).
- Never put high-traffic properties inside a foldout, and never put a foldout inside a container.
- When a field has focus, its label turns `accent-text`, so the eye finds the active row in a long list.
- A value that can never be edited here is plain text in a `KeyValueList`, never a disabled field.

**Example.** An agent named Release notes writer: Model (`Select`), Temperature 0.7 (`NumberField` with a `Slider`), Max output tokens 4,096, Tools (web.search, repo.read in a reorderable list), Tool approval (Ask, Automatic, Never), Retries 2. A trace's span: Started 09:14, Duration 52 min, Tool Claude Code, Redactions 3, Proof verified.

[Unity Foundations: inspector, inheritance] [trace-commons: TracesInspectorHost.swift]

## Foldouts

- An `Expander` row: the chevron sits in the gutter, offset into the leading padding; then an optional glyph, then the label. Each nesting level indents `dense-indent` 15, six levels at most.
- In an inspector, the chevron and the label both toggle. In a tree, the chevron expands and the label selects.
- Option-click (Alt-click) a chevron to expand or collapse every level below it.
- The chevron turns 90 degrees on `duration-fast`; under Reduce Motion it jumps.
- Idle headers have no fill; under the pointer they take `row-hover`.
- Remember open and closed state per object type, per window.

## Numeric fields

`NumberField` in a dense panel:

- **Anatomy.** A scrubbable label; a 20 field on `field` with `radius-dense`; the unit after the value in `text-tertiary`; tabular figures (`nr-tabular`). Add a `Slider` when the range is bounded at both ends: the field sits at the trailing end and the slider flexes, with the same track length for every slider in the panel.
- **Scrubbing.** Dragging the label left or right changes the value; the pointer becomes the left-right resize shape. Shift multiplies the step by 10; Option or Alt divides it by 10.
- **Keys.** Up and Down nudge by one step, with the same Shift and Option multipliers. Return commits; Esc reverts; Tab commits and moves on.
- **Units.** The field shows its unit, accepts it typed, and converts compatible units on commit ("2 h" in a minutes field becomes 120 min).
- **Expressions.** Arithmetic is evaluated on commit: `1024*4` becomes 4,096. An expression that cannot be evaluated reverts and says why.
- **Bounds.** Clamp on commit and say so under the row ("The maximum for this model is 8,192.").
- **Vectors.** Multi-value fields put a short sub-label (X, Y, Z) before each box.
- Always show a value. Empty means mixed; a dash means unknown.

[Unity Foundations: numeric field, slider] [Unity App UI: numerical field]

## Mixed values

When several objects are selected, a field whose values differ shows that they differ. Unknown and mixed look different: unknown is a dash or the product's unknown word and is read-only (NDS-16); mixed means the service answered and the answers disagree.

| Control | Mixed display | On edit |
|---|---|---|
| `TextField`, `NumberField` | An empty field with the product's mixed word ("Mixed") as its placeholder | The typed value applies to every selected object |
| `Checkbox` | The mixed dash glyph, announced as mixed | The first click checks all |
| `Switch` | Not used; dense panels and multiple selections use a `Checkbox` | |
| `Select`, `SegmentedControl` | The mixed word, no segment selected | The choice applies to all |
| `Slider` | No thumb until the person drags; the field shows the mixed word | The dragged value applies to all |

- One edit to a mixed field is one undo entry for all objects. Esc leaves them mixed.
- A parent checkbox follows its children: checking it checks all, unchecking clears all, mixed children make it mixed.

[Unity Foundations: toggle] [Unity App UI: checkbox]

## Live and committed values

Every field reports two values: a live one while it is being edited and a committed one on Return, blur, slider release or picker close.

- Preview live values at once: the canvas, the chart, the token estimate.
- Create an undo entry only on commit, one per commit, named for the property ("Undo Temperature"). Typing, scrubbing and dragging compress into that one entry.
- Use a delayed field, which commits only on Return or blur, when applying is slow, costly or destructive (rerunning an evaluation, re-indexing a folder). Elsewhere, update live.
- Invalid input reverts to the last valid value on commit. While the field has focus it shows a 1px `critical` ring, and the reason appears under the row in `critical-text`.
- The Edit menu names the next undo. Undo and Redo buttons disable at the ends of the history.
- Changes an agent makes are undo entries too, batched per run ("Undo changes from run 14").

[Unity App UI: undo stack] [HIG: undo and redo]

## Docking panes and window types

A pro-tool window (an agent workbench: runs, transcript or canvas, inspector, console) docks several panels into the window.

- Each dock region is a `Pane` with the flat-glass geometry, `pane-gap` 10 apart. Dense changes what is inside a pane, never the pane itself.
- The gap is the splitter. It shows the resize pointer; double-click resets the default size; dragging below a panel's 275 minimum collapses it to a tab.
- Several panels can share a pane as `Tabs` in the pane header. Each pane has a More menu: Move to New Window, Close, Reset Layout.
- Layouts persist per window across restarts. Window > Reset Layout restores the default.

| Type | Component | Docks | Moves | Resizes | Closes on outside click | Blocks the window |
|---|---|---|---|---|---|---|
| Docked panel | `Pane` in the window | Yes | By its tab | Splitter | No | No |
| Floating panel | Panel torn off into its own window | Back into a pane | Yes | Yes | No | No |
| Dropdown | `Menu`, `Select`, `Popover` | No | No | No | Yes | No |
| Utility panel | Find and replace, a detached model picker | No | Yes | Fixed | No | No; stays on top |
| Modal | `Modal` | No | No | No | No | Yes |
| Alert | `Modal` confirmation | No | No | No | No | Yes |

[Unity Foundations: windowing, overlays] [Unity App UI: split view]

## Toolbars that show only usable tools

- A panel's toolbar sits under its tabs and holds actions about that panel, never the person's whole task.
- Tool groups are contextual. A group appears when the selection or mode makes it usable and leaves when that changes (span tools appear when a span is selected). Global view options stay.
- Inside a group that is showing, a tool that cannot run right now is disabled with its reason in the tooltip; it is never hidden.
- Put high-traffic tools at the leading end and low-traffic ones at the trailing end. Group by kind (tools, toggles, view options) with `space-8` between groups, three groups at most.
- Dense tools are 20 square `IconButton`s with `radius-dense` and `toolbar-glyph`. A pressed toggle (Show redactions) takes `accent-tint` behind an `accent-text` glyph.
- As the panel narrows, the lowest-priority tools move into a More menu.
- Every tool is a registry command; its tooltip shows the label and the shortcut.

[Unity Foundations: toolbar, contextual tooling]

## Trees

A dense tree is a `ListRow` tree at 20 rows.

- Indent `dense-indent` 15 per level, six levels at most, with the chevron in the gutter. Labels are `mac-label`; only top-level containers are bold. Counts and durations sit at the trailing end in `text-secondary`, tabular.
- The tree is one tab stop. Up and Down move; Right expands, then moves to the first child; Left collapses, then moves to the parent; Home and End jump; typing jumps to a matching label; Return acts (in Gateway, it opens the review).
- Shift-click selects a range; ⌘-click (Ctrl-click) toggles a row. Rename through the context menu or by double-clicking a selected label.
- The selected row takes `selection` with `text-on-accent`; hover takes `row-hover`, never over a selected row. Keyboard focus draws the ring around the tree.
- Expose tree semantics: tree and tree item roles, level, expanded state, position in set.
- Drag vertically to reorder and sideways to change the parent. The 2px `accent` insertion line starts with a small circle at the target depth.
- Virtualize long trees. A fixed row height makes it cheap.

Examples: Gateway's folder and trace tree; an agent run with its steps and tool calls.

[Unity Foundations: tree view, foldout] [trace-commons: TracesTree.swift]

## Tables

A dense `DataTable` at 20 rows:

- **Header.** Sticky (`z-sticky`) on the pane's hard scroll edge, so rows never show through. Labels in `mac-label`, `text-secondary`.
- **Rows.** A `hairline` between rows, never around the table. Hover takes `row-hover`; selection takes `selection`.
- **Sorting.** Clicking a sortable header sorts ascending, then descending; the arrow glyph follows the label. Shift-click adds a second key. Expose the order with `aria-sort` or the platform equivalent, and keep it per window.
- **Columns.** Resize by dragging the header edge; double-click fits the content. Reorder by dragging the header. Show or hide optional columns from the header's context menu.
- **Alignment.** Numbers align to the trailing edge in tabular figures; text to the leading edge. Figures that describe what leaves the device are monospaced.
- **Empty cells.** A cell without a value shows a dash, never zero.
- **Keyboard.** The grid is one tab stop. Arrow keys move the active row or cell; Return edits an editable cell; Esc reverts.
- Use columns, never tabs, when people compare values across items.

Example: the Private AI calls table, with Time (mono), Model, Tokens in, Tokens out and Proof (a `ProofTag`: verified, pending, no proof).

[Unity Foundations: multi-column views] [trace-commons: InferenceViews.swift]

## Message tiers, status bar and console

Choose the tier by scope, then the tone by severity. Every message follows Problem, Cause, Solution, without an "Error:" prefix.

| Tier | Scope | Component | Behavior | Example |
|---|---|---|---|---|
| Dialog | The whole app; blocks | `Modal` confirmation | One to three buttons, each a verb; rare | "Near.ai cannot start the watcher because the folder near-agents is no longer readable. Choose the folder again in Settings." |
| Banner | The window | `Toast`, or a window `Notice` | A toast fades after a time scaled to its length; a toast with an action stays until used or replaced; a notice stays until resolved | "Exported 214 calls to calls.csv." |
| Help box | A section or property | `InlineAlert`, or a small `Notice` under the control | Stays until resolved; 200 characters at most; one button that fixes it in place and one link to the docs | "Max output tokens is above this model's limit of 8,192. Lower it or choose another model." |
| Console | Operations over time | Status bar and console pane | Time-stamped entries; the status bar shows the latest; clicking it opens the console | "09:14:07 web.search returned 0 results." |

- Severity is a glyph plus words, never color alone. Critical means the operation will not complete; caution means it completes and may surprise; neutral is information.
- Empty states never use warning glyphs. An `EmptyState` explains the condition; a help box explains a failed recovery.

**Status bar.** A 20 strip at the bottom of a panel or window, in `mac-caption` (`web-caption` in the shells) and `text-secondary`. It holds brief status only (counts, last saved, the latest console line), because it can fall off-screen. Nothing critical lives there.

**Console pane.** Rows of 20 in `mac-mono` (`web-mono` in the shells) with columns for time, severity, source and message. Filter by severity with a `SegmentedControl`; search; Copy; Clear. Follow new lines only while the person is at the bottom; once they scroll up, never pull them back. Announce errors politely; never announce every line.

[Unity Foundations: errors and messaging, help box, empty states]

## Keyboard-first operation

- Every command is reachable from the keyboard, and its shortcut shows in menus, the palette and tooltips, all read from the registry.
- Tab moves through fields in reading order. Control-F6 (macOS) or F6 (Windows, Linux) moves between panels.
- Return commits a field, Esc reverts it, Space toggles a checkbox, arrow keys move in trees, tables and segmented controls.
- Esc steps out one level at a time: revert the field, leave the field, close the transient surface.
- ⌘[ and ⌘] (Ctrl+[ and Ctrl+] elsewhere) walk the selection history, up to 50 entries, with no duplicates and no animation.
- Type-ahead works in every list and tree. ⌘F filters the focused panel; Mod+K opens the palette.
- Single-key tool shortcuts work only while the canvas has focus, and people can remap them.
- The focus ring is the standard 2px `focus-ring`, 2px outside (NDS-5). In a dense panel it overlaps the 2px gap; draw it above the neighboring rows.

[Unity Foundations: accessibility, selection history]

## Tooltips

- Show after 0.4 s of hover or on keyboard focus. Moving straight to a neighbor that has a tooltip shows it at once. Hide at once when a drag starts or the pointer leaves for something without one. Stay while hovered.
- At most 300 wide, three lines, 200 characters, placed `space-10` below the element and centered, flipping at window edges.
- Write complete sentences. When the label is truncated, the first line repeats it in full; the description follows. The shortcut comes from the registry.
- Every inspector label and every icon-only control has one. An icon-only control's tooltip equals its accessible name.
- Draw tooltips on the floating layer with `z-tooltip`. Never put essential information only in a tooltip.

[Unity Foundations: tooltip]

## Hide or disable

- **Hide** an action in a row or a card that cannot run, and a control whose state is not yet known (NDS-41). A Reconnect with no tool to reconnect, Stop on a session the app does not control and a switch waiting for the service's answer are absent, not dimmed. Gateway's Submit pill on a folder with nothing to submit is absent too.
- **Hide** a control that applies only in rare cases or whose value means nothing in the current state. A dependent control appears directly below the control that reveals it, ideally on the next line.
- **Disable** toolbar toggles, menu-bar items and form fields whose value matters but cannot change now (it is set automatically, or the service has not answered). Disable the whole control at `opacity-disabled` 0.45, with no hover, and give the reason in its tooltip or beside it. A toolbar toggle that does not apply to the current view (Gateway's Graph outside Traces) is disabled, not hidden, so the toolbar never reflows.
- Never hide a button to show state; state is a dot plus words beside it.
- Context menus and row menus hide what cannot run. The menu bar disables it. Tabs are never disabled.

[Unity Foundations: interactions]

## Reference measures from the Unity Editor kit

The Unity Editor UI Toolkit Figma library measures the Editor's own chrome. Use these figures when a dense panel must sit beside pro tools people already know.

| Element | Editor kit | Parent dense equivalent |
|---|---|---|
| Value field | 18 high | 20 (`size-control-dense`); the 2px difference is the larger macOS label |
| Buttons | 18 / 20 / 24 (mini, regular, large) | 20 dense, 28 compact |
| Toolbar, tab strip, dock tab | 20 high; a search field shrinks to 16 inside | A dense `Toolbar` row is 28; inside a dense panel's own toolbar use 20 with a 16 `SearchField` |
| Tree and list rows | 16 | 20 (`ListRow` dense); 16 only for read-only logs |
| Property-row pitch | 20 (18 + 2) | 22 (20 + `space-2`) |
| Label column | About 120, or 33% for horizontal labels | 33 to 40 percent, at least 96 |
| Indent | 15 per level | `dense-indent` 15 |
| Object header, section header | 60, about 22 | Object header band 44; `Expander` header 22 |
| Type | Six sizes: 9, 10, 11, 12, 14, 19 (Inter; 12 is the default, drawn at 11.5 to match the Editor) | `mac-micro` 10, `mac-caption` 11, `mac-label` 12, `mac-body` 13, `mac-title` 15, `mac-heading` 17 |

- **Depth by brightness, not shadows.** In the Editor's dark theme, value wells sit darker than the window (#2a2a2a on #383838) and buttons lighter (#585858). The parent does the same with `field` and `well` below the pane and `control` above it; dense panels never add shadows.
- **Hover is an overlay.** The Editor tints a hovered row with 6% white (dark) or black (light) so hover reads on zebra rows too; `row-hover` (5% white, 4% black) is the parent equivalent.
- **Focus has three cues.** A field border, a button ring and the focused field's label recolored. The parent keeps `focus-ring` and recolors the label to `accent-text`.
- **Selection follows window focus.** The Editor selects in blue (#2c5d87) only while its window is focused and in grey (#4d4d4d) otherwise, as Apple's unemphasized selection does. The parent keeps `selection` and dims the whole pane with `inactive-dim` in a background window; a separate unfocused-selection role is a candidate for a later version.
- **States.** Dense controls need the full set: default, hover, focused, focus and hover, pressed, pressed and focused, checked, selected, selected in an unfocused window, accepted (a valid drop target), invalid, mixed, disabled, loading.
- **Segmented groups** are built from leading, middle and trailing pieces that share borders and round only the outer corners. `SegmentedControl` in a dense panel follows this construction with `radius-dense`.
- **Toolbar separators** are 1px hairlines drawn inside the toolbar, never separate elements.
- **Window templates are variants, not layouts.** One "default window" covers most tools as background (plain, recessed, zebra) × tabs on or off × toolbar on or off × one to three panes. Build dense tool windows from the same switches.
- **Console counters.** A status bar shows counts by severity with a glyph each (info, warning, error); log rows are two lines with a severity glyph. Use this for agent run logs and trace spans, with `positive`, `caution` and `critical` marks and words.
- **Dialogs stay native.** Unity uses the operating system's menus, window frames and dialogs unchanged. Do the same; the parent restyles only what the app draws.

[Unity Editor UI Toolkit library; Unity App UI v3.2 library; partial read, internal paddings not captured]

## Mapping onto Apple and Material

### The benchmark's conflicts, resolved

| # | Topic | Resolution |
|---|---|---|
| 1 | Depth | The content layer is flat with no shadows; hierarchy comes from fills (`card-quiet` bands) and hairlines. `shadow-float` belongs to panes and the floating layer only (NDS-2, NDS-9). |
| 2 | Corners | Pane geometry never changes; inside a dense panel, radius marks what is interactive: `radius-dense` 3 on controls, none on rows and groups. |
| 3 | Toggle naming | Name them `Checkbox` and `Switch`; dense panels use `Checkbox`, and `Switch` stays for settings that take effect at once outside dense panels. |
| 4 | Capitalization | Copy is written in sentence case (NDS-16); shells may set macOS and iPadOS menu-bar items in title case with the ellipsis, and nothing else. |
| 5 | Tooltip timing | 0.4 s in dense panels with instant hand-off and no auto-hide while hovered; the platform default elsewhere. |
| 6 | Toast stacking | One `Toast` per window at a time; a newer one replaces it, and a replaced Undo stays in Edit > Undo. |
| 7 | Tabs scope | `Tabs` navigate; `SegmentedControl` switches views inside a panel (four at most at 275 wide); neither is ever disabled. |
| 8 | Radio or dropdown | Two to five options inline (`RadioGroup` or `SegmentedControl`), six to fifteen in a `Select`, more than fifteen in a searchable `Select`. |
| 9 | Disabled styling | `opacity-disabled` 0.45 on the whole control on every platform, with the reason in words. |
| 10 | Target size | Dense controls are 20 tall with a hit area across the row and its gap; that is below WCAG 2.5.8's 24, so dense is opt-in, pointer-only and one switch from compact. |
| 11 | Dialog button order | Cancel leads and the primary trails (NDS-19); a destructive action takes the trailing place and is never the default (NDS-15); Esc cancels. |
| 12 | Links | Links leave the app or open documentation, in `accent-text` with an external glyph; moves inside the app use buttons, rows and breadcrumbs; underline on hover in dense chrome, at rest in running text on the web. |
| 13 | Status fill contrast | The NDS-6 floors hold with no overrides; status words use the `*-text` tokens and counts on `badge-fill` use `text-on-status`. |
| 14 | Type sizes | On macOS, 12 for labels and values (`mac-label`), 11 for captions and the status bar (`mac-caption`), 10 only for tags and chart ticks (`mac-micro`); the shells use the nearest `web-*` step; nothing smaller. |
| 15 | Icons | Vector glyphs from the icon registry at `size-glyph` 16 in dense and compact controls and 20 on touch toolbars, tinted by token, never bitmaps (see Iconography). |
| 16 | Text over glass | Dense rows sit on painted content inside a pane whose `glass-veil` holds 4.5:1 over the worst-case ground (NDS-6); dense text never sits straight on a blur. |

### Where the platforms differ

| Platform | Dense rendering |
|---|---|
| macOS | Native controls at the small control size inside dense panels; outline views at the small row size for trees; native menus. Sidebar row size follows the system setting, never the panel's density. |
| Windows, Linux shells | `.nr-dense` on panel containers; container queries enforce the 275 minimum; the forced-colors path still applies. |
| Desktop web | Same as the shells; `@media (pointer: coarse)` falls back to touch density. |
| iPadOS | No dense tier. With a pointer and keyboard attached, pro panels use compact. |
| Android | No dense tier; M3's 48dp target holds. Desktop windowing with a mouse uses regular density. |
| visionOS | Never dense; targets stay at `target-spatial` 60. |

See Layout, density and targets for the density properties, and Forms and data for field and table behavior at the other densities.
