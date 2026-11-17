# Web patterns

The web shell renders Near AI products in a browser, in the Windows and Linux desktop shells (Tauri) and on mobile web. It uses our own components on the parent tokens (decision NDS-18) and keeps what people expect from the web: every place has a URL, Back works, text zooms, and the page adapts to any window. On the web the glass has no desktop behind it, so the `.nr-scene` gradient stands in for one.

## Layout classes and container queries

Classify layout by the width of the window or the container, never by device (NDS-12). The viewport class decides which navigation shows and how many panes fit. A container query inside each pane decides how components inside it lay out.

| Class | Width (px) | Media query | Panes | Navigation | Margin |
|---|---|---|---|---|---|
| Compact | < 600 | `(max-width: 599px)` | 1 (each pane is a page) | Bottom `TabBar` + top `Toolbar` | `margin-compact` 16 |
| Medium | 600 to 839 | `(min-width: 600px)` | 1, or 2 at 50/50 for light content | Collapsed `NavigationRail` 96 | `margin-medium` 24 |
| Expanded | 840 to 1199 | `(min-width: 840px)` | 2 | Collapsed or expanded rail | `margin-expanded` 24 |
| Large | 1200 to 1599 | `(min-width: 1200px)` | 2, or the three-pane window | Expanded rail 220 to 360, or `Sidebar` | 24 |
| Extra-large | 1600 and up | `(min-width: 1600px)` | 3 (third is the inspector) | Expanded rail or `Sidebar` | 24 |

- Generate the media queries from `bp-medium`, `bp-expanded`, `bp-large` and `bp-xlarge` at build time. CSS custom properties do not work inside `@media` conditions, so never hand-type the numbers.
- Make every pane a size container (`container-type: inline-size`) and write component layouts against it. The inspector at `size-pane-inspector` (293) and the same inspector shown as a full page at compact then pick their layouts from their own width. This replaces SwiftUI's `ViewThatFits` in the review card's action row: inline buttons when the container is wide enough, stacked when it is not.
- Treat a height under 480 (a phone in landscape) as compact height: keep one pane, keep bars short, and never pin two bars at once.
- Support 200% browser zoom and reflow at 320 CSS px with no horizontal scrolling (WCAG 1.4.10). Zoom halves the effective width, so a 1280 window at 200% is a medium layout. Size type in `rem` on a 16px root so browser text settings scale it.
- Cap running text at `size-readable-width` (680) at every class. Panes grow on large screens; lines do not.
- Choose density from the input device. `@media (pointer: coarse)` puts the shell in `.nr-touch` (48 targets, `target-touch-android`); a mouse or trackpad keeps `.nr-regular` (28 targets, `target-pointer`). Gate every hover affordance with `@media (hover: hover)` and give it a focus and tap equivalent.
- Use logical properties (`margin-inline-start`, `inset-inline-end`) so the rail and the inspector swap sides in right-to-left languages.

[M3: breakpoints] [HIG: layout]

## The glass app shell

The shell is a scene with panes floating on it. Panes are the navigation layer (glass); everything inside a pane is the content layer (painted); menus, popovers and the command palette are the floating layer (NDS-9). See Glass and materials for the recipes.

| Region | Layer | Web recipe | No `backdrop-filter` support | Reduced transparency, forced colors, slow device |
|---|---|---|---|---|
| Page ground | Scene | `.nr-scene`: `scene`, `scene-warm`, `scene-glow-1` to `-3`, filling `100dvh` | Same | Flat `scene` |
| Rail, sidebar, panes | Navigation | `.nr-pane`: `blur-pane` under `glass-veil` and `pane-fill`, `radius-pane`, `shadow-float` | `pane-base` | `pane-opaque` |
| Top and bottom bars at compact | Navigation | `blur-bar` under `glass-veil`, shown once content scrolls under the bar | `pane-base` | `pane-opaque` |
| Cards, rows, fields, charts | Content | `card`, `card-quiet`, `field`, `control`, `surface-chart` | Same | Same, plus `edge-hc` in the `-hc` themes |
| Menus, popovers, tooltips, `CommandPalette` | Floating | `.nr-floating`: `blur-floating` under `popover` or `menu` | `pane-base` | `pane-opaque` |
| `Modal` | Modal | `pane-base` and `pane-fill`, `shadow-modal`, over `scrim-modal` and `blur-scrim` | Scrim without blur | Scrim without blur |

