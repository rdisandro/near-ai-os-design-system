# Tablet patterns

Tablets take the desktop's structure at touch density. An iPad, an Android tablet, an unfolded foldable or the inner display of iPhone Duo gets a sidebar or rail, two or three panes, an inspector, a menu bar or command list, and pointer and keyboard support, with every target at the touch floor. Never ship a phone layout stretched to a tablet.

As on phones, the screen is an opaque pane (`pane-base`, `pane-opaque` under Reduce Transparency; see Glass and materials). Glass is for chrome only: the tab bar, sidebar, rail, toolbars, inspector column, menus and popovers (NDS-9). Density is the touch tier (NDS-10): targets of `target-touch-apple` 44 on iPadOS and `target-touch-android` 48 on Android, even when a trackpad is attached, with `ios-*` and `android-*` type.

## Classes on tablets

Lay out from the window's width in the Near AI classes (NDS-12). Apple's size classes only choose idiom components. Regular width gets the sidebar-adaptable tab bar, an inspector column and popovers; compact width gets a tab bar and sheets.

| Window | Width (pt or dp) | Class | Layout |
|---|---|---|---|
| iPad Split View or a narrow window | about 320 to 507 | Compact | Phone patterns |
| iPad mini portrait, iPad 11" portrait | 744 to 834 | Medium | One pane plus sidebar overlay, or 50/50 for light content |
| iPad 13" portrait, iPad 11" landscape | about 1032 to 1194 | Expanded | Two panes |
| iPad 13" landscape, Stage Manager on a display | 1366 and up | Large | Two panes and an inspector |
| Android tablet portrait, foldable inner display portrait | 600 to 839 | Medium | One pane, collapsed rail |
| Android tablet landscape, foldable landscape | 840 to 1199 | Expanded | Two panes |
| iPhone Duo outer display / inner display | compact / regular | Compact / medium or expanded | Phone patterns / tablet patterns |

Treat any window that is wider than it is tall but under 480 high as compact height: one pane and short bars.

[M3: breakpoints] [HIG: layout]

## iPad

### Sidebar-adaptable tab bar

Use `TabView` with the `.sidebarAdaptable` style. The `TabBar` floats in glass near the top of the window and converts to a `Sidebar` (`size-sidebar` 280) with a button people control. Apple asks for the tab bar first; the sidebar is for products with collections people move between.

- Keep five tabs or fewer by default so the compact and regular layouts match, and let people customize the set.
- Label every tab with one word and a filled SF Symbol. Never disable or hide a tab; an empty destination shows an `EmptyState`.
- In sidebar form, add sections below the tabs: pinned threads and projects in a Near AI chat app; watched folders under Traces. Show at most two levels; deeper hierarchy goes in a content column.
- Never hide the sidebar by default, and never put critical items at its bottom.
- Tabs switch places. Actions go in the toolbar, never in the tab bar.

**Gateway worked example.** Home / Private AI / Traces / Insights become the tabs, Traces carrying the decisions-owed `Badge` (or a dash when the count is unknown). Home's sub-pages keep their `Breadcrumb` inside the content column.

### Split view and inspector

Use `NavigationSplitView` with two or three columns and `.inspector` for the trailing column. The columns follow the canonical layouts in Web patterns.

| Gateway pane (Mac) | iPad at regular width | iPad at compact width |
|---|---|---|
| Main pane (440: tabs, notices, tree) | Content column, about 440 | The root of the navigation stack |
| Content pane (map) | Detail column, flexible | A pushed page from a toolbar button |
| Inspector (293) | `.inspector`, `size-pane-inspector` 293 | Detail page for a trace; `Sheet` for Summary |

- Put the sidebar toggle at the leading end of the toolbar and the inspector toggle at the trailing end, beside search.
- Let a horizontal shelf or hero image extend under the sidebar (the background extension effect); keep its text and buttons outside the extended part.
- Inspector demand carries over from Desktop patterns: events that need the inspector open it, nothing closes it on its own, and people close it with its toggle.
- The split view reflows continuously while a window resizes. Columns collapse in order: inspector to a sheet, then the content column into the navigation stack.

