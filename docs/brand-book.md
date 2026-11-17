The Near AI OS Design System is the parent system for every Near AI product on desktop, web, tablet and phone. It carries the look of the Gateway macOS app (flat glass: frosted panes over the desktop, flat painted fills inside them, one accent for the one action) into a shared set of tokens, components and pattern libraries, and lets each product bring its own accent. Read this page first, then the section for the surface you are building.

## How the system is put together

Three layers, each overriding the one above it only where it must:

1. **The parent** (this system): color roles, type steps, spacing, radii, materials, motion, components and patterns. Its default accent is Near AI blue.
2. **Product themes**: a product replaces the accent family and its data colors, nothing else. Gateway is the first product theme (`gateway-light`, `gateway-dark`); since 2026-10-19 it uses the parent's Near AI blue and differs only in two fills (NDS-22).
3. **Platforms**: one set of tokens, rendered with each platform's own idioms. macOS leads; iOS and iPadOS use their native navigation and system glass; Android uses Material 3 Expressive components in Near AI tokens; web uses Material's adaptive layouts with a light CSS glass on navigation only.

Themes in `tokens.json`: `light`, `dark` (the parent), `light-hc`, `dark-hc` (increased contrast, 7:1 text), `gateway-light`, `gateway-dark` (the Gateway product). Follow the system appearance by default; an in-app Light / Dark / System choice is allowed under Settings > General > Appearance. Select the `-hc` theme whenever the person turns on Increase Contrast or `prefers-contrast: more`.

## Principles

- **Proof, not promises.** Show what happened and what will happen to someone's data: sizes, destinations, proofs. Never promise privacy or security in copy. A model call is "verified" only when its attestation checks out; otherwise say "pending" or "no proof".
- **The person decides.** Nothing leaves the device unless the person says so. The safe action is the default: Return never answers an irreversible send, destructive actions are never the default, and reversible actions act at once with Undo.
- **One action per surface.** `accent` marks the one primary action and the current selection. Everything else is neutral glass (`control`) or a link. Brand color lives in content and marks, not on every control.
- **Glass for navigation, paint for content.** Panes, bars, sidebars, menus and popovers are glass. Cards, rows, fields and charts inside them are painted fills. Never put glass on glass.
- **Status is a dot plus words.** Color never carries meaning alone. An unknown value is a dash or the product's "unknown" word, never zero and never "on".
- **Native where it exists.** Use the platform's tab bar, sidebar, menus, sheets and pickers; restyle with tokens rather than rebuilding them.
- **Dense on a desk, roomy under a finger.** Pick the density for the input, not the screen size. Touch targets never shrink below 44pt (Apple), 48dp (Android, touch web) or 60pt (visionOS).
- **Calm motion.** One curve for fades and fills, standard springs for movement, an expressive spring for at most one or two hero moments. The N may draw itself at a welcome and think beside a reply (NDS-26); nothing shimmers on a card, a celebration marks only a real arrival, and nothing ambient runs while the window can't be seen (NDS-40). Nothing moves under Reduce Motion.

## Using the tokens

**Surfaces.** Put content on a pane: `glass-veil` with `pane-fill` over the native material or `blur-pane`. Where there is no material (Android below 12, Windows, Linux, a modal backing) use `pane-base`; under forced colors, and under Reduce Transparency wherever the product paints its own glass, use `pane-opaque`. On Apple platforms Reduce Transparency is the system's to apply to the native material (NDS-23). Inside a pane use `card` for grouped content, `card-quiet` for inspector sections and notices, `well` for recessed tracks, `field` for inputs, `control` for neutral buttons and pickers. Floating surfaces use `popover` and `menu` (94%, so nothing under them shows through) over `blur-floating` with `shadow-float`. A control on a menu or a selected row takes `control-on-menu` or `control-on-selection`; a card inside a card takes `card-nested` (NDS-38). Content drawn straight on the scene (a first-run stage, a chat's welcome) uses `scene-card`, `scene-control`, `scene-rule` and the one `scene-glow-brand`. Modals sit on `pane-base` over `scrim-modal` and `blur-scrim` with `shadow-modal`. On phones and tablets the screen is an opaque pane (`pane-base`); only bars and floating toolbars are glass. Wherever the ground is opaque (phone screens, Reduce Transparency, opaque content panes), cards take `card-on-opaque` and `card-quiet-on-opaque`.