**Spacing.** Panes sit `pane-gap` (10) from each other and from the viewport edge, and content sits `pane-padding` (12) inside a pane, so content lands 22 from the window edge. Pages without panes (compact screens, settings at compact) use `margin-compact` 16 and `margin-medium` 24 directly; marketing pages use their own grid (see *Marketing pages*). Where an element hugs its container, its corners are concentric (outer radius minus the padding between them, never below `radius-tile`).

**The glass budget.** Show about four glass surfaces per viewport and at most one large blurred surface. Count every pane, bar and floating surface that has its own `backdrop-filter`.

- The panes of the window form one glass group. Render one shared backdrop element clipped to the panes (the grouping rule in Glass and materials), so the panes count as one large surface. If the build cannot share a backdrop, keep `blur-pane` on the main pane only and paint `glass-veil` and `pane-fill` straight over the scene for the others. The scene is a static gradient, so a blurred copy of it looks almost the same as an unblurred one.
- A control group floating inside a pane (the Traces / Private AI `SegmentedControl` over the map, a zoom `Toolbar`, a node card) is painted with `popover` and takes no blur of its own. A second blur there is glass on glass.
- Open one floating surface at a time. A submenu replaces nothing and counts as the same surface.

| Layout | Glass surfaces |
|---|---|
| Three-pane window with a menu open | Pane group (1) + menu (1) = 2 |
| Rail and two panes with the command palette open | Rail and panes as one group (1) + palette (1) = 2 |
| Compact page with both bars and a menu | Top bar (1) + `TabBar` (1) + menu (1) = 3 |
| Compact page with a sheet | Sheet chrome replaces both bars; scrim is not glass = 1 |

**Floating opacity.** `popover` and `menu` are 94% opaque, so the rows, pills and Submit buttons under a menu never show through it (NDS-24). The blur behind them is for depth, not legibility.

**Compact.** Below 600 the scene goes away and the page itself is an opaque pane (`pane-base`), as on phones. Only the bars float, and they take `blur-bar` only when content is behind them. See Phone patterns.

[Liquid Glass: non-Apple platforms] [trace-commons: glass.css]

## The chat shell

The Near AI chat (the private chat built on LibreChat) uses an opaque shell instead of the glass panes, because a browser has no desktop behind its glass (NDS-44). It is that product's shell, not a replacement for the glass app shell, and it keeps this section's layout classes and navigation model (NDS-12, NDS-13).

| Region | Expanded and up | Medium | Compact |
|---|---|---|---|
| Frame | The `scene` color fills the window | Same | The page is the pane, full bleed |
| Navigation | An icon rail on the scene; its buttons open the chats panel, prompts and bookmarks | The rail collapses; the chats panel opens over the page | The `TabBar` or a top-bar menu button |
| Top band | 48 tall, on the scene, above both cards: the masthead (Near AI N 22 + wordmark 18 tall, NDS-27) over the panel, then the conversation title (`web-label` medium, truncated) and the chrome buttons | Same | An overlay top bar with the model picker |
| Cards | The chats panel (`card-on-opaque`, rows 36 tall, "New chat" first) and the conversation card, 8 from the window's edges, `radius-pane` 20 on their outer corners, meeting at a 1px line with square inner corners | The conversation card only | No cards; the page is the pane |
| Composer | `radius-pane` 20, two rows, the model picker after the attach button | Same | Folds to one 54 pill row (attach, text, send) while the draft is empty or one line |

- Chrome icon buttons (bookmark, proof, share, temporary chat, overflow) show their container only on hover, press and while their menu is open (`IconButton`, toolbar variant, 36 on the web).
- The current chat in the panel takes `accent-tint` over the panel with no edge bar; hover and press are two clearly separate grey steps (see `Sidebar`).
- The deployment's proof pill sits in the band's trailing group; each signed reply leads its actions with a `ProofTag` (NDS-43).
- The empty thread is the welcome described in AI and agent patterns: the drawn N, a title and a subtitle anchored above the composer, with `scene-glow-brand` rising from the composer's top edge.
- The chat keeps the drawer and the 640 and 768 breakpoints it inherits from LibreChat. They stay out of the system for now (owner, 2026-11-04; NDS-49): the layout classes and "no drawer" above still bind every other web product.