### Windows that resize

iPadOS runs apps full screen or in freely resizable windows, several at once, and an app cannot tell which (iPadOS 26). Design every screen for any width from 320 up.

- Use layout margins, safe areas and size classes; never a fixed width or a device check.
- The system places window controls at the leading edge of the toolbar. Inset leading toolbar items so they never sit under the controls.
- Support several windows. Offer "Open in New Window" on a thread, an agent run and a review, from the context menu and the File menu. Each window keeps its own selection, scroll position, unsent draft, column widths and inspector state, and restores them on relaunch.
- Inactive windows dim their content. Painted panes add `inactive-dim` in the same state.

### Menu bar

iPadOS 26 adds a menu bar. Render the command registry into it (NDS-14), in the standard order: app menu, File, Edit, Format, View, product menus, Window, Help. Navigation and commands holds the registry and the shortcut table.

- Every toolbar item is also a menu command. Shortcuts are written `Mod+Key` and shown with ⌘.
- Show menu-item icons only for key actions, as iPadOS 27 does.
- Esc and ⌘. stop a running generation. ⌘F finds in the current pane, ⌘N starts a new thread or run, ⌘, opens Settings.
- Settings is a destination in the sidebar, or its own window when the app supports several (NDS-21). Never present it as a sheet over the main window.

### Pointer

A trackpad or mouse adds to touch on iPad; it never replaces it.

| Element | Pointer effect | Example |
|---|---|---|
| Small control on a transparent background | Highlight | Toolbar `IconButton`s, `SegmentedControl` segments, tab items |
| Small control with an opaque fill | Lift | App tiles, tool tiles |
| Large element | Hover: tint with `card-hover` or `row-hover`, no scale | Interactive `Card`, `ListRow`, `StatCard` |
| Text | I-beam | `TextField`, `TextArea`, `PromptComposer` |

- Extend hit regions about 12 pt around controls with a visible shape and about 24 pt around borderless ones. Make neighboring toolbar buttons' regions touch so the pointer never flickers back between them.
- Pointer movement reveals controls that minimized during reading. Hover is an enhancement; nothing is reachable only by hover. A `Tooltip` shows on pointer hover and its words also serve as the accessible name.
- Support band selection in lists that allow several selections (traces in a folder), and secondary click for the context menu. The context menu carries the same actions as the row's swipe actions.

### Keyboard

- Use focus groups: Tab moves between the sidebar, the list, the detail, the inspector and the composer; arrow keys move inside a group; each group has a primary item that takes focus first. A list shows the focused row as a full-row highlight; fields show the focus ring.
- Keep the ring on (NDS-5). If a product turns it off, keyboard users on iPad lose their only sign of where focus is, and the product fails WCAG 2.4.7.
- With a hardware keyboard, Return sends from the `PromptComposer` and Shift+Return adds a line, as AI and agent patterns sets out. Confirmations follow the ladder (NDS-15): Gateway's Submit has no shortcut and never answers Return.
- Name each shortcut exactly as its menu item is named, so the menu bar teaches the keyboard.

### Apple Pencil

- Every control responds to a Pencil tap. Scribble works in every text field, including `SearchField` and the `PromptComposer`.
- While someone writes with Scribble, suppress suggestions and completions in the field, keep the field still, hide the placeholder at the first stroke, and never scroll it.
- Where an agent returns a document, image or chart, offer markup with PencilKit. Ink appears on contact with no mode switch. Keep Dark Mode color adaptation off over PDFs and photos. In a compact window, put Undo and Redo in the toolbar.
- Pencil hover previews and never acts. Double tap follows the person's system setting. Squeeze (Pencil Pro) runs one discrete, non-destructive action near the tip, such as opening the markup tools; it never sends, contributes or deletes.
- Keep tool palettes movable and clear of either hand.

[HIG: designing for iPadOS] [HIG: pointing devices] [HIG: Apple Pencil and Scribble] [Liquid Glass: sidebars, inspectors and split views]

