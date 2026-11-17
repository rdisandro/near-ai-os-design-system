# Desktop patterns

The macOS app is the lead desktop client. It is built in SwiftUI and AppKit, and the Gateway monitor (its bundle still ships as "Near.ai", NDS-48) is its reference. Windows and Linux run the same product as the web app inside a Tauri shell, drawn with our web components on the parent tokens (NDS-18). This section generalizes the trace-commons window and its surfaces into patterns any Near AI desktop app can use, and says how each one renders on Windows and Linux. Navigation, the menu bar and shortcuts are in Navigation and commands; browser specifics are in Web patterns.

## Windows a desktop app owns

| Window | Role | Default size | Minimum | Chrome |
|---|---|---|---|---|
| Main window | Primary: navigation and content | 1193 × 614 with three panes (440 + 10 + 440 + 10 + 293); opens sized to the panes it shows (890 with the inspector hidden) | Height 560; width is the sum of the visible panes | Hidden title bar; window controls inside the main pane |
| Settings | Auxiliary, one instance | 780 × 640 | 540 × 420 | Standard title bar; `pane-opaque` |
| First run | Auxiliary, one instance | 860 × 760; the stage scales down to fit a smaller host | None | Hidden title bar; one full-window stage on the scene (NDS-32) |
| Review | Auxiliary, or a `Modal` in the main window | 760 × 620 | None | Pane-tier sheet, Close only |
| Menu-bar panel | Glance and quick controls from the `StatusItem` | 285 wide (NDS-33) | None | One glass layer pinned under the menu bar |
| Edge rail | Opt-in working surface at the screen edge (macOS) | 4 × 240 closed, 484 × 680 open | None | Borderless, does not take focus, on every Space |
| `Modal` | Confirmations and scoped tasks inside a window | `size-modal-width` 780 or `size-modal-narrow` 450 | Inset `modal-inset` 28, `modal-inset-top` 52 | `scrim-modal` over a `blur-scrim` of the window |

[trace-commons: TraceCommonsAppMain.swift, ThreePane.swift]

## The floating three-pane window

The main window is three floating panes with nothing drawn between them. Each is a `Pane` on the navigation layer: glass, `radius-pane` 20, one `shadow-float`. Everything inside a pane is painted content (NDS-9).

1. **Main pane**, `size-pane-main` 440 by default, always shown. It holds the top row, the `Tabs` and the tab's content; notices float over its top (see *Notices and the gate triad*).
2. **Content pane**, flexible, at least `size-pane-content-min` 360. It holds the map, a canvas, a transcript or a document. Overlays on it (segmented tabs, a zoom toolbar, a node card) sit on the floating layer, never as a second glass pane.
3. **Inspector**, `size-pane-inspector` 293, two thirds of the main pane. It holds detail for the selection.

Panes sit `pane-gap` 10 apart. On macOS the window background is clear, so the panes meet the window edge; in the web shell the same gap separates them from the window edge.

- Turning the content pane or the inspector on grows the window to the right by the pane plus its gap; turning it off shrinks it from the right. The left edge stays put (NDS-35).
- When the screen edge is in the way, the window slides left by exactly as much as it must: the new pane is fully on screen, the window's right edge sits on the screen edge, and the main pane keeps its width. The slide is animated with the pane. Closing a pane never snaps the window back to the edge.
- The window stays on its current display and is kept on screen at launch, as AppKit does. There is no custom placement for relaunch, thin strips or several displays.
- A divider between the main and content panes moves width between them; both widths are remembered. With the content pane hidden, the main pane takes the width. The inspector keeps 293.
- While the person drags the window edge, panes follow the frame directly; pane widths never animate frame by frame. Only showing and hiding a pane animates.
- On first launch, show the content pane when the screen is at least `bp-map` 1100 wide and the inspector when it is at least `bp-inspector` 900 wide.
- Persist per window: pane visibility, pane widths, the selected tab, the selection, sub-pages, the graph footer, filters. Restore them on relaunch.
- The empty parts of the window move it. Content that drags (a folder in a tree, a pressed row) holds the window still. In the web shell, mark the top row's empty space as a drag region.