[nearai/LibreChat PR #5]

## Navigation by class

One navigation model, rendered per class (NDS-13). The rail and the bottom bar hold the same destinations in the same order.

| Class | Primary navigation | Overflow and secondary |
|---|---|---|
| Compact | `TabBar` at the bottom: 3 to 5 destinations, 64 tall, icon over label, glass bar | More than five: a menu button in the top `Toolbar` opens a modal expanded `NavigationRail` over `scrim`. Settings sits in the account menu |
| Medium | Collapsed `NavigationRail`, `size-rail-collapsed` 96, leading edge | The rail's menu button opens the expanded rail as a modal over `scrim` |
| Expanded | Collapsed rail; the expanded rail (standard, pushing content) when the person opens it | Same |
| Large and up | Expanded rail, `size-rail-expanded` 220 (up to 360), or a `Sidebar` at `size-sidebar` 280 | Sections inside a destination use `Tabs` or a `SegmentedControl` in the pane |

- Never build a navigation drawer; the expanded rail replaces it.
- Label every destination at every class. The collapsed rail shows icon over label; the expanded rail shows icon beside label, and its whole width is the target.
- Selecting the current destination again scrolls its pane to the top.
- Keep the bottom bar visible while content scrolls. Native apps hide it on scroll only when no screen reader runs, and the web cannot tell, so it stays.
- Put the title and the screen's actions in a `Toolbar` at the top of the content pane, with at most three groups and one primary action at the trailing end (NDS-19).
- Use a `Breadcrumb` for sub-pages inside a destination at medium and up (Home > History). At compact the breadcrumb collapses to a back button naming the parent ("Home").

**Gateway worked example.** The Gateway monitor keeps its navigation inside the main pane: `Tabs` with the ember rule for Home / Private AI / Traces / Insights at medium and up (NDS-37), with the decisions-owed count on Traces. At compact the same four become a `TabBar`, and the count moves onto the Traces tab. History is a sub-page of Traces and Missions a sub-page of Home, each a `Breadcrumb` in the pane. Before onboarding only Private AI shows, at every class.

[M3: navigation rail] [trace-commons: MonitorWindowView.swift]

## Canonical layouts

Use the three M3 canonical layouts before inventing one. Each states its panes per class and what happens on resize.

**List-detail.** A list of items and the selected item's detail. Examples: Traces (folders and traces, then the trace's review card); agent runs (runs, then the `AgentRun` with its `ToolCall`s); chats (threads, then the thread).

| Class | Shows | Back | Selection |
|---|---|---|---|
| Compact, medium | List or detail | Detail shows a back button and browser Back returns to the list | Not drawn |
| Expanded and up | List (`size-pane-main` 440, never under 360) and detail side by side | No back button | The selected `ListRow` uses `selection` with `text-on-accent` |

- Opening a wide window with nothing selected shows an `EmptyState` in the detail pane, written by the product ("Select a trace to review it.").
- Narrowing a window with a selection shows the detail. Widening it shows both, with the selection kept.
- Keep each pane's scroll position and the read state across these changes.

**Supporting pane.** Primary content takes about two thirds; a supporting pane holds related material. Examples: a chat thread with its sources and tool calls; the Private AI ledger with its account section; the "Look inside" review with its sizes card.

| Class | Supporting pane |
|---|---|
| Compact | Below the primary content, or a `Sheet` at the medium detent |
| Medium | A modal side sheet over `scrim` (at most 400 wide) |
| Expanded and up | A fixed pane beside the primary content: `size-pane-inspector` 293 for inspection, up to 360 for reading |

**Feed.** A grid of cards. Examples: Home's `StatCard`s (Waiting, Contributed, Credit) and icon cards (Missions, Private AI Settings); a mission or model catalogue. One column at compact; add columns from medium as the container widens; keep every card's text inside `size-readable-width`. A whole-card link has the role of a link and one target.

**The three-pane window on the web.** Gateway's floating three-pane window (main 440, flexible content, inspector 293) translates by class. The browser window cannot grow to the right the way the Mac window does, so a pane that no longer fits swaps places with another.

| Class | Main pane | Content (map) | Inspector |
|---|---|---|---|
| Compact | Each tab is a page | Its own page, opened from a toolbar button | The detail page in list-detail; a `Sheet` for summary-only views |
| Medium | Full width | Replaces the main pane while open | Modal side sheet |
| Expanded | 440 | Swaps with the inspector: the one opened last shows | 293 |
| Large and up | 440 | Flexible, at least `size-pane-content-min` 360 | 293 |

The toolbar toggles for the map and the inspector stay at every class. A toggle whose pane is swapped out reads as off (`toolbar-glyph-off`). Inspector demand still applies: events that open the inspector (undo, contributed, kept) open it, and nothing closes it on its own.

[M3: canonical layouts] [trace-commons: ThreePane.swift]

## Pages and panes

A page is a destination with its own URL and title. A pane is a region of the window that holds a page beside others. At compact every pane is a page; at expanded and up, related pages sit side by side as panes.