**Text.** Set every word in `text-primary`, `text-secondary` or `text-tertiary`; prompts in `text-placeholder` on glass and `text-placeholder-on-opaque` on opaque grounds; links and accent eyebrows in `accent-text`. Each holds 4.5:1 on every pane, card, field, popover and menu over the worst desktop the glass can show (a white desktop under dark glass, #333333 under light glass). Text on `accent` is `text-on-accent`; the count on `badge-fill` is `text-on-status`. Status words use `positive-text`, `caution-text`, `critical-text`; destructive labels use `destructive-text`. `neutral` is a mark color and never text.

**Accent.** `accent` fills the primary button, the selected segment, row and tab, the on switch, checkbox and radio. It holds 3:1 against every ground, so a selected state is visible on its own. Pressed is `accent-pressed` (8% darker, never a fade). `accent-soft` draws accent marks that are not text (step nodes, the tab ember, a single data series); `accent-tint` is the ground behind accent content.

**Status.** Pair a `positive`, `caution`, `critical` or `neutral` dot with words in `StatusLabel`. Tags use the `-tint` ground with the `-text` ink. The only badge is `badge-fill` with `text-on-status`, and it counts decisions owed, nothing else. A passed proof is `proof-text` on `proof-tint`, calmer than the success greens (NDS-43).

**Charts.** Plot on `surface-chart`, never straight on glass. Use `data-1` to `data-8` in order and never cycle them. Gridlines are `chart-grid`; labels are text tokens, never the series color. Every chart has words: a legend for two or more series and a table view.

**Type.** Each platform tier is a set of type classes over one step scale: `micro`, `eyebrow`, `caption`, `label`, `body`, `body-strong`, `title`, `heading`, `display`, `number`, `mono`. Use `mac-*` on macOS and in dense desktop tools (SF Pro text styles at macOS sizes, body 13), `web-*` on the web and the Windows and Linux shells (body 14), `ios-*` on iPhone and iPad (Dynamic Type, body 17), `android-*` on Android (M3 roles, body 16). `hero-display` and `hero-figure` are for one or two hero moments, never inside tools. Faces are the platform's own: SF Pro and SF Mono on Apple, Roboto Flex on Android, Segoe UI Variable on Windows, `system-ui` on the web. Never ship SF as a web font. Set figures that describe what leaves the device in `mono`.

**Spacing and radius.** Space with the 2-step scale (`space-2` to `space-16`, then `space-20`, `space-24`) inside components and the 8-grid steps (`space-24` to `space-64`) between page sections. Panes sit `pane-gap` apart with `pane-padding` inside; cards use `card-padding-y` and `card-padding-x`, `card-gap` between them. Corners: `radius-pane` 20, `radius-card` 16, `radius-card-quiet` 14, `radius-control` 11, `radius-tile` 6; buttons, segments, wells, chips and switches are capsules (`radius-pill`). Nested corners are concentric: the inner radius is the outer radius minus the padding between them, never below `radius-tile`.

**Density.** Size controls from the density, not the platform. `.nr-compact` (desktop): inline controls `size-control-large` 28, action-bar buttons `size-cta` 34, modal action buttons `size-cta-small` 30, rows `size-list-row` 40. `.nr-regular` (web) uses the same heights with web type. `.nr-touch`: controls `size-control-touch` 44 on iOS, 40 visible inside a 48 target on Android. `.nr-dense` (pro panels): 20px rows and controls, 2px between fields.

**Motion.** Fades, fills, hover and press: `duration-fast` with `ease-standard`. Panes, menus and modals: `duration-standard`. Anything that moves uses a spring: `spring-spatial-fast` for small controls, `spring-spatial` for panes and sheets, `spring-spatial-slow` for full-screen changes, `spring-effects` for color and blur. `spring-expressive` is for one or two hero moments per product. Brand moments have their own curves: the N's marker draw (1s), a welcome's rise (1.6s) and glow (2s), the proof stamp (420ms); Motion lists them. Under Reduce Motion, jump to the end state.

**Focus.** Keyboard focus draws a 2px `focus-ring` outline 2px outside the control. It is on by default. A product may turn it off on its root (`.nr-focus-off`); doing so fails WCAG 2.4.7, and Gateway currently does.

## Content fundamentals

Write directly, from the person's side of the screen, about what happens to their data. "Nothing is sent unless you say so." Concede limits before they surprise anyone: "Nothing matched a pattern. That is not the same as nothing being there." Never name the mechanism; state the consequence ("your queue is safe", not "the ingest claim succeeded").

- Buttons name the action, a verb or a verb and an object, one or two words: **Submit**, **Look inside**, **Turn on**, **Send**, **Refresh**, **Create task**. Never a bare "OK".
- Titles and buttons have separate jobs: the title "Turn on Automatic for near-agents?" over the button **Turn on**.
- Put consequences beside the action, not in a tooltip: "{size} remaining" by **Load more**; the destination and scope by **Send**.
- Navigation names things ("Data uses", "Change log"); choices name values ("1 hour", "Until morning", "Until resumed").
- Sentence case everywhere. No exclamation marks, no emoji, no apologies in errors. Errors say what went wrong and what to do.
- State copy is a full sentence with a period: "Nothing is waiting." "The watcher isn't running."
- Counts inflect in the copy source, never in the UI ("1 trace", "2 traces"). Unknown is "—" or "Unknown", never "0".
- Say "trace" for the person's recorded work, never "session" (NDS-29). Folder modes are **Ask**, **Automatic** and **Never** (NDS-30).
- Explanations can move behind an "i"; status, failures, prerequisites and anything irreversible stay on the page.
- Components never author words, including accessibility labels. Each product keeps one copy source (Gateway: the Rust core) and every shell reads it.

## Visual foundations

- **Color.** Cool neutrals: navy-black in dark (`scene` #070a1a, `pane-opaque` #0d1124) and a cool grey in light (`glass-veil` #e3e6ec at 66%). One accent per product. Status hues stay fixed across products.
- **Materials.** Flat glass: frosted, lightly veiled, no rims, no specular highlights. Floating surfaces cast one soft `shadow-float`. The Classic treatment (gradient sheens, specular top highlight and bottom shade, a glow on the primary button: `edge-classic-*`) is an optional expressive treatment.
- **Shape.** Capsule controls, continuous (squircle) corners on Apple, concentric nesting everywhere.
- **Elevation.** Expressed by layer, not by stacked shadows: scene, pane, painted content, floating, modal. Only floating things and modals cast shadows.
- **Lines.** A hairline (`hairline`, one device pixel) separates rows inside a list; `rule` sits under a modal header, over its footer and under a tab row. Containers never get a hairline border, except the 1px `edge-hc` every painted surface gets in the `-hc` themes.
- **States.** Hover replaces the fill (`control-hover`, `card-hover`, `row-hover`); pressed darkens 8%; selected is `accent` with `text-on-accent`; disabled is `opacity-disabled` 0.45 on the whole control with no hover and a reason nearby; invalid is a 1pt `critical` ring with words beside it.
- **Layout.** Classify by the window or container width: compact under 600, medium to 839, expanded to 1199, large to 1599, extra-large beyond. Desktop windows float panes 10pt apart: a main pane (440pt to start) and a content pane (minimum 360) that share a divider, and a 293pt inspector. A pane opening near the screen edge slides the window left just enough (NDS-35).
- **Marketing.** Marketing pages are dark-only, Near AI blue on a void ground, set in the brand faces, with live dithered pixel art, squircle corners and flat blue buttons with a soft glow (NDS-45). App surfaces never borrow any of it.

## Iconography

SF Symbols on Apple platforms, Material Symbols (rounded, weight matched to text) on Android and the web. One registry maps each semantic name to both. Glyphs are 16px in desktop controls, 13pt in the macOS toolbar, 20px in touch toolbars. Icon-only controls always carry a label that becomes the tooltip and the accessible name. Refresh is a labelled pill, the word before the glyph (NDS-36). The macOS menu-bar item is the N plus a small bar graph in the menu bar's ink (NDS-33); tray icons elsewhere stay single-ink. The Gateway glyphs from the original web shell (`viewMenu`, `graph`, `map`, `inspector`, `gear`, `chevronDown`, `folder`, `kebab`) and its warning triangle remain available to Gateway. Third-party tool logos (Claude, Codex, OpenCode and others) appear only inside 22pt tool tiles in their own tints, after a trademark check. Never use emoji as icons. Details in Iconography.

## Brand

The master brand is Near AI: the "near AI" wordmark, the "N" monogram lockup and the tile, from the Near AI logo kit (asset group Logos). Use the color lockup on light grounds and the white-and-color lockup on dark grounds; keep the kit's clear space. `brand-blue` #0091fd is the "AI" of the wordmark; it appears in marks and, in the dark themes, as `accent-soft` and `data-1`, but never as text on a light ground. `brand-sky` and `brand-deep-blue`, from the near.ai/brand palette, are for illustration only.

- **The wordmark leads.** Product headers carry the Near AI wordmark: the menu-bar popover, the chat's masthead, the marketing header. A product name sits beside it as a typeset lockup after a 1px divider, as "Gateway" does on the site (NDS-27).
- **The N stands alone.** Without its tile, the N is a product mark: the menu-bar item, the edge rail's app tile, the chat's reply icon, the first run's hub. It draws itself like a marker at a welcome and animates beside a reply while one is being worked on, always from the kit's own path data (NDS-26). It is never redrawn, recolored or given effects beyond those moments.
- **Names.** The brand is spelled Near AI. The macOS app is Gateway ("Near AI Gateway" in full), formerly Trace; its bundle still ships as "Near.ai" until the code is renamed (NDS-48). "Trace Commons" appears nowhere a person can see; copy says "this app" and "the server that receives your traces" (NDS-28). "Private AI" names the destination that answers an agent's calls. How the chat product is named is open question 4.
- **App icons** are built from the tile in Icon Composer, `brand-tile` in light and `brand-tile-dark` in dark (NDS-47).

## Intentional additions

trace-commons defines the desktop vocabulary. These components are added for the platforms and products it did not cover, each grounded in Apple, Material 3 or Unity guidance:

- `Sidebar`, `NavigationRail`, `TabBar`, `Toolbar`: navigation for web, tablets and phones (HIG tab bars and sidebars; M3 navigation bar and rail; the M3 navigation drawer is replaced by the expanded rail).
- `Sheet`, `Tooltip`, `CommandPalette`: touch presentation with detents, pointer tooltips, and one command registry on web, Windows and Linux.
- `SearchField`, `Slider`, `NumberField`, `DataTable`, `PropertyInspector`: data entry and dense pro-tool panels (Unity Editor Foundations and App UI).
- `Toast`, `ProgressBar`: undo after reversible actions, and determinate progress for long work.
- `Message`, `PromptComposer`, `ProofTag`, `AgentRun`, `ToolCall`: AI and agent surfaces (HIG generative AI; App UI thread and composer).
- `Logo`: the Near AI lockups.
- `StatusItem`, `GetStartedCard`, `ProofSeal`: the macOS menu-bar item (NDS-33), the shared get-started card (NDS-39) and the key-derived proof seal (NDS-43), added from the products' own designs.

## Sections

Foundations: Architecture and theming, Color, Glass and materials, Typography, Layout, density and targets, Shape and elevation, Motion, Iconography, Accessibility, Writing and content. Pattern libraries: Navigation and commands, Desktop, Web, Tablet, Phone, Spatial, Dense and pro-tool, AI and agent, Feedback and states, Forms and data. Reference: Platform crosswalk, Implementation, Decisions and open questions.
