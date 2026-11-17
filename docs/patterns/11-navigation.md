# Navigation and commands

Near AI products share one information architecture and one command registry. Each platform renders them with its own idioms (NDS-3): a floating glass `TabBar` on iPhone, a `NavigationRail` on Android tablets and the web, a `Sidebar` or the three-pane window on the desktop, a menu bar on macOS and iPadOS, and a `CommandPalette` where there is no menu bar. This section sets which component carries navigation at each layout class, how deep a hierarchy may go, how Back works, where search lives, and how one command reaches menus, palettes, shortcuts and the system.

## The navigation model

### Layout class picks the component

Measure the window or the container, never the device (NDS-12). The class decides how many panes fit and which primary navigation shows. Apple's size classes only choose between idiom components (tab bar or sidebar, sheet or popover).

| Class | Width | iPhone and iPad | Android | Web | macOS, Windows, Linux | Panes | Margin |
|---|---|---|---|---|---|---|---|
| Compact | < 600 (`bp-medium`) | iPhone: floating glass `TabBar`. iPad Slide Over or a narrow split: `TabBar` | `TabBar` (M3 navigation bar, 64 tall); overflow in a modal expanded `NavigationRail` | Bottom `TabBar` plus a top `Toolbar` | Main pane only (the window is the sum of its panes) | 1 | `margin-compact` 16 |
| Medium | 600 to 839 | iPad portrait: tab bar at the top, sidebar-adaptable | Collapsed `NavigationRail`, `size-rail-collapsed` 96 | Collapsed `NavigationRail` 96 | Main pane plus a sheet for detail | 1 | `margin-medium` 24 |
| Expanded | 840 to 1199 (`bp-expanded`) | iPad landscape: `Sidebar` from the adaptable tab bar | Collapsed or expanded rail | Collapsed rail; expanded on request | `Sidebar` or the three-pane window, two panes visible | 2 | `margin-expanded` 24 |
| Large | 1200 to 1599 (`bp-large`) | iPad 13 inch landscape: `Sidebar` | Expanded rail (standard, pushes content) | Expanded rail `size-rail-expanded` 220 to 360, or `Sidebar` | Three panes | 2 to 3 | 24 |
| Extra-large | 1600 and up (`bp-xlarge`) | Not reached | Expanded rail | Expanded rail or `Sidebar` | Three panes; running text capped at `size-readable-width` 680 | 3 | 24 |

- Use one primary navigation component per window. Never pair a bottom `TabBar` with a `NavigationRail`, and never put a bottom `Toolbar` beside a `TabBar`.
- Never build a navigation drawer. Where Material would use one, use the expanded `NavigationRail`, modal over `scrim` at compact and medium.
- Primary navigation holds destinations only. Actions go in a `Toolbar`, an `ActionBar` or a `Menu`.
- Treat a height under 480 (iPhone in landscape) as compact height: one pane, short bars, the `TabBar` minimizes on scroll. Keep the tab bar visible while VoiceOver or TalkBack runs.
- Label every destination at every class. Selecting the current destination again scrolls it to the top.

### Form factors

- **Phone.** A bottom `TabBar` with three to five destinations (NDS-13). iOS draws it as the system's floating Liquid Glass bar with an optional trailing search tab; Android draws the M3 navigation bar on `blur-bar`. See Phone patterns.
- **Tablet.** iPad uses the sidebar-adaptable tab bar, which people can switch between a top tab bar and a `Sidebar`. Android and touch web use the `NavigationRail`. See Tablet patterns.
- **Desktop.** A `Sidebar` (`size-sidebar` 280) or the three-pane window, plus a `Toolbar` and the menu bar or `CommandPalette`. See Desktop patterns.
- **Spatial.** visionOS moves the tab bar into a vertical ornament on the window's leading edge. See Spatial patterns.

Choose the desktop structure by the shape of the information. Use a `Sidebar` when the app moves among more than five areas or among collections people create (conversations, projects, agents). Use the three-pane window when the app has up to five top-level areas that share one overview: a fixed main pane carrying `Tabs`, a flexible content pane and an inspector. The Gateway monitor is the reference: Home, Private AI, Traces and Insights in the main pane, the map in the content pane, the trace review in the inspector.

### Crosswalk