- Fix the shell to `100dvh` from medium up and let each pane scroll itself (`overflow: auto`, `overscroll-behavior: contain`). At compact let the document scroll, so the mobile browser's bars collapse and its pull-to-refresh behaves as people expect.
- Give the shell landmarks: `nav` for the rail or bar, `main` for the primary pane, `aside` for the inspector, and a skip link to `main`. Focus order follows the visual order, leading to trailing.
- Title the document `Page · Product` ("Traces · Near.ai"). Keep the product name out of in-page headings.
- Panes never stack scroll views on the same axis. A transcript inside a review page scrolls with the page.

## URL and history

Every place a person can land on has a URL, and Back always takes them somewhere sensible.

| State | Where it lives | Example |
|---|---|---|
| Destination and selected item | Path | `/traces/near-agents/2026-10-12T0914` |
| Sub-page | Path | `/traces/history` |
| View of the item a shared link should keep | Query | `?tab=transcript`, `?q=api_key` |
| Pane visibility, pane widths, collapsed sections | Per-device storage, read with try/catch | Inspector open, map hidden |
| Drafts | Per-device storage, autosaved | An unsent prompt in `PromptComposer` |
| Anything sensitive | Nowhere in the URL | Prompt text, tokens, email addresses |

- Push a history entry when the destination, the sub-page or (in a single-pane layout) the open item changes.
- Replace the entry when selection changes inside a two-pane layout, so Back leaves the section instead of stepping through every row a person clicked.
- At compact, a `Sheet` or full-screen task pushes one entry, so browser Back closes it. Dialogs at medium and up do not push; Esc closes them.
- A deep link opens exactly that item at any class. The in-app back button goes up to the parent list even when browser history is empty.
- Restore scroll position on Back. Never intercept Back with a confirmation; autosave drafts instead.
- Changing the URL never changes data. Actions (Submit, Dismiss) are buttons, never links.

## Dialogs, sheets and popovers

Choose the presentation by need, then by class. Never stack modals; queue approvals and show them one at a time.

| Need | Compact | Medium | Expanded and up |
|---|---|---|---|
| Confirm an irreversible or consent action (NDS-15) | `Modal`, full width minus 32 | `Modal` at `size-modal-narrow` 450 | `Modal` 450, or `size-modal-width` 780 when it carries a `ConsentBlock` |
| A scoped task (rename, add an account, submit as) | `Sheet` at the large detent, or a full-screen task | `Modal` | `Modal` |
| Supplementary detail | Detail page or `Sheet` | Modal side sheet | Inspector pane |
| Small anchored information (an info button) | `Sheet` at the medium detent | `Popover` at `size-popover-width` 260 | `Popover` |
| Choices for an action just started | `Menu`, or a `Sheet` for more than about seven items | `Menu` | `Menu` |
| Read-only review ("Look inside") | Full-screen task with Close | `Modal` 780 | `Modal` 780 |

**Modal.** Use the `<dialog>` element with `showModal()`, which makes the page behind it inert. Focus moves to the first field or the safest action, Tab wraps inside, Esc closes any modal that is not mid-commit, and focus returns to the control that opened it. Keep `modal-inset` 28 to the viewport edges. Cancel sits leading and the primary trailing (NDS-19), with at most one primary. Destructive is never the default. An irreversible send (Submit in the review) is drawn prominent but never answers Return, and a consent confirmation can stay disabled until its `Checkbox` is ticked. A click on the scrim never closes a modal.

**Sheet at compact.** A bottom sheet with `radius-sheet` 28 top corners, a 32 by 4 drag handle centered in a 48 band, and medium and large detents. Dragging down or tapping the handle changes detent; a visible Close or Cancel button is always present, because dragging is never the only way. Confirm before a swipe discards unsent text.

**Popover and menu.** Use the Popover API for top-layer rendering and light dismiss. Light dismiss (a click outside, Esc) is for popovers and menus only. Menus use roving focus, arrow keys, Home and End, and typeahead. Menu items show their shortcut, written per platform.

[HIG: sheets] [M3: dialogs]

## Command palette

The web, Windows and Linux have no menu bar, so the `CommandPalette` is where the whole command registry lives (NDS-14). It renders the same commands the Mac menu bar lists, with the same labels and enabled states.