On macOS the window is the sum of its panes, so its class follows from what is shown. In the Windows and Linux shells people resize freely, so the panes reflow by layout class (NDS-12):

| Window width | Panes shown | Inspector | Content pane |
|---|---|---|---|
| 1200 and up | Main, content, inspector | Trailing pane | Flexible |
| 840 to 1199 | Main plus one | Trailing pane; opening it hides the content pane, and the reverse | Trailing pane |
| Under 840 | Main only | A trailing side `Sheet` over the main pane | A full-window view with a back chevron in the top row |

[trace-commons: GlassThreePane, `GlassPaneLayout.windowFrame(onScreen:)` in ThreePane.swift (#1775), HoldsWindowStill.swift] [M3: panes]

## Inspector demand

Events open the inspector; nothing closes it but the person.

- Open it when something happens whose result people need to see: an action that can be undone, an item submitted or kept, a folder submitted, a review requested, an agent run finishing.
- Open it when people select an item that has detail (a trace, a history row, a folder with its own cards). Clicking a folder's node on the map selects that folder.
- Show the inspector only on tabs that have detail. Elsewhere its toolbar toggle is disabled with a tooltip that says why (a toolbar toggle disables; NDS-41).
- With nothing selected, the inspector shows a summary: counts, the legend pair, the decisions waiting, the safeguards.
- Build it from an inspector header (an optional large tool tile, the heading in one bold line, a caption in `text-tertiary`) and inspector sections (a quiet `Card` holding an `Expander`, collapsible or fixed). Pad it `inspector-padding-x` 16 by `inspector-padding-y` 18, with `card-gap` 10 between sections. Sections never nest a second card.
- Keep decisions next to the list. The trace review, with Submit and Look inside, lives in the inspector; Dismiss lives in the row's menu. Sheets are for read-only deep looks.
- Offers, undo and health banners sit above the list they act on: on Traces above the tree, on the other tabs at the top of the inspector.
- A menu opened from a control inside a card (the Decisions card's Submit split button) is never clipped by the card. Draw it at the nearest ancestor that does not clip (the inspector column), trailing-aligned with its trigger and `space-4` below it, never past the column's leading edge. When the trigger is at the end of a scroll view, add room under the card while the menu is open and scroll just far enough to show it, on `duration-fast`.
- In pro tools the inspector becomes a `PropertyInspector` at dense density. See Dense and pro-tool patterns.

[trace-commons: MonitorShell.swift, SessionReviewCard.swift, InspectorPrompts.swift; the Decisions card menu, #1902]

## The main pane top row

- **Leading.** Clear space for the window controls. macOS reserves 78 × 30 and centers the row on the traffic lights. On Windows and Linux the caption buttons sit at the trailing edge, so the clearance moves there and an app menu button takes the leading end.
- **Trailing.** One `Toolbar` group: a control-tier capsule with `space-2` padding holding `IconButton` toggles (Graph, Map, Inspector). A toggle whose pane is hidden draws its glyph in `toolbar-glyph-off`; a toggle whose menu is open takes `toolbar-expanded` (Gateway fills it with the accent). A toggle that does not apply to the current tab is disabled, not hidden (Graph outside Traces). After the group, a round 28 `IconButton` opens Settings.
- Options that belong to one list live in that list's own menu, not in the toolbar: Gateway's "Show ignored folders" is in the Traces filter menu.
- Every toolbar item is also a View menu command in the menu bar with the same label and state, and its tooltip equals its accessible name.
- On macOS, Settings lives in the App menu on ⌘,. Gateway's gear in the top row is a second path for people who never open the menu bar. On Windows and Linux the gear is the main path.

## Notices and the gate triad

Notices float; the gate sits in the tab.

- **Popover notices.** A desktop notice is the popover variant of `Notice` (NDS-25): an opaque plate on the floating layer over the top of its tab, just under the tab bar, that pushes nothing down. A tone coin leads, then the title, a summary that says only what the decision needs, a "Details" expander for the rest and the actions; an X dismisses it. A consequence the person must see before acting stays in the summary, never behind Details.
- **The stack.** Several notices stack with the newest in front and at most two earlier plates peeking `space-8` behind it, three drawn in all. A new notice slides in while the stack holds still. A notice anchored to a map's foot stacks upward. A batch of the same event collapses into one plate with a count.
- **Actions.** Every notice's call to action is a primary `Button`; Not now, Decline and Dismiss are links. A pure dismiss is the X. A health banner has no action. A notice the service holds open (a gate held for a project) has no X.
- **Gate triad.** Every surface backed by a service (the local watcher, the account, a server) shows one of three gates before content. *Awaiting*: a standalone `Spinner` with a line of words replaces the content. *Down*: a health banner, with held data kept visible. *Signed out*: one place offers sign-in. A whole surface that needs an account shows a notice with Sign in; a section that waits on the account says so once, beside its heading ("No data – Sign in", with Sign in as a link), and its cards carry no sign-in sentences. A card that needs the account puts a small primary Sign in where its Refresh pill sits when signed in. The main window, Settings and the menu-bar panel use the same triad.
- **Fail closed.** A value the service has not answered is absent or a dash, never "On" and never zero (NDS-16).
- **Held data stays.** A failed reload adds an `InlineAlert` or a notice with Refresh and keeps the last value on screen.

[trace-commons: PopoverNotice.swift (`GlassPopoverNotice`, `GlassPopoverStack`: peek 8, three drawn), MonitorNotices.swift, MonitorWindowView.swift, HomeViews.swift (owner, 2026-11-02)]

## Tabs with the ember rule

The main pane's top-level areas use the rule variant of `Tabs`: equal-width titles over a 1px `rule` that bleeds to the pane edges. The selected title gets a 2px `tab-ember` line reaching past it on both sides, with `tab-ember-halo` rising behind it. The ember glides between tabs on `spring-ember` (`duration-spring-ember` 488) and jumps under Reduce Motion.

- A tab carries one count pill in its status tint (the tone's `-tint` ground with its `-text` ink) for decisions owed, or a dot when there is no count; the meaning is also in the tab's accessibility value in words.
- No tab draws a press fill. Movable tabs lift on a held press (0.35 s) before they can be dragged; a click still opens the tab, and Home stays first (NDS-37).
- Gateway's tabs are Home, Private AI, Traces and Insights, on ⌘1 to ⌘4. A person's own order is kept.
- ⌘1 to ⌘9 select tabs. Sub-pages inside a tab use a `Breadcrumb`, and Esc goes back one level.
- The first element of every tab sits `space-16` below the tab bar; the pane owns that gap.
- Tabs are never disabled. See Navigation and commands for the depth rules.

[trace-commons: Navigation.swift (`GlassRuleTabs`, owner 2026-11-02)]

## Menu-bar glass panel

The `StatusItem` opens a panel of glances and quick controls. In Gateway it is the panel people use most.

1. **Frame.** 285 wide (NDS-33), `space-10` padding, `space-8` between rows, `radius-pane`. The panel is the only glass layer: it masks the system's own material so nothing is glass on glass, and it keeps its top edge pinned under the menu bar.
2. **Header.** The Near AI wordmark leads, 16 tall (about 85 wide), from the kit's own paths (NDS-27). Round `IconButton`s trail: Watching (`eye`; a menu of the pause durations 1 hour, Until morning, Until resumed), Settings and Quit. A long count shrinks the header's words before it truncates them.
3. **Product section.** Shown only while signed in: an eyebrow with the service's state as one word and a dot ("On" only once the service confirms it is running), then one launch button per tool that can be started (Claude Code, Codex, OpenCode). A launch button opens the main window at that tool's launch dialog.
4. **Glances.** The app's dot-matrix `BarGraph` over 11 days in its compact form: the app's dot spacing, every other weekday labelled, the legend following the pointer. While watching is paused both series draw grey and the legend keeps its colors.
5. **Menu rows.** Separated by `hairline`: Open app, then Check for Updates where the app updates itself. Settings and Quit are in the header.

- Never show "On" unless the service confirms it. A control whose state is not yet known is hidden, not dimmed (NDS-41).
- Confirm inside the panel with an inline well (Keep and Confirm). Sheets are unreliable in a menu-bar window.
- Resubscribe to the event stream 5 s after it drops, and re-read glances every 60 s while the panel is open.
- The panel takes its size only from its own controller; a change in content height applies in one step, never animated.
- Never rely on the status item being visible; a notch or a crowded bar hides it. Every panel command also lives in the main window and the Dock menu.
- Show the status item by default only for apps whose job is ambient, such as Gateway watching folders, and offer a switch in Settings to remove it.
- **Windows** opens the same panel as a flyout from the notification area, on Acrylic. **Linux** shows it from the tray where the desktop supports status items (GNOME needs an extension), so the main window must carry everything.

### The status item

The status item is brand plus data in one image (NDS-33): the N at 14 in the menu bar's own ink, `space-4`, then a 17 by 17 micro bar graph of the last 24 hours, and the badge slot. Nothing fills behind them. The image is drawn for both bar appearances and follows the menu bar, not the app. Unknown data draws no bars; paused greys the trace bars; the badge counts decisions owed at 11 tall, caps at 99+, and is hidden at zero or unknown, with an attention mark in its place. Anatomy, colors and states are in `StatusItem`.

- Draw the status item with an accessibility label and help text from the copy source; VoiceOver reads the full count, never "99+".
- On Windows and Linux the tray icon stays a single-ink template image.

[trace-commons: MenuBarGlassPanel.swift (`width` 285), MenuBarPanel.swift (`GlassMenuBarStrip`), GlassNearWordmark.swift; #1490, #1539, #1585, #1640, #1692, #1730] [HIG: the menu bar]

## Edge rail

`EdgeRail` is an opt-in working surface on the right edge of the screen (NDS-34). It is off by default and turned on in Settings > General. macOS only: on Windows and Linux the notification-area panel carries the same peeks.

- **Closed:** a 4 × 240 hover zone holding a 3 × 72 handle, centered vertically.
- **Open:** a 56-wide rail of 44 tiles inset 12 from the edge (the product's sections, a rule, then the app's tile, the blue N), and a 380-wide peek pane 16 to its left, at most 680 tall. Gateway opens on Private AI.
- Hovering the zone opens it; leaving starts a 300 ms grace (`duration-slow`) before it closes. Hovering a tile selects its peek; clicking the app's tile opens the app.
- Each peek is its tab in miniature, in the tab's own cards and words: a header with the title (and the service's state word), then the menu-bar panel's round buttons (Settings, Quit; Watching on Traces). There is no footer link and no "nothing sent" line.
- Writes run from the peek as they do in the tab: Pause and Resume, a folder's Submit split button and its "…" menu, a rule change, a tool launch. Anything that needs a review or a dialog (a trace's review, Submit as…, a rule change that confirms) opens the main window there instead.
- The rail is always drawn as focused (never `inactive-dim`) and reads data only while open.
- Rail content never animates its size. The window grows before the rail slides in and shrinks only after it has slid out; expanding a folder applies at once.
- The keyboard and assistive path: the handle has an Open action, and a Show edge rail command in the registry opens it with focus on the first tile. Esc closes it.
- It slides on `duration-slide` with `ease-standard` and fades only under Reduce Motion.

[trace-commons: EdgeRailController.swift, EdgeRailView.swift (owner, 2026-10-22); #1518, #1519, #1585]

## Settings window

Settings opens in a window of its own with ⌘, (Ctrl+, on Windows and Linux), from the App menu, the gear, or the palette. It is never a modal over the main window (NDS-21). A second ⌘, brings the open window forward.

1. **Header.** Title, subtitle, and a `Chip` with the state people most need to see (Watching or Paused). A `rule` below.
2. **Section list.** `size-modal-nav` 180 wide. Rows use `text-secondary` and `row-hover`; they scroll the body to a section and select nothing, so they never take the menu-selection fill. A name that has not loaded yet shows a disabled dash row.
3. **Body.** One scroll. Each section starts with a section rule (an accent eyebrow and a hairline) and is built from eyebrow `Card`s in a column padded `space-20` by `space-12`.

- Fill the window with `pane-opaque`. Esc and ⌘W close it. Reopen at the last section.
- Gate it with the same triad as the main window. Each setting that reads from the service has a read state: a `Spinner` while awaiting, a line and Retry when it failed, the control when answered.
- Apply changes at once; there is no Save button. A consequential change follows the confirmation ladder, and consent changes are checkbox-gated.
- Appearance is a `SegmentedControl` (Light, Dark, System) in General, applied immediately (NDS-17).
- Keep Settings for things people change rarely: account, data and consent, notifications, folders, startup. Task options stay where the task is. Never duplicate a system setting.
- A choice made during setup that sets a default (Gateway's "Automatic / Ask each time" sharing choice) sits at the top of its Settings section with the same disclosures, and an item's own setting always wins over it (NDS-30).

[trace-commons: SettingsModal.swift, SettingsStateRow.swift, SharingChoiceCard.swift] [HIG: settings]

## First-run window and the stage

First run is one animated scene, not a set of pages (NDS-32).

- **Window.** 860 × 760, the stage's own canvas; in a smaller host it scales down to fit. Hidden title bar. The whole window is the scene: `scene` with one `scene-glow-brand` glow breathing from the top-leading corner on every step. Content on it uses the scene tokens (`scene-card`, `scene-control`, `scene-rule`), because pane-tier fills vanish on the navy scene. This is the only place a macOS app paints the scene.
- **Steps.** Welcome, Tools, Uses, Traces, Private AI, Join. Sign-in is last, and nothing that needs an account is blocked before it.
- **Actors.** The N and the tool tiles are shared actors that move between steps rather than redrawing. A scan or a count that ran once does not replay on Back.
- **Skeleton.** Every step has the same frame, top to bottom: the step thread (`StepProgress`, thread variant; hidden on Welcome and at the end), the step's graphic, the title under the graphic, a card sized to its content, then the action bar. The free height is split into three equal gaps (thread to graphic, graphic to title, card to action bar), at least `space-24`, with `space-20` from the title to the card.
- **Title.** Centered, two weights: a light half and one bold phrase ("Connect your **tools**"), with no period.
- **Cards.** `scene-card`, as wide as their content; cards on one step share the widest one's width. An expanding card (Customize on Tools) grows up and out from its anchored bottom edge over the graphic, and shrinks back the same way.
- **Action bar.** Back leads on `scene-control`; on the trailing side a Customize link (where the step offers one) and the primary. Stage buttons are 13 semibold at `size-cta` 34. A note about the primary sits above the bar in `text-secondary`. Join has no Back and no Skip; its primary waits for sign-in.
- **Choices.** Nothing is pre-selected: found tools start unticked and Continue waits for one tick; past traces start unticked. A choice that needs an account (Automatic sharing, per project or for every project) can be picked before sign-in, shows the same arming confirmation, reads "Turns on once you sign in." and is armed at Start.
- **Welcome.** The N draws itself like a marker (1.0 s, from the inner lower-left, a pen-tip dot riding the stroke), the title rises word by word, and a soft shine crosses the N about 1.5 s in and then every 15 s (NDS-26). No pulse. Under Reduce Motion every step opens at its final frame.
- **Finish.** The stage folds into the N, which flies toward the menu bar where the `StatusItem` lives.
- Quitting during first run resumes at the same step. The signed-out gate reopens it.

[trace-commons: FirstRunStage.swift, FirstRunFrame.swift, WelcomeScreen.swift, ToolsScreen.swift, GlassBrandMarkDrawing.swift; #1558, spec 2026-10-22-animated-first-run-design.md]

## Review sheet

Any flow that sends data off the device offers a read-only review of exactly what would leave. Gateway calls it Look inside.

- Present it as a `Modal` at `size-modal-width` 780 or a pane-tier sheet at 760 × 620. The footer has Close only; Submit stays on the inspector card and Dismiss in the row's menu.
- The header holds an eyebrow, a title, a description, the gate statement, a quiet card of sizes in monospaced digits ("would send 41 KB · on disk 118 KB") and the send disclosure.
- A `SegmentedControl` switches Transcript, Search original, Turn index and Search. The search field takes focus on its tab and on ⌘F.
- Long content is virtualized, with Copy everything and Load more naming what remains ("214 KB remaining").
- Redactions render as inline mono chips with spoken labels.
- A consent step inside the review (a witness review) is a checkbox-gated `Modal` whose Confirm is prominent and never the default.

[trace-commons: PreviewSheet.swift]

## Action ordering and the confirmation ladder

**Inline cards.** In an offer card or a review card, the action comes first as a primary or glass `Button`, then decline, dismiss and secondary actions as link buttons, then the failure line (`InlineAlert`) under both. In a notice the call to action is always primary (NDS-25). Two inline confirmations in a card (Withdraw, an override in the menu-bar panel) keep cancel first.

**Action bars and modals.** Cancel leads and the primary trails, with at most one primary per surface (NDS-19). Window and sheet action bars use `size-cta` 34 for every button; modal action bars use `size-cta-small` 30.

| Rung | Use for | Desktop rendering | Keys |
|---|---|---|---|
| Act and offer Undo | Reversible actions: pause watching, ignore a folder, dismiss a notice | Runs at once; a `Toast` or the undo card offers Undo; Edit > Undo names it | ⌘Z |
| Default confirmation | Reversible but consequential: setting a folder to Automatic; clearing an override or a restriction that would resume automatic sending; setting a folder to Never when that clears waiting traces (the confirmation shows how many) | `Modal` with a default confirm. When the items' states are unknown it fails closed and asks | Return confirms, Esc cancels |
| Destructive confirmation | Destroys data: Dismiss a trace, Withdraw, Delete run | `Modal`; the destructive button trails in `destructive-text` and is never the default | Return does not confirm; Esc cancels |
| Prominent, no Return | Irreversible sends from a review or a dialog: Submit, send to an outside model | Drawn as the primary, never the default, no shortcut | Return does nothing |
| One-click row send | A trace row's or folder row's Submit pill, for a folder the person has already set to share (NDS-31) | Sends at once with no outcome question; the row dims with a `Spinner` while it sends. The pill is absent when the service isn't answering, the person isn't enrolled, the trace isn't eligible or its folder is ignored | Return on the row opens the review; it never sends |
| Checkbox-gated | Lasting consent: go public, a new reviewer, automatic sending | Confirm enables only after a `Checkbox` stating the consequence | Esc cancels |
| Inline well | Where sheets are unreliable (menu-bar panel) or the choice belongs in place (Withdraw on a card) | A well under the control with Keep and Confirm | Esc keeps |

While a modal is busy, its scrim, Esc, close button and Cancel do nothing until the work finishes.

A skipped or partial send never looks like success: the toast or a withheld line says what was not sent, and its Undo survives selecting another item.

[trace-commons: Modal.swift, cross-screen patterns 10 and 11; #1256 (clearing an override confirms); #1585 (row Submit)]

## Window sizes and breakpoints

| Measure | Value | Token |
|---|---|---|
| Main, content minimum, inspector panes | 440, 360, 293 | `size-pane-main`, `size-pane-content-min`, `size-pane-inspector` |
| Gap between panes | 10 | `pane-gap` |
| First launch shows the inspector, the content pane | 900, 1100 | `bp-inspector`, `bp-map` |
| Shell reflow (Windows, Linux, web) | 600, 840, 1200, 1600 | `bp-medium`, `bp-expanded`, `bp-large`, `bp-xlarge` |
| Modal widths, insets | 780 or 450; 28 sides, 52 top | `size-modal-width`, `size-modal-narrow`, `modal-inset`, `modal-inset-top` |
| Settings section list | 180 | `size-modal-nav` |
| Edge-rail peek, tray flyout | 380 | `size-panel-width` |
| Menu-bar panel | 285 | none (Gateway's `MenuBarGlassPanel.width`) |
| Running text | at most 680 | `size-readable-width` |

## Multi-window and the menu bar

- The macOS app has a Dock icon and a status item. Clicking the Dock icon reopens the main window. An ambient app keeps running when its last window closes; other apps follow the platform.
- Only the key window answers shortcuts and draws the focus ring. Panes in background windows take `inactive-dim`.
- The Window menu lists open windows. Settings and first run are single instance and never appear twice.
- Open in New Window detaches a conversation, an agent run or a review into an auxiliary window that keeps its own state.
- On Windows and Linux each window has its own app menu button and `CommandPalette`. On Windows, closing the last window quits unless the app lives in the notification area, and Settings says which.

See Navigation and commands for the menus, the shortcuts and the registry.

## Pointer and hover

Every hover has a keyboard-focus equivalent and a tap equivalent. Nothing important exists only under the pointer.

| Hover behavior | Keyboard focus | Without hover |
|---|---|---|
| Info text in a `Tooltip` or an info glyph's `Popover` | Shows on focus; activating the info button pins the popover | Click or tap pins it; Esc or an outside click unpins |
| Menu-bar panel's round buttons show their names | `Tooltip` on focus | The name and state are in the accessibility label |
| Edge rail opens with a 300 ms grace | The Show edge rail command focuses the first tile | Not offered without a pointer |
| Map nodes light and show a node card beside the drawn art | Arrow keys move between nodes; focus shows the card | Tap selects and shows the card |
| Bar-graph columns reveal values | Arrow keys step columns; values are announced | Tap a column; a table view gives every value (NDS-20) |
| Row actions appear (kebab, Submit pill) | Shown on the focused or selected row | Always shown; also in the context menu |
| Icon-only buttons show a label | `Tooltip` on focus | Visible labels on touch toolbars |

- A hover fill replaces the resting fill (`control-hover`, `card-hover`, `row-hover`); it never stacks, never applies to a selected row or a disabled control, and fades on `duration-fast` with `ease-standard`.
- On the web shell, gate hover styles with `@media (hover: hover)`.
- Hover never commits anything. No send, run, delete or consent happens on hover. Menus open on click; submenus may open on hover.
- A hover card never covers what it describes. Place a map node's card beside the node's drawn art (measured from the art, not the node's dot): to the right when it fits, else to the left, `space-12` from the art and at least `space-8` from the pane's edge, 260 wide, clamped 48 from the top and bottom. It shows on hover or keyboard focus only; a click never pins it. An info button's `Popover` still pins on click.
- A row's chevron and menu button are not tab stops; the row's own keyboard model reaches them.
- Pointer shapes: the arrow over buttons, the pointing hand over links only, the I-beam over text, resize pointers over splitters, the copy and not-allowed pointers during a drag. The web shell keeps the arrow on buttons to match the OS.
- The pointer target is `target-pointer` 28, never below 20. Adjacent toolbar targets touch so the pointer never falls between them. Small glyphs (info, a card's close X) get an invisible hit area up to 28.
- A secondary click always opens the context menu.

[trace-commons: gaps 9.1 item 2; FlowMapView.swift node cards (#1672)] [HIG: pointing devices]

## Drag and drop

- Within one container a drag moves; into another container it copies; between apps it always copies. Use the platform's copy modifier: Option on macOS, Ctrl on Windows and Linux.
- Show the drag image after about 3 points of movement. Highlight a destination only while a valid item hovers over it; an invalid one shows the not-allowed pointer and nothing else. A failed drop springs back on `spring-spatial`, or fades under Reduce Motion.
- A drop zone at rest is a dashed 1px border in `text-tertiary` with `radius-control`. While a valid item hovers, the border turns `accent` over an `accent-tint` fill.
- Every drop has another path: an Add button or file chooser, paste, and a Move to… command for assistive technology.
- A drop stages; it never sends. Dropping files on the composer or a folder onto first run adds them for the person to review. Make drops undoable.
- Show a placeholder and a `ProgressBar` at the drop point while a slow drop lands. A rejected drop says why in an `InlineAlert`.
- Reorder only lists whose order means something. The insertion line is 2px `accent`; in a tree it starts with a small circle at the target depth.
- Dragging content out offers the richest format first, then Markdown, then plain text.

[HIG: drag and drop] [Unity Foundations: interactions]

## Undo and redo

Reversible actions act at once and offer Undo (NDS-15). One Undo command renders three ways on the desktop: Edit > Undo with the action's name (⌘Z; Ctrl+Z, with Ctrl+Y and Ctrl+Shift+Z for Redo), a `Toast` with an Undo button, and in Gateway the undo card, which stays until dismissed. The undo card sits above the list it acts on: above the Traces tree on Traces, at the top of the inspector on the other tabs.

- Name the action: "Undo Ignore", "Undo Pause watching".
- Count up from a real moment ("Paused 12 s ago"). Never count down to a deadline the app cannot see.
- Show the result. Scroll to and select what came back, and open the inspector if that is where it lives.
- Keep undo back to when the window opened. A drag, a scrub or a burst of typing is one entry, committed on release, Return or blur.
- Batch agent changes: every change an agent makes can be undone, and "Undo changes from this run" reverses the run.
- Irreversible actions cannot be undone, which is why they confirm.

[HIG: undo and redo] [trace-commons: InspectorPrompts.swift]

## Notifications on desktop

- Ask permission when a notification first helps, such as after people start work that finishes later. Never ask at first launch. Settings has a switch per category.
- Notify only about work people started and decisions they owe. When the window is in front, update it in place instead.
- Map urgency: a result ready is Active; a decision with a deadline within the hour is Time Sensitive; digests and suggestions are Passive; nothing is Critical. Windows and Linux use their normal urgency; Linux never uses critical.
- Keep prompts, outputs, file paths and personal data out of the title and body. Payloads carry ids.
- Offer at most two actions: one that opens the item (Gateway: Review) and one that defers it (Not now). No notification action sends, uploads or grants consent.
- Notify once per event; never repeat for something people ignored.
- The Dock badge and the Windows taskbar overlay show decisions owed only, the same number as the tab's `Badge`. Clear it at zero; show nothing when the count is unknown.
- Words come from the product's copy source, like every other surface.

[HIG: notifications, managing notifications] [trace-commons: contributor shell spec 2026-08-08]

## Windows and Linux shells

The shells render every pattern above with the web components. These are the differences.

| Concern | macOS (lead) | Windows | Linux |
|---|---|---|---|
| Toolkit | SwiftUI and AppKit | Tauri (WebView2), React components on the parent tokens | Tauri (WebKitGTK), same components |
| Panes | Liquid Glass `regular` tinted with the veil on macOS 26 and later, vibrancy on 14 to 25, then `glass-veil` and `pane-fill` (NDS-7) | Windows 11: Mica behind the window, `glass-veil` and `pane-fill` painted over it. Without Mica: `.nr-scene` with `blur-pane` | `pane-base`, with blur only where the compositor provides it and the frame budget holds |
| Floating layer | Painted over a within-window blur | `.nr-floating`; separate flyouts on Acrylic | `.nr-floating`, or `pane-base` |
| Frame | Hidden title bar; traffic lights in the main pane | System title bar and caption buttons, or content extended into the title bar with the system buttons kept | The desktop's own decorations |
| Window corners | System | The OS rounds a system frame; `radius-window` 22 only on a window the app draws, such as the tray panel | Same as Windows |
| Commands | Menu bar | App menu button and `CommandPalette` (Ctrl+K) | Same as Windows |
| Ambient surface | Menu-bar panel, edge rail | Notification-area flyout | Tray, where supported |
| Type | SF Pro text styles, `mac-*` | `web-*` steps in Segoe UI Variable through `--font-web` | `web-*` steps in the desktop's sans through `--font-web` |
| Focus ring | On by default (NDS-5); Gateway turns it off | On | On |
| Increased contrast | Increase Contrast selects the `-hc` themes | Contrast themes arrive as `forced-colors: active`: system colors and real borders | `prefers-contrast: more` selects the `-hc` themes |
| Reduced transparency | The system's to apply: the native material frosts itself and the painted veil and fill stay (NDS-23) | Transparency effects off: `pane-opaque` | `pane-opaque` |

- The shells use the web app's regular density with pointer targets (`.nr-regular`, `target-pointer` 28) and never ship SF (NDS-4). Pro-tool panels opt into dense as on the Mac.
- Keep Cancel leading and the primary trailing (NDS-19) although native Windows dialogs lead with the primary.
- Turning the focus ring off, as Gateway does, fails WCAG 2.4.7 (Focus visible).
- Test every Windows screen with a contrast theme on.

[trace-commons: cross-platform 8.1 to 8.5] [Liquid Glass: Windows and Linux]