| Concept | Component | iOS and iPadOS | macOS | Android (M3) | Web |
|---|---|---|---|---|---|
| Primary navigation, bottom | `TabBar` | Floating glass tab bar | None | Navigation bar, 64 | Bottom bar at compact |
| Primary navigation, side, collapsed | `NavigationRail` | iPad tab bar (sidebar-adaptable) | Collapsed sidebar | Rail, 96 | Rail, 96 |
| Primary navigation, side, expanded | `Sidebar` or expanded `NavigationRail` | Sidebar in a split view | Source-list sidebar | Expanded rail, 220 to 360 | Expanded rail or sidebar |
| Top-level areas inside a pane | `Tabs` | Segmented control | Rule tabs | Primary tabs | Tabs |
| View switch inside a pane | `SegmentedControl` | Segmented control | Segmented control | Connected button group | Segmented control |
| Drill-down path | `Breadcrumb` | Navigation stack with a back button | Breadcrumb or path control | Top app bar with back | Breadcrumb |
| Title and screen actions | `Toolbar` | Toolbar; large title collapses on scroll | Window toolbar | Top app bar, small to large | Top bar |
| Supplementary detail | Inspector `Pane`, or `Sheet` | Inspector; a sheet at compact | Inspector pane | Side sheet; bottom sheet at compact | Inspector pane; sheet at compact |
| Back | System | Back button and edge swipe | Breadcrumb back, Esc | System back with predictive back | Browser history |

[M3: navigation bar, navigation rail] [HIG: tab bars, sidebars] [trace-commons: MonitorWindowView.swift]

## Hierarchy depth

Keep navigation shallow and put depth in content.