- Open it with `Mod+K` and with a visible search button in the top `Toolbar`. At compact it opens as a full-screen sheet with the field at the top; elsewhere it floats near the top of the window at `size-modal-narrow` 450, on the floating layer.
- Group results: recent items, then destinations (Home, Traces, Private AI, each settings section), then commands. List only commands that can run now. An irreversible send such as Submit may be listed; choosing it opens the review where the action lives.
- When the product has an assistant, add one explicit row, "Ask Near AI", that turns the typed text into a prompt. The palette never sends a prompt unless that row is chosen.
- Write shortcuts as the platform shows them: ⌘K in a browser on a Mac, Ctrl+K elsewhere. Never bind keys the browser keeps (`Mod+T`, `Mod+W`, `Mod+N`, `Mod+L`, `Mod+R`, `Mod+Q`, Ctrl+Tab) or `Mod+Space`.
- `Mod+,` opens the settings page. Esc stops a running generation when focus is in the composer or the transcript, after first closing the topmost floating surface if one is open.
- List every shortcut in a keyboard shortcuts dialog reachable from the palette. Navigation and commands holds the registry and the full shortcut table.

[HIG: the menu bar] [trace-commons: TraceCommonsAppMain.swift]

## Forms on the web

Forms and data holds the full field rules. On the web:

- Put the label above the field (`web-label`), helper text below (`web-caption`, `text-tertiary`), and an `InlineAlert` under the field it refers to, linked with `aria-describedby`.
- Mark the smaller group in words: "(optional)" after optional labels, or "required" as inline text after the label, in `positive-text` on consent rows (NDS-42). An asterisk alone is not enough. Set `aria-required` on required fields.
- Validate a field once it has been touched, never during a first attempt or on page load. Keep submit enabled and report problems inline; with two or more errors, or one out of view, add a `Notice` at the top that links to each field. An empty `PromptComposer` is the exception: its Send stays disabled.
- Set `autocomplete`, `inputmode` and `enterkeyhint` on every field (`enterkeyhint="send"` on the composer, `"search"` on a `SearchField`). Use native date and time inputs where the browser's picker is adequate.
- A `Switch` applies at once and offers Undo where the change is reversible; a `Checkbox` group applies on Save.
- Settings is a page (NDS-21), never a modal over the app. From expanded up it has a section list at `size-modal-nav` 180 and one scrolling body, each section introduced by a rule; at compact the list and each section are separate pages. Appearance lives in Settings > General as a `SegmentedControl`: Light / Dark / System.

## Theming

The page carries one of the six themes in `data-theme` on `<html>`. Resolve it in the order Architecture and theming gives: product, then appearance, then contrast.

| Signal | Result |
|---|---|
| In-app choice (Light / Dark / System) | Overrides the system appearance on this device; applies at once in every open tab |
| `prefers-color-scheme` | Light or dark when the choice is System (NDS-17) |
| `prefers-contrast: more` | The `-hc` theme of the current appearance. Gateway has no `-hc` pair, so it uses `light-hc` or `dark-hc`, accent included |
| `prefers-reduced-transparency: reduce` | Panes and floating surfaces become `pane-opaque`; blur is removed. Offer the same switch in settings, because support for the query varies by browser |
| `forced-colors: active` | Surfaces become `Canvas` with a 1px `CanvasText` border; state is carried by borders and outlines, never by fills. Only `Logo` and chart swatches opt out with `forced-color-adjust: none` |
| `prefers-reduced-motion: reduce` | Nothing moves. Changes jump to their end state and view transitions are off (NDS-11) |

- Set `data-theme` and `color-scheme` from a small blocking script in `<head>` before first paint, so the page never flashes the wrong appearance. Listen for `matchMedia` changes and re-resolve.
- Keep the focus ring on: 2px `focus-ring`, 2px outside, keyboard focus only (NDS-5). A product may turn it off with `.nr-focus-off`, as Gateway does; turning it off fails WCAG 2.4.7 (Focus Visible), and it hurts most on the web, where keyboard users have no system ring to fall back on.

## Performance budgets