## Android tablets and foldables

### Navigation rail

| Class | Navigation |
|---|---|
| Medium, one pane | Collapsed `NavigationRail`, `size-rail-collapsed` 96 |
| Medium, two panes | The bottom `TabBar` (navigation bar), so both panes keep their width |
| Expanded and up | Collapsed rail, or the expanded rail (`size-rail-expanded` 220 to 360) as a standard rail that pushes content |
| Any class, opened from the menu button | The expanded rail as a modal over `scrim`, `radius-card` 16 on its trailing corners |

- Keep the rail on the leading edge (the right edge in right-to-left languages), vertical, destinations only.
- Put the screen's one constructive action at the top of the rail: a FAB in the collapsed rail, an extended FAB in the expanded rail ("New chat"). Never show a second FAB in the content.
- Badges sit on the icon in the collapsed rail and beside the label in the expanded rail. Labels stay readable at 200% font scale.
- Never show the rail and the bottom bar together.

### Panes

Use `ListDetailPaneScaffold` and `SupportingPaneScaffold` with window size classes, opting in to the large and extra-large classes (`supportLargeAndXLargeWidth = true`).

- Two panes from expanded up, separated by a 24 dp spacer. A fixed pane is 360 dp at expanded and 412 dp at large and up.
- The rail narrows only the leading pane, so the spacer stays centered in the window.
- Offer a drag handle between the panes with snap points at 360, 412 and the visual center. In list-detail, remember the width people set; a supporting pane returns to its default each time.
- Medium shows one pane, or two at 50/50 only when both are light (a short list beside a short detail).
- Gateway's Traces tab maps to list-detail: folders and traces in the list pane, the trace review card in the detail pane. Private AI maps to a supporting pane: the ledger primary, the account section supporting.

### Predictive back

Android Back is the system's, with a preview of where it goes. Implement it natively for every surface that participates.

- In a single-pane list-detail, Back from the detail previews the list. In two panes, Back leaves the destination.
- Back closes, in order: the open menu, the bottom sheet or modal side sheet, the modal rail, focused search, then the screen.
- Never block Back with a confirmation, except when unsent work would be lost and cannot be saved as a draft.

[M3: navigation rail] [M3: canonical layouts]

## Foldables and iPhone Duo

The same rules cover Android foldables and iPhone Duo. The layout follows the class of the display in use, and the hinge is a reserved region.

**Postures.**

| Posture | Hinge | Layout |
|---|---|---|
| Closed (outer display) | none | Compact: phone patterns |
| Flat | none | Medium or expanded: two panes |
| Half-open as a book | Vertical | Two equal panes, one on each side of the fold |
| Half-open on a table (tabletop) | Horizontal | Content above the fold; controls, the `PromptComposer` and playback below |

- On Android read the hinge from Jetpack WindowManager's `FoldingFeature` (bounds, `FLAT` or `HALF_OPENED`, orientation, whether it separates). On iPhone Duo use `ReservedRegion`.
- Never put text, a control or a target across a separating hinge. Split panes at the fold.
- Never build a layout per pose. The compact and regular classes cover every pose; let the layout expand rather than rearrange.
- Avoid large layout changes while the device folds. Prefer small shifts; keep the selected item and the scroll position.
- Use an even number of grid columns, so a fold never splits a column.

**iPhone Duo reserved regions.** The outer front camera is always present and expands into the Dynamic Island. The inner front camera is present only while the camera is on, and the interface moves aside to reveal it. The folding region exists only when the device is partly open; it splits the inner display and its center is excluded. Alerts, context menus and sheets move off the fold on their own; custom views must do the same.

**Split views on Duo.** A split view collapses to one pane on the outer display and expands on the inner one, as it does between compact and regular on other iPhones. Fully open, the list pane is narrower than the detail. Partly folded, the two panes are equal, one on each side. Keep the same functions and state on both displays; the inner display may add one more level of hierarchy. Keep navigation containers outside arrangement views.