- Hold three to five destinations in a `TabBar` (iPad defaults to five or fewer so compact and regular widths match) and three to seven in a `NavigationRail`.
- Show at most two levels in a `Sidebar`: group headings and items. For anything deeper add a list column (list-detail) or a tree in the content pane.
- Never disable a tab or a rail item, and never hide one to report state. A destination with nothing to show opens to its `EmptyState` ("No agents yet"). A product may show a reduced set before setup finishes (Gateway shows only Private AI until first run completes); it never shows a disabled one.
- Report counts that need action with a `Badge` on the destination. Gateway counts decisions owed and caps at 99+; a tab draws a dash when the count is unknown, and the menu-bar `StatusItem` hides its badge instead (NDS-33). Never badge queue depth or credit.
- Drill down inside a pane with a `Breadcrumb` (Traces › History › Gateway; Gateway's own shell draws the separator as "/"). A sub-page lives under the tab whose content it extends: Gateway's History sits inside Traces. The back chevron and Esc go up one level. Stop at three crumbs; a fourth level opens in its own window or `Sheet`.
- In list-detail, show the back button only in single-pane mode and the selected row only in two-pane mode. Widening with no selection shows the detail `EmptyState`; narrowing with a selection shows the detail.
- Draw data hierarchies (folders and traces, a run and its tool calls) as a tree of `ListRow`s in the content pane, one tab stop with arrow keys. A tree is content; it never replaces primary navigation.
- Keep each destination's state when people leave and return: scroll position, selection, sub-page, pane visibility. Restore it per window on relaunch.
- Show the selected destination with two cues: the indicator (fill, ember or pill) and a filled glyph or heavier label.

[HIG: sidebars, tab bars] [M3: list-detail] [trace-commons: Navigation.swift]

## Back and history

| Platform | Back control | Gesture and keys | Rules |
|---|---|---|---|
| iOS, iPadOS | Back chevron at the leading edge of the toolbar, a symbol with no "Back" text | Interactive edge swipe pops the stack; swipe down dismisses a sheet | Keep the edge swipe working everywhere except a canvas that needs horizontal drags. Confirm before a swipe discards an unsent prompt or unsaved input |
| Android | Top app bar arrow, only when the stack is not empty | System Back with predictive back: the previous screen previews as the gesture runs | Back closes, in order: a menu or search view, a sheet, the modal rail, then the stack; at the start destination it leaves the app |
| Web | In-app back in the top `Toolbar` at compact, `Breadcrumb` above | Browser Back and Forward | Push history for destinations and sub-pages; replace it for in-pane switches. At compact a full-screen `Sheet` or search view pushes one entry so Back closes it. See Web patterns |
| macOS | `Breadcrumb` back chevron | Esc goes up one breadcrumb level; ⌘[ and ⌘] step through a window's history when it keeps one | No app-wide back gesture. Swipe between pages only in paged content |
| Windows, Linux shells | `Breadcrumb` back chevron | Alt+Left and Alt+Right; mouse back and forward buttons | Same history model as the web |

- Esc works as a ladder on desktop and web. The first press closes the topmost transient surface (tooltip, then menu or popover, then a sheet or modal that is not busy). The next clears a filled search field. The next goes up one breadcrumb level. Esc never discards typed content without a confirmation.
- Back never runs an action and never stops agent work. Leaving a running conversation keeps the run going (see AI and agent patterns).
- Never intercept Back to ask "Are you sure?". Autosave drafts instead, and confirm only when input would be lost.
- In a pro-tool window, selection is the navigation: ⌘[ and ⌘] (Ctrl+[ and Ctrl+] elsewhere) walk the selection history. See Dense and pro-tool patterns.

[HIG: gestures] [M3: predictive back]

## Search placement

| Form factor | Placement | Focused layout | Keys |
|---|---|---|---|
| iPhone | `SearchField` in the bottom toolbar, or a search tab at the trailing end of the `TabBar`; at the top only when bottom content must stay visible | The field rises above the keyboard; results replace the content | Hardware keyboard: ⌘F |
| iPad | Trailing end of the `Toolbar`. At the top of the `Sidebar` when it filters sidebar items. A search tab for a dedicated discovery area | Results fill the content column; in compact widths the field moves above the list column | ⌘F |
| macOS | `SearchField` at the trailing end of the toolbar or the main pane's top row | Results filter or replace the content pane; never a modal | ⌘F focuses the view's field; ⌥⌘F jumps to the toolbar field |
| Android | M3 search bar: a 56 tall pill at the top, 360 to 720 wide | Full-screen search view at compact; docked under the bar at medium and up; Back closes it | None |
| Web | `SearchField` in the top `Toolbar`; the `CommandPalette` searches commands and destinations | Full-screen at compact; a docked results panel at medium and up | Mod+K for the palette. Leave Mod+F to the browser unless content is virtualized, where in-app find replaces it and says so |
| Windows, Linux shells | Top row field and the `CommandPalette` | Docked results panel | Ctrl+K palette, Ctrl+F in-view find |

- One place searches everything. A local field filters only its view, and its placeholder names the scope ("Search traces in near-agents").
- Show recent searches before typing and suggestions while typing. Let people clear recents, and keep them off shared surfaces such as the menu-bar panel, the edge rail and widgets.
- Search as people type when results are local. When results need a server or a model, show suggestions at once and results on Return.
- When one field can both search and ask an agent, show the mode on the field and send nothing to a model until that mode is chosen. The palette's explicit "Ask Near AI" row is the pattern.
- Esc clears the field; a second Esc leaves search. Announce the result count politely to assistive technology.

[HIG: search fields, searching] [M3: search]

## The command registry

Every action an app offers is declared once and rendered on every surface that shows it (NDS-14). `Menu`, `CommandPalette`, `Toolbar`, `IconButton`, `SplitButton`, context menus, the menu bar and App Intents all read from the registry. No surface invents its own command.

### The command record

| Field | Meaning | Gateway example |
|---|---|---|
| Id | Stable identifier | `traces.trace.review` |
| Label | Words from the product's copy source: a verb, or a verb and object (NDS-16) | Look inside |
| Accessible name | Label plus object when the control repeats | Look inside trace from 09:14 |
| Symbol | One glyph from the icon registry (see Iconography) | Eye |
| Shortcut | Written `Mod+Key`; optional | Return, inside the tree |
| Enablement | When it can run, and the sentence that says why when it cannot | Needs the watcher to answer |
| Surfaces | Where it appears | Menu bar, context menu, palette, inspector card |
| Confirmation | Its rung on the confirmation ladder (NDS-15) | None |
| Exposure | App Intent, App Shortcut, Android shortcut, jump list | None |
| Menu | Its menu and group in the menu bar | Traces |

- Put every toolbar item and every context-menu item in the menu bar on macOS and iPadOS, and in the `CommandPalette` on web, Windows and Linux.
- Give irreversible sends and consent actions (Gateway's Submit, Go public) no shortcut and no Return key. The palette may list them; choosing one opens the review where the action lives. A row's Submit pill is the one place a send is a single click (NDS-31), and only for a folder the person has already set to share. Never expose sends as one-step App Intents.
- Use the same label on every surface. The shell may adapt case and punctuation to the platform: title case and a trailing ellipsis for macOS and iPadOS menu-bar items that need more input, sentence case everywhere else, no ellipsis on Windows.
- Toggle commands change their label with state (Show inspector, Hide inspector) or carry a checkmark in menus.
- A command that cannot run explains why: in its `Tooltip`, on the palette row's second line, and as a dimmed menu-bar item. In rows and cards it is hidden instead (NDS-41).
- Read shortcuts for tooltips, menus and the palette from the registry. Never hard-code a shortcut string in a component.

### The menu bar on macOS and iPadOS

Keep the system order: App, File, Edit, Format, View, the app's own menus, Window, Help. Every Near AI desktop app ships App, File, Edit, View, Window and Help. Format appears only when the app edits rich text.

| Menu | Near AI baseline | Rules |
|---|---|---|
| App (Near.ai) | About Near.ai · Settings… ⌘, · app items · Services · Hide Near.ai ⌘H · Hide Others ⌥⌘H · Show All · Quit Near.ai ⌘Q | About first and alone; app name 16 characters or fewer; Settings lives here |
| File | New Chat or New Window ⌘N · Open in New Window · Close ⌘W · Export Conversation… | Name the type created; keep File even without documents, for windows |
| Edit | Undo [action] ⌘Z · Redo [action] ⇧⌘Z · Cut · Copy · Paste · Paste and Match Style ⌥⇧⌘V · Delete · Select All ⌘A · Find ▸ | Undo and Redo name their target ("Undo Ignore") |
| View | Show or Hide Sidebar ⌃⌘S · Show or Hide Inspector ⌥⌘I · areas ⌘1 to ⌘9 · Show or Hide Toolbar ⌥⌘T · Enter Full Screen ⌃⌘F | Always present; labels follow the current state |
| App menus (one to three) | Gateway: Traces (Look Inside, Submit, Submit As…, Dismiss). An agent app: Conversation (Send, Stop ⌘., Regenerate, Branch) and Model | Between View and Window; list every custom command; order from general to specific |
| Window | Minimize ⌘M · Zoom · Bring All to Front · open windows | Always present, even with one window; windows listed alphabetically; no panels or modals |
| Help | Near.ai Help · Release Notes | Trailing |

- Disable unavailable items in the menu bar; never hide them. Context menus, row menus and cards do the opposite: they hide what cannot run (NDS-41).
- Use one-word menu titles. Dynamic items (a modifier reveals an alternate) use one modifier and are never the only path.
- On iPadOS the bar stays hidden until people point to or swipe from the top edge. Everything in it must also be reachable in the interface. Settings opens the app's page in the Settings app; in-app settings go in an item under it. List the top-level areas in View with ⌘1 to ⌘9.
- The menu-bar panel (an extra) is covered in Desktop patterns. Never rely on it being visible; mirror its commands in the Dock menu and the main window.

[HIG: the menu bar] [trace-commons: TraceCommonsAppMain.swift]

### Windows, Linux and web

There is no global menu bar. The `CommandPalette` carries the whole registry, grouped by the Mac menu names, with each command's shortcut and enabled state. An app menu button at the leading end of the top row opens the same groups as a `Menu`: About sits under Help, Quit under File (the copy source supplies "Exit" for Windows), Settings under File. Draw Alt+letter access keys only where an in-window menu bar is drawn. The browser keeps Mod+W, Mod+T, Mod+N, Mod+L, Mod+R, Mod+Q and Ctrl+Tab; never bind them on the web. See Web patterns.

### Context menus

- Open one with a secondary click, Control-click on a Mac, Shift+F10 or the Menu key on Windows, Linux and the web, and a long press on touch. Every row with a context menu on web or touch also shows a visible More `IconButton`.
- Hold only the most relevant, frequent commands, in about three groups or fewer, with one submenu level at most.
- Hide unavailable items. macOS keeps Cut, Copy and Paste visible and dimmed.
- Put destructive items last, after a separator, in `destructive-text`.
- Show shortcuts in context menus on Windows, Linux and the web; omit them on Apple platforms.
- Give icons to every item in a group or to none. Add a title only to clarify scope ("3 traces").
- Every item also exists in the main interface. On iOS an item has a context menu or an edit menu, never both.
- A message in a conversation offers Copy, Regenerate, Edit, Share, a separator, then Delete.

[HIG: context menus] [Unity Foundations: menus]

### Command palette

The `CommandPalette` opens with Mod+K and from a visible search button in the top `Toolbar`. It is required on web, Windows and Linux and optional on macOS, where the Help menu's search already finds menu commands.

- Each row shows the glyph, the label, the menu path in `text-tertiary` and the shortcut at the trailing end. Recent commands come first.
- List only commands that can run now; a disabled menu-bar item becomes an absent palette row. Destinations appear in their own group.
- Choosing a command runs it with its usual confirmation rung. Esc closes the palette and returns focus to where it was.
- At compact the palette opens as a full-screen sheet; elsewhere it floats near the top of the window at `size-modal-narrow` 450 on the floating layer.

[Unity Foundations: contextual tooling] [trace-commons: GlassMenu]

## Keyboard shortcuts

### Modifiers and notation

| Role | macOS | Windows and Linux | Rule |
|---|---|---|---|
| Primary | Command ⌘ | Ctrl | The registry writes `Mod` |
| Secondary | Shift ⇧ | Shift | Adds a related command: ⌘Z and ⇧⌘Z |
| Rare | Option ⌥ | Alt | Power commands only; Alt+letter opens access keys on Windows |
| Avoid | Control ⌃ | None | The system uses Control on the Mac; never map it to Windows Ctrl |
| Display | Glyphs, no separators, in the order ⌃⌥⇧⌘ then the key: ⌥⇧⌘V | Words joined by "+", in the order Ctrl, Alt, Shift, then the key: Ctrl+Shift+V | The web detects the platform and renders accordingly |

- Add custom shortcuts only for the most frequent app-specific commands.
- Never add Shift to reach a key's upper character: Help is ⌘?, never ⇧⌘/. ⌘ with any key is safe on every keyboard layout; use other modifiers only with letters.
- Never add a modifier to an existing shortcut to mean an unrelated command.
- A shortcut with no modifier works only while its pane has focus, and people can turn it off or remap it (WCAG 2.1.4).
- Never bind Mod+Space. Any global launcher shortcut is off until a person chooses one.
- On visionOS, holding ⌘ lists every command with a shortcut, grouped by menu with no submenus, so each label must make sense on its own.

### Shortcuts the system reserves

Every Near AI app keeps these bindings. A product never rebinds them.

| Command | macOS | Windows and Linux shells | Web | Rule |
|---|---|---|---|---|
| Settings | ⌘, | Ctrl+, | Mod+, | Opens the Settings window or page (NDS-21) |
| New chat or new window | ⌘N | Ctrl+N | Browser keeps it | Web offers the command in the palette |
| Close window | ⌘W | Ctrl+W | Browser keeps it | Closes the key window; its state returns when it reopens |
| Quit | ⌘Q | Alt+F4 on Windows, Ctrl+Q on Linux | None | |
| Undo, redo | ⌘Z, ⇧⌘Z | Ctrl+Z; Ctrl+Y and Ctrl+Shift+Z | Mod+Z, Mod+Shift+Z | Names the action in the Edit menu and the `Toast` |
| Cut, copy, paste, select all | ⌘X, ⌘C, ⌘V, ⌘A | Ctrl+X, C, V, A | Same | |
| Paste and match style | ⌥⇧⌘V | Ctrl+Shift+V | Mod+Shift+V | |
| Find, next, previous | ⌘F, ⌘G, ⇧⌘G | Ctrl+F, F3, Shift+F3 | Browser keeps Mod+F except in virtualized content | |
| Command palette | ⌘K (optional) | Ctrl+K | Mod+K | |
| Stop a running generation | Esc, ⌘. | Esc | Esc | When focus is in the composer or transcript and no transient surface is open; ⌘. works anywhere in the window |
| Close the topmost transient surface | Esc | Esc | Esc | Busy modals ignore it |
| Switch top-level area | ⌘1 to ⌘9 | Ctrl+1 to Ctrl+9 | None (the browser switches tabs) | Gateway: ⌘1 Home, ⌘2 Private AI, ⌘3 Traces, ⌘4 Insights (the default order; Home stays first, NDS-37) |
| Back, forward | ⌘[, ⌘] | Alt+Left, Alt+Right | Browser keeps them | In pro tools, selection history |
| Show or hide inspector | ⌥⌘I | Palette | Palette | |
| Full screen | ⌃⌘F | F11 | F11 (browser) | |
| Help | ⌘? | F1 | None | |

Never bind what the operating system or the browser owns: ⌘Space and ⌃Space (Spotlight, input sources), ⌘Tab, ⌘\`, ⌘H, ⌘M, ⌥⌘Esc, ⇧⌘3, ⇧⌘4, ⇧⌘5, ⌃F1 to ⌃F7, ⌘F5 (VoiceOver); the Windows key with anything, Alt+Tab, Ctrl+Alt+Delete, Ctrl+Shift+Esc; in browsers Mod+T, Mod+W, Mod+N, Mod+L, Mod+R, Mod+Q, Mod+Shift+N, Mod+Shift+P, Ctrl+Tab and Ctrl+1 to Ctrl+9.

[HIG: keyboards] [trace-commons: TraceCommonsAppMain.swift]

## App Intents and App Shortcuts

The registry also feeds the system. On Apple platforms, mark the commands people run most as App Intents, so Siri, Spotlight, Shortcuts, the Action button, Controls and widgets can run them.

- Adopt an Apple app schema where one fits the domain; use App Shortcuts for the rest. Offer at most 10 App Shortcuts, each with at most one optional parameter whose values are predictable.
- Include the app name in each phrase ("Pause watching in Near.ai", "Ask Near.ai"). Finish in place with a snippet when the task is simple ("Paused until morning."); open the app for anything with more than one step.
- Never run an irreversible send, a consent change or a payment from an intent. Open the review instead.
- Never present an agent as Siri or as a system assistant.
- Use the same exposed actions for the Dock menu (New Chat, New Window, recent conversations), the iOS Home Screen quick actions (four at most), Android app shortcuts, Windows jump lists and the web app manifest's shortcuts.

See AI and agent patterns for snippets and Live Activities. [HIG: App Shortcuts, Siri]

## Deep links

- Give every destination and every selectable item a route. The same route opens from a custom URL scheme, a universal link or Android App Link, and a web URL.
- Opening a link rebuilds the parents so Back works: a synthesized back stack on phones, the `Breadcrumb` on desktop, the in-app back button on the web even when browser history is empty.
- A link never performs an action. It may open the place where an action lives, such as a review or a confirmation; sends and consent wait for the person.
- When people are signed out, route through sign-in and continue to the destination. An invite link opened after setup opens the main window.
- An unknown, expired or forbidden link opens an `EmptyState` that says what happened and offers a way back to the start destination.
- Widgets, notifications, Live Activities and snippets each link to the exact item. Their payloads carry ids only, never prompt text, output or file paths.

[HIG: widgets, Live Activities] [trace-commons: R15 plan D-14]

## Multiple windows

- A primary window holds navigation and content. An auxiliary window holds one task, offers no navigation and has a close button: Settings, first run, a review, a detached conversation.
- Offer Open in New Window in the context menu and the File menu for long-lived items such as a conversation, an agent run or a trace review. On iPad, support pinch to open and dragging an item to the screen edge.
- Reuse single-instance windows. A second ⌘, brings the open Settings window forward.
- Each window keeps and restores its own navigation, selection and pane visibility. A change made in one window appears at once in every other window of the same account.
- Only the key window answers shortcuts. Background windows dim their panes with `inactive-dim`.
- On the web each browser tab is a window. The app never opens a tab for in-app navigation; Open in New Tab sits in the context menu and on Mod+click.
- On Windows and Linux each primary window is its own OS window with its own app menu button and palette. The OS title reads the window's subject; the app name appears in the title or taskbar only, never as an in-view heading.

[HIG: windows, multitasking] [Unity Foundations: windowing]