| Budget | Value |
|---|---|
| Glass surfaces per viewport | About 4, at most 1 large (the pane group counts as one) |
| `backdrop-filter` on scrolling items (cards, rows, messages) | Never |
| Animated properties | Opacity and transform only; never the blur radius |
| Compositor cost of glass | Under 2 ms a frame on mid-range hardware |
| Opaque fallback trigger | 4 or fewer cores, Save-Data, `prefers-reduced-data`, or sustained dropped frames |
| Refraction (SVG displacement lensing) | Not used. Flat glass has none, and Firefox draws nothing for it |
| Largest contentful paint, interaction to next paint, layout shift | 2.5 s, 200 ms, 0.1 at the 75th percentile |
| Rendered rows before virtualizing a list | About 100 (Gateway's History caps at 100 rows) |

## Loading and streaming

- Render the shell (scene, rail, pane frames, toolbar) at once. A blank page reads as broken.
- Inside a pane, show the product's loading line ("Reading local queue..."), with a `Spinner` beside it after 200 ms. Use a `Skeleton` only for the first load of rows or cards whose layout is known, never on a refetch. Use a determinate `ProgressBar` when the size of the work is known.
- A reload never replaces held data. A failed read keeps the last value and adds an `InlineAlert` or a section `Notice` with Retry; a value past its freshness window shows a dash, never zero.
- Stream answers into the `Message` as they arrive. Announce the start and the end through a polite live region, never each token.
- Follow the stream only while the reader is at the bottom of the transcript. Once they scroll up, show a "Jump to latest" control instead of pulling them back.
- Streaming never moves focus. The `PromptComposer` stays usable during generation, its Send becomes Stop, and Esc stops.
- While a run continues in a background tab, the document title carries its state ("Running · Traces · Near.ai"). Web Push notifies only when the person granted it.
- Reopen a closed event stream after 5 s and keep showing what was held. Tell people only when the gap matters ("Showing values from 14:02.").
- When the browser goes offline, keep the page, add a status `Notice`, and keep drafts. Sending waits for the connection and says so.

See AI and agent patterns and Feedback and states.

## Sign-in

- Let people look around before signing in where the product allows it. Ask for an account at the first action that needs one (defer commitment).
- Offer a passkey first: WebAuthn with conditional mediation, so the field with `autocomplete="username webauthn"` offers saved passkeys. Name the method the device offers ("Use a passkey", "Windows Hello").
- The account is the Near AI account. Gateway's Join step, the last step of first run (NDS-32), shows one Near AI account card whose action turns into a spinner and then a "Signed in" `StatusLabel`; its passkey card was removed on 2026-10-31. The action note above the `ActionBar` states the consequence: "Connecting or creating an account doesn't authorize any data sharing." Gateway requires the account to finish setup, so Join has no Skip.
- When sign-in continues in another browser tab or window, keep Cancel visible while it waits and show a `Spinner` in the primary action.
- Settings > Account offers sign-out and account deletion, with the same effort to delete as to sign up. Deletion says what it removes (chats, memory, files) and when it is complete.

## Cookie and consent banners

- Show a banner only when the surface sets storage that is not essential. App surfaces that keep only essential storage show none.
- Place it at the bottom of the viewport on the floating layer, above the `TabBar` and the `PromptComposer`, never over them. It never blocks reading or scrolling.
- Give accept and reject equal weight: two neutral `Button`s ("Allow all", "Reject optional"), plus "Choose" for categories. Neither is the primary and neither answers Return.
- In "Choose", each category is a `Switch`, off by default. Essential storage is shown on and locked, tagged "required". Each category states its consequence ("Analytics cookies record which pages you open.").
- Remember the choice, never ask again on the next visit, and keep a "Cookie settings" link in the footer and in Settings.

## Marketing pages

Marketing pages sell a product to someone who does not have it yet. They follow their own register, set by the owner on the Near AI Gateway site (nearai-gateway-website, 2026-10-27 to 10-30, NDS-45): Near AI blue on a near-black void, live pixel art, and the Near AI brand faces. App surfaces keep everything above this section.

| | Marketing pages | App surfaces |
|---|---|---|
| Ground | Void #070708, dark only | `scene` and panes, following the system appearance (NDS-17) |
| Type | Brand faces: Schibsted Grotesk, Mona Sans, JetBrains Mono (NDS-45) | `system-ui` and `web-*` steps only (NDS-4) |
| Accent | Near AI blue #0091FD with void ink | `accent` with `text-on-accent` |
| Material | Glass on the header bar only; content on painted surfaces with a 1px rule | Flat glass shell |
| Motion | Live art at 24 fps, paused when unseen | Standard springs and `ease-standard` |
| Marks | The Near AI wordmark with the product name typeset beside it (NDS-27) | Product mark in the app tile, rail or masthead |

### Palette

| Role | Value | Use |
|---|---|---|
| Void | #070708 | Page ground, CTA ground, art grounds |
| Obsidian | #0F0F11 | Plates and notes |
| Basalt | #18181B | Panels |
| Slate | #26262B | 1px rules and card edges, the lockup divider |
| Silver | #C1C1C1 | Body text, nav links |
| Marble | #FAFAF7 | Headings, the current nav item, the brightest art step |
| Pewter | #808088 | Meta and the few remaining labels (5.1:1 on void) |
| Near AI blue | #0091FD (`brand-blue`) | Primary fill, link underlines, bullets, signals. Void ink on it is 6.2:1; white on it is only 3.3:1, so never white |
| Art ramp | #035CA3, #0091FD, `brand-sky` #83DCFF, #FAFAF7 | The four lit steps of every illustration |

The neutrals come from the owner's Cyber-Classical pattern library (its "classical" register), with Near AI blue as the one pigment. There is no light marketing theme: the owner removed every light section. A marketing page still sets `color-scheme: dark` and honors `prefers-reduced-motion`.

### Type

| Role | Face | Size / weight / line |
|---|---|---|
| Hero title | Schibsted Grotesk | 40 to 68 (`clamp(2.5rem, 4.8vw, 4.25rem)`), 600, 1.04, −0.035em; a second line in 500 and silver |
| Page title, section head | Schibsted Grotesk | 56 and 52, 600 |
| Subhead | Schibsted Grotesk | 34, 600; card titles 22, 500 |
| Lede | Mona Sans | 21, line 1.45 to 1.5, at most 62ch |
| Body | Mona Sans | 16, line 1.55 |
| Button | Mona Sans | 15, 600, sentence case |
| Nav link, label, code | JetBrains Mono | 12, 500, uppercase with 0.1em tracking for nav; code and terminal text 12.5 to 13.5 |

Below 768 the titles step down to `clamp(2.1rem, 9vw, 2.75rem)` and ledes to 18. Faces load from the font host with system fallbacks; SF is never served (NDS-4).

### Header

- A floating glass bar, sticky 12 from the top, 56 tall, radius 36 (squircle; 20 where `corner-shape` is unsupported). Glass is `rgba(255,255,255,.04)` over a navy veil (`rgba(7,10,26,.7)`), `blur(22px) saturate(1.2)` and a soft drop. No edge or top highlight: the owner removed it.
- The lockup leads: the Near AI wordmark (17 tall), a 1px slate divider, then the product name typeset in Schibsted Grotesk 21 / 600 at −0.04em ("Gateway"), as tall as the wordmark's "AI". The product name hides below 340.
- Links trail in JetBrains Mono. The current page is marble with a 2px Near AI blue underline 8 below the label. The app's ember glow was tried on the site nav and reverted.
- No Download button in the bar. Below 900 a Menu button opens the same glass as a panel 8 below the bar, with a full-width "Download for macOS".

### Page heads and header art

- Every head starts on the same line: `--head-top: clamp(56px, 9vw, 132px)`. Inner heads end `--head-gap: clamp(112px, 15vw, 216px)` above their first section, and the art may run behind that section. No rule under a head.
- Header art is full bleed behind the copy, reaching up under the bar, running off the top and trailing edges and fading toward the copy with a radial mask. On phones it sits behind the copy at 55% opacity, never above it.
- Text over moving art gets a stacked black text shadow (`0 0 2px #000` out to `0 0 56px rgb(0 0 0 / .85)`), which the owner asked for. Keep art away from body paragraphs.

### Sections and grid

- Content width `min(100% − 2 × gutter, 1234px)`; gutters 16, 24 from 768, 32 from 1280.
- Sections are `clamp(72px, 10vw, 128px)` apart, tight ones `clamp(48px, 7vw, 88px)`, with a hairline between consecutive sections and none under a hero or page head.
- No eyebrows above headlines, no section numbers and no § marks: the owner removed all of them. Numbered steps use numerals in squircle tiles (JetBrains Mono, tabular), which roll once into view.

### Buttons

- **Primary.** Flat Near AI blue, void ink, no border, about 50 tall (padding 13 × 20), radius 18 squircle (10 fallback), with a soft blue glow below (`0 14px 30px -12px` at 65%), which the owner kept because it echoes the app's tab ember. Hover mixes 12% white into the fill and lifts the glow.
- **Secondary.** Transparent with a 1px marble outline; hover fills marble with void text.
- **Link.** No container, 16 text with a 1px underline 4 below.
- An `<a>` styled as a button carries its own ink; it never inherits the body's link color.
- No arrows, gradients, glass, frost, halftone fills or edge highlights on buttons. Each was tried and the owner reverted to "something minimal".

### Art direction

- Every illustration is drawn live (canvas or WebGL) as light, then quantized to a pixel grid (3 for header art, 2 for section art and on phones) through an ordered Bayer dither into the art ramp, after a contrast curve. Pixels render crisp (`image-rendering: pixelated`).
- Art runs at 24 frames a second, pauses offscreen and in a hidden tab, and shows one still frame under reduced motion. Without WebGL it falls back to a 2D drawing.
- A group of cards shares one canvas clipped to each card's outline, so one field reads across them, never one effect per card.
- Frames, captions, placards and magnifier lenses around art were all removed.

### Components

| Component | Anatomy |
|---|---|
| Terminal window | macOS-style title bar (#2c2c2e, three grey 11px lights, centered title), body #1e1e1f with #e4e4e6 text, radius 22 (12 fallback). Copy is a 28 icon in the title bar with a status word ("Copied") that clears after 2.4 s |
| Release card | A terminal window titled with the file name: product, version in mono, size and date, the primary download and links (Release notes, SHA-256) |
| Steps | A numeral column (44 or 32 numerals in Near AI blue) beside a title and body, hairlines between |
| Callout | Near AI blue at 6% over void, a 10px blue square mark, `radius-card`-like 28, no border |
| Plates | Three cards in a row (one column below 1024): a 5:4 figure on void over a body with a numeral, title and line |
| Stations | Three stops joined by a dotted line; the middle stop (the person) filled blue |
| Ledger | Mono rows with a dotted leader to the value or a tag |
| CTA panel | Void, 1px rule, radius 36, centered: title, primary and link, mono meta |
| Footer | Four columns (two below 900): the lockup and one line, then link columns with mono headings; a base row with the copyright |
| Share card | 1200 × 630: the hero's still frame under its mask, the lockup, the title and one line |
| Product tour | A replay of the app at 1:1 (its own tokens, sizes and words) inside a desktop frame, with chapter chips, a caption card in the lower trailing corner and play / pause. It autoplays only in view and in a foreground tab, and shows end states under reduced motion |

### Writing

Marketing copy follows the same voice: say what happens to data, name the action on each button, sentence case, no exclamation marks. Headings say the point first ("You decide what leaves your Mac."). Facts (versions, sizes, requirements) come from the release feed, never typed by hand.

### Open conflicts

These shipped on the Gateway site and contradict the rules elsewhere in this system. They are recorded, not adopted:

- "Private by default, always" promises privacy (see Writing and content). The app's one permitted sentence, "Add a privacy layer to AI models you are already using.", is the model.
- "Paid with your Near AI credit." puts "credit" on a Private AI section, where it is restricted.
- The site writes the folder modes "Ask each time, Automatic or Never"; the app says Ask / Automatic / Never (NDS-30).
- Tool logos are recolored into the dithered art, against the third-party logo rule (Iconography).
- Art moves behind headlines and ledes without pause, against "Nothing fidgets" (Motion).
- "Gateway" as a product name collides with the proof state "Gateway only" (AI and agent patterns).

[nearai-gateway-website: assets/css/site.css, assets/js/site.js]

## Windows and Linux shells

The Windows and Linux desktop apps are this web app in a Tauri shell. Desktop patterns holds the full shell table (material, frame, commands, ambient surfaces); the rules that change the web patterns above are these.

- **Material.** On Windows 11 the system draws Mica behind the window and the panes paint `glass-veil` and `pane-fill` over it, so the pane group needs no `backdrop-filter` of its own; without Mica, the in-page `.nr-scene` and `blur-pane` apply. Linux panes stay `pane-base`, with blur only where the compositor provides it and the frame budget holds.
- **Panes.** People resize the window freely, so panes reflow by class exactly as in the three-pane table above. On first launch, the window shows the inspector when the screen is at least `bp-inspector` (900) wide and the content pane when it is at least `bp-map` (1100).
- **Frame.** Keep the system title bar and caption buttons, or extend content into the title bar with the system buttons kept, and mark the top row's empty space as a drag region. Draw `radius-window` 22 only on a window the app draws itself, such as the tray panel.
- **Focus.** Paint `inactive-dim` over the panes when the window loses focus. Only the focused window answers shortcuts.
- **Commands.** `Mod` is Ctrl. An app menu button at the leading end of the top row and the `CommandPalette` carry every command. Settings opens in its own window with Ctrl+, (NDS-21).
- **Density and type.** Regular density with pointer targets (`target-pointer` 28). The `--font-web` stack resolves to Segoe UI Variable on Windows and the desktop's sans on Linux.
- **Button order.** Cancel leading, primary trailing (NDS-19), although native Windows dialogs put the primary first.
- **System surfaces.** The notification-area flyout (Windows) or tray (Linux) holds the glance panel at `size-panel-width` 380. A running agent shows progress on the taskbar or tray; results arrive as system notifications.
- **Contrast.** Windows contrast themes arrive as `forced-colors: active`. Test every screen with one on.

[Liquid Glass: Windows and Linux] [trace-commons: tauri.conf.json]