**Vertical controls on Duo.** On the outer display and on the inner display in landscape, toolbars and tab bars move to the trailing hardware edge in one column: Dynamic Island, status bar, toolbar, tab bar. This edge is fixed to the hardware and is not mirrored in right-to-left languages, unlike the Android rail, which is leading and mirrored.

- Order the column from the top: Back or Close, then the prominent action (Send, Done), then the remaining groups.
- Overflow runs from the bottom up. Give groups and items a visibility priority; the running-agent indicator, Stop and unread badges keep the highest priority.
- Give every icon item a title and a symbol, since titles appear in overflow. Avoid text-only buttons, which force a horizontal bar.
- Never override the system's bar placement. Use the system overflow menu and merge custom overflow into it.

**Chat on a foldable.** Closed, the device shows the list or the thread; open, it shows both side by side. Keep the `PromptComposer` clear of the fold (below it in tabletop, inside one pane in book posture), and keep Stop, Send and the model picker in the same place across postures.

[HIG: designing for iPhone Duo] [M3: canonical layouts]

## Inspector as side sheet or sheet

The inspector is supplementary. It shows facts and decisions about the selection and never holds primary navigation.

| Platform | Compact | Medium | Expanded | Extra-large |
|---|---|---|---|---|
| iPadOS | `Sheet` at the medium detent, growing to large | `.inspector` column when the width is regular; otherwise a sheet | `.inspector` column, `size-pane-inspector` 293 | Same |
| Android | Modal bottom sheet | Modal side sheet over `scrim` (at most 400 dp) | Standard side sheet beside content | The third pane |

- A standard side sheet is part of the screen: `pane-base`, separated by a `rule`. A modal side sheet floats over `scrim` with `radius-sheet` on its inner corners and `shadow-modal`.
- Keep the person's inspector width per window.
- Choose a detail page over a sheet when the inspector holds a decision. Gateway's trace review card carries Submit and Look inside, so at compact it becomes the detail page; the Summary inspector, which only reports, becomes a sheet.
- Show one sheet at a time. On iPad prefer the form or page sheet style, centered over a dimmed window.

## Drag and drop

Support drag and drop wherever content moves, and give every drag a menu equivalent.

| Drag | Result | Modifier |
|---|---|---|
| Within one list or pane | Move | Option (iPad) or Ctrl (Android with a keyboard) forces a copy |
| Between panes or windows of the app | Copy | |
| Between apps | Always copy | |

- Show the drag image after about 3 pt of movement. Highlight only targets that accept the item, with an insertion point in lists; elsewhere show nothing or the not-allowed symbol. A rejected drop animates back to its source.
- Hovering a dragged item over a sidebar item or tab opens it after a pause (spring loading).
- The `PromptComposer` is a drop target. Accepted files become `Chip`s with upload progress; a rejected file gets an `InlineAlert` with the reason ("This file type can't be attached."). Attach and paste do the same job.
- Dragging a `Message` out offers rich text, then Markdown, then plain text. A `CodeBlock` drags out as its text.
- Gateway's first run accepts a folder dropped on the dashed add tile; the tile's edge turns `accent-soft` while a folder is over it. The Files app is the source on iPad.
- Make drops undoable. Confirm only a drop that cannot be undone.

[HIG: drag and drop]

## Multitasking

- Expect any window size at any time: Split View, Slide Over, Stage Manager, Android split screen and free-form windows. A narrow window gets phone patterns; a window on an external display may reach extra-large and show the three-pane layout.
- An Android tablet with a keyboard and mouse may run in desktop windowing. Keep touch targets at 48 dp and add hover states for the pointer.
- Save and restore context per window: selection, scroll position, unsent draft, pane widths, inspector visibility.
- Agent runs keep going on the server when the app moves to the background. Notify only when a run the person started finishes, fails or needs an answer, and stream the result in quietly when the window is in front. See Phone patterns for notifications and Live Activities.
- Keep audio and voice input polite: pause dictation when the app loses focus, and resume only on request.

[HIG: multitasking]
