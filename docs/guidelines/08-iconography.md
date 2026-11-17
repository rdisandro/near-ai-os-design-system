# Iconography

Near AI products draw interface icons from the platform's own set: SF Symbols on Apple platforms, Material Symbols Rounded on Android and on the web (which also carries the Windows and Linux shells). One icon registry gives every icon a semantic name and maps it to both sets, so code asks for `refresh` and each platform draws its native glyph. Custom glyphs, third-party tool logos, app icons and brand marks are separate families with their own rules, covered below.

## Principles

- **Words first.** Most buttons are text buttons. Use an icon for a frequent, well-known action (search, close, add, refresh), for navigation destinations that also carry a label, and for status beside words. In a menu or a group, give every item an icon or none. [Unity Foundations: iconography] [HIG: menus]
- **One concept per glyph.** A glyph means the same thing everywhere in a product. If `eye.slash` means Paused in the menu bar, it never means "hidden" on another screen. Gateway breaks this today: `eye` means Watching in the menu bar and Settings, and since 2026-11-02 also the Automatic-sharing toggle in the Traces toolbar. Give one of them another glyph.
- **An icon never carries status alone.** Status is a dot or a glyph plus words (`StatusLabel`, NDS-16). A lone glyph that changes state (a toolbar toggle, an icon-only button) needs 3:1 against its ground and a name in words.
- **Every icon-only control has a name.** The tooltip, the accessible name and the copy-source string are the same words. The glyph itself is hidden from assistive technology.
- **Glyphs take text and glyph tokens.** Interface glyphs use `text-primary`, `text-secondary`, `toolbar-glyph`, `toolbar-glyph-off` or `text-on-accent` on an accent fill. Status glyphs use the status mark tokens (`positive`, `caution`, `critical`, `neutral`). Never color a functional glyph with `brand-blue` or a product's mark colors.
- **Selection uses two cues.** A selected icon switches to its fill variant and takes the selected tint, and its label gains weight. Color alone never shows selection. [M3: navigation bar]
- **Code names semantics, never raw symbol strings.** trace-commons writes about 40 SF Symbol names inline; the parent replaces them with registry names.
- **Glyphs, not characters.** A glyph inside a control comes from the registry, never a typed character ("→", "›"), so it centers optically. A disclosure chevron rotates about its own center.

## Icon sets by platform

| Platform | Set | Default style | How it ships | License |
|---|---|---|---|---|
| macOS, iOS, iPadOS, visionOS | SF Symbols | Outline, monochrome, weight matched to the adjacent text | By name from the system (`Image(systemName:)`, `NSImage(systemSymbolName:)`) | Apple platforms only |
| Android | Material Symbols Rounded | Fill 0, weight 400, grade 0 (−25 in dark themes), optical size 24 | Vector drawables generated from the registry at those axes | Apache 2.0 |
| Web, and the Windows and Linux shells | Material Symbols Rounded | Fill 0, weight 400, grade 0 (−25 in dark themes), optical size 20 | An SVG sprite generated from the registry, or a self-hosted subset of the variable font | Apache 2.0 |
| Dense tools inside the Unity Editor | Registry glyphs exported to Unity's icon format | 16px artboard, 14px live area, `@2x` 32px, `d_` dark variants | Transparent PNG | As the source set |

Rounded is the Material style closest to SF Symbols' rounded terminals and to the parent's radii (control 11, card 16, pane 20). Never mix Outlined, Sharp and Rounded in one product, and never mix Material Symbols into an Apple build that has a fitting SF Symbol.

Load icon fonts or sprites from the product's own origin. A request to a third-party font host tells that host about every page view, which is a data consequence a Near AI surface must not create silently. [M3: icons] [material-web: md-icon]

## SF Symbols on Apple platforms

### Rendering modes

| Mode | Use in Near AI products |
|---|---|
| Monochrome | The default for every interface glyph, colored with one text or glyph token. |
| Hierarchical | Large glyphs (20pt and up) whose layers read better with depth, such as an empty-state glyph. One token; the system sets layer opacities. |
| Palette | Only for a status glyph whose secondary layer needs a token of its own. Both layers still meet their floors. |
| Multicolor | Never in interface chrome. Intrinsic symbol colors are not parent tokens and do not follow the themes. |
| Gradient (SF Symbols 7) | Never. Gradients belong to marks, and decorative gradients are off-brand. |

Check every glyph at its real size over the worst-case ground; the Automatic mode only picks a starting point. [HIG: SF Symbols]

### Weights, scales and variants

Match the symbol weight to the text beside it. In SwiftUI a symbol inherits the font it sits in, so set the same text style on the label and the glyph (`Label(title, systemImage:)` with `.font(.callout)`); inside a fixed-size control use the fixed-size modifier (trace-commons' `glassGlyph(_ size:, weight:)`).

| Adjacent type step | Symbol weight |
|---|---|
| `*-body`, `*-caption`, `*-mono` (400) | Regular |
| `*-label` (500) | Medium |
| `*-body-strong`, `*-title`, `*-heading` (600) | Semibold |
| `*-micro`, `*-eyebrow`, `*-display`, `*-number` (700) | Bold |

Use the **small** scale inline with captions and in dense rows, **medium** (the default) everywhere else, and **large** only for emphasis in empty states and onboarding answer rows. Scale changes emphasis without breaking the weight match.

Variants: **outline** is the default. **Fill** marks the selected tab, sidebar item or swipe action; iOS tab bars apply it themselves. **Slash** means off or unavailable (`eye.slash` for Paused watching, `bell.slash` for notifications off). **Enclosed** (`.circle`, `.square`) improves legibility below 14pt, which is why the info glyph is `info.circle`. The registry stores the base name; the component applies the variant for its state.

### Variable values

Variable color fills a symbol's layers as a value crosses thresholds. Use it only for a value that changes (a usage quota, a signal level), never to show depth, and always show the value in words or figures beside it. Never use a variable symbol as a progress indicator on its own; `ProgressBar` and `Spinner` carry progress with a label.

### Symbol animations and Reduce Motion

Symbol effects carry small state changes. They never overshoot (NDS-11), never loop as decoration, and never carry meaning the words do not also carry.

| Effect | Allowed use | Under Reduce Motion |
|---|---|---|
| Replace, Magic Replace | A state swap in place: Send to Stop in `PromptComposer`, Watching to Paused | Instant swap |
| Appear, Disappear | A glyph entering or leaving with its row | Instant |
| Pulse | Ongoing activity beside a word ("Listening") | Static glyph; the word stays |
| Variable color (iterative) | A tool running in `ToolCall`, beside its progress text | Static glyph |
| Draw On, Draw Off | Progress that completes once | Final state |
| Bounce, Wiggle, Breathe, Scale, Rotate | Not used. Bounce and Wiggle overshoot; Breathe and Scale change size; `Spinner` owns indeterminate progress | Not applicable |

Gate every effect on the setting explicitly (`.symbolEffect(.pulse, isActive: !reduceMotion)` with `@Environment(\.accessibilityReduceMotion)`); do not rely on the system to soften it. Symbol effects are never one of a product's hero moments. See Motion. [HIG: SF Symbols animations]

## Material Symbols on Android and the web

Material Symbols is one variable font with four axes. The registry fixes them per context so every exported glyph matches.

| Axis | Range | Near AI setting |
|---|---|---|
| Fill | 0–1 | 0 by default; 1 for the selected navigation item, a selected icon toggle and filled status glyphs |
| Weight | 100–700 | 400 beside body and caption text, 500 beside `*-label`, 600 beside `*-body-strong` and titles. Never below 300; never mix weights in one row |
| Grade | −25 to 200 | 0 in light themes; −25 in dark themes so light glyphs on dark grounds do not bloom. No positive grade; emphasis comes from weight and fill |
| Optical size | 20, 24, 40, 48 | 20 for 16–20px glyphs (desktop web, dense panels), 24 for 24dp Android icons, 40–48 for empty-state and onboarding glyphs |

- The grid is 24dp with a 20dp live area and 2dp padding; keylines are an 18dp square, a 20dp circle and 20×16 rectangles. Custom glyphs for Android and web follow it.
- Beside text, use the glyph at the text's size and optical weight and shift it down about 11.5% of the text size so it sits on the baseline.
- On the web, mark every glyph `aria-hidden="true"` and name the button, link or tab instead. Use `currentColor` for fill and stroke so glyphs follow the theme and forced colors.
- Navigation items always show labels. Glyphs smaller than 20dp need a visible label unless they are simple and familiar. [M3: icons]

## The icon registry

The registry is one table beside `tokens.json`. Each entry has a semantic name, its meaning, an SF Symbol, a Material Symbol, whether it mirrors in right-to-left layouts, and optional product overrides (Gateway's custom glyphs). A generator emits a Swift enum, Android vector drawables and a web sprite from it, so a product never types a symbol name. The accessible name is not in the registry; it comes from the copy source at the call site, because the same glyph names different actions on different screens.

To add an icon, find a fitting glyph in both sets. When one set lacks a match, choose the glyph closest in meaning even when the shapes differ (Apple's Share is a box and arrow, Android's is three nodes). When neither fits, draw a custom glyph for both (see Custom glyphs).

### Starter registry

| Name | Means | SF Symbol | Material Symbol | Notes |
|---|---|---|---|---|
| `home` | Home destination | `house` | `home` | Fill when selected |
| `agents` | Agents and agent-made content | `sparkles` | `auto_awesome` | Never decorative |
| `private-ai` | The Private AI destination | `cpu` | `memory` | Names a place. Never a lock or shield |
| `traces` | Traces destination and lists | `point.topleft.down.to.point.bottomright.curvepath` | `timeline` | Gateway override: four nodes in a T (`GlassTraceNodesGlyph`), three across joined by a line and one below the middle |
| `folder` | A watched folder or project | `folder` | `folder` | Gateway override: `GlassGlyph.folder` |
| `trace` | One trace: a recorded working session from a coding tool | `text.page` | `article` | `doc.text` before SF Symbols 6. The word in copy is "trace" (NDS-29) |
| `account` | Account and sign-in | `person.crop.circle` | `account_circle` | |
| `settings` | Opens Settings | `gearshape` | `settings` | Gateway override: `GlassGlyph.gear` |
| `history` | History, past activity | `clock.arrow.circlepath` | `history` | |
| `notifications` | Notifications, contribution mode | `bell` | `notifications` | Slash variant when off |
| `search` | Search | `magnifyingglass` | `search` | Never mirrors |
| `filter` | Filter a list | `line.3.horizontal.decrease` | `filter_list` | |
| `sort` | Change order | `arrow.up.arrow.down` | `swap_vert` | |
| `add` | Add, enlarge | `plus` | `add` | |
| `remove` | Remove, reduce | `minus` | `remove` | |
| `close` | Close, cancel, clear | `xmark` | `close` | |
| `edit` | Edit, rename | `pencil` | `edit` | |
| `delete` | Delete | `trash` | `delete` | Destructive; always confirmed or undoable |
| `copy` | Copy | `document.on.document` | `content_copy` | `doc.on.doc` before SF Symbols 6 |
| `share` | Share, export | `square.and.arrow.up` | `share` | Metaphors differ by design |
| `download` | Download, install | `arrow.down.to.line` | `download` | |
| `upload` | Upload | `arrow.up.to.line` | `upload` | |
| `attach` | Attach a file | `paperclip` | `attach_file` | |
| `send` | Send a prompt | `arrow.up` | `arrow_upward` | Replaces with `stop` while running |
| `stop` | Stop a generation or run | `stop.fill` | `stop` | Esc and Mod+. do the same |
| `pause` | Pause | `pause` | `pause` | Media glyph; never mirrors |
| `resume` | Resume, play | `play` | `play_arrow` | Never mirrors |
| `refresh` | Reload from the source | `arrow.clockwise` | `refresh` | Drawn after the word "Refresh" in a pill, never bare (NDS-36). Spins while refreshing |
| `undo` | Undo | `arrow.uturn.backward` | `undo` | Mirrors |
| `redo` | Redo | `arrow.uturn.forward` | `redo` | Mirrors |
| `show` | Visible, watching | `eye` | `visibility` | Gateway also uses it for Automatic sharing; see One concept per glyph |
| `hide` | Hidden, paused watching | `eye.slash` | `visibility_off` | |
| `back` | Go back | `chevron.backward` | `arrow_back` | Mirrors. Native idiom per platform |
| `forward` | Go forward, next | `chevron.forward` | `arrow_forward` | Mirrors |
| `go` | Ends a text link that opens another place ("Open Traces") | `arrow.right` | `arrow_forward` | Mirrors. After the words, never alone |
| `disclosure` | Opens a detail (row chevron) | `chevron.forward` | `chevron_right` | Mirrors |
| `expand` | Expand, open a picker | `chevron.down` | `expand_more` | Gateway override: `GlassGlyph.chevronDown` |
| `collapse` | Collapse | `chevron.up` | `expand_less` | |
| `more` | More actions (overflow) | `ellipsis` | `more_vert` | Gateway override: `GlassGlyph.kebab` |
| `view-menu` | View options | `line.3.horizontal` | `menu` | Gateway override: `GlassGlyph.viewMenu` |
| `info` | More information | `info.circle` | `info` | 12pt on macOS |
| `warning` | Needs a look, caution | `exclamationmark.triangle` | `warning` | Gateway override: `GlassWarningGlyph` |
| `error` | Failed | `exclamationmark.circle` | `error` | With words; never in empty states |
| `success` | Done, succeeded | `checkmark.circle` | `check_circle` | Never mirrors |
| `verified` | Proof checked | `checkmark.seal` | `verified` | `ProofTag` |
| `pending` | Proof or result expected | `clock` | `schedule` | `ProofTag` |
| `no-proof` | No proof recorded | `minus.circle` | `do_not_disturb_on` | Shows that proof is absent |
| `locked` | A value that cannot change | `lock` | `lock` | Means "cannot be edited" only |
| `credential` | A key, token or saved sign-in | `key` | `key` | Never a checkmark shield |
| `sample` | Sample data stands in for the person's own | `testtube.2` | `science` | On the sample-data banner (NDS-39) |
| `chart` | Insights, a chart view | `chart.xyaxis.line` | `show_chart` | |
| `graph-strip` | Shows the activity graph | `chart.bar` | `bar_chart` | Gateway override: `GlassGlyph.graph` |
| `map` | Shows the flow map | `map` | `map` | Gateway override: `GlassGlyph.map` |
| `inspector` | Shows the inspector pane | `sidebar.trailing` | `view_sidebar` | Mirrors. Gateway override: `GlassGlyph.inspector` |

Two entries need care. `locked` describes immutability ("A saved specification cannot be changed."). It never decorates Private AI, a consent screen or a data destination, where a padlock or shield would read as a security promise. `more` follows the platform: Apple shows the horizontal `ellipsis` (or `ellipsis.circle` in toolbars), Android and the web the vertical `more_vert`. Reserve the ellipsis glyph for overflow. [HIG: icons, standard icons]

## Sizes by density

The glyph size never sets the hit target; the control's target token does (`--nr-target`, see Layout, density and targets).

| Context | Compact (macOS) | Regular (web) | Touch (iOS) | Touch (Android) | Dense |
|---|---|---|---|---|---|
| Glyph in a control or row | 16 (`size-glyph`) | 16, opsz 20 | Follows the text style (17pt body, medium scale) | 20dp in buttons and chips, 24dp in icon buttons | 16 (14 live) |
| Toolbar glyph | 13 (Gateway's own glyphs 14×12) | 20 | System bars size their own; drawn toolbars 20 | 24dp | 16 |
| Info glyph | 12 | 16 | 17, small scale | 18dp | 12 |
| Disclosure chevron | 10, semibold | 16 | System (`chevron.forward`, small scale) | 24dp | 12 |
| Tool logo in its tile | 15 in 22 (`size-tool-tile`); 20 in 30; 12 in an 18 menu-bar row | 15 in 22 | 20 in 30 | 20dp in 30dp | 12 in 16 |
| Empty-state glyph | 22 | 32, opsz 40 | 34, large scale | 40dp, opsz 40 | not used |

On touch the visible glyph sits inside a 44pt (Apple) or 48dp (Android, touch web) target; on pointer the minimum is 20 and the recommendation 28.

**Dense tools in the Unity Editor.** Follow the Editor's icon conventions: a 16×16 artboard with a 1px margin (14×14 live), never a border to make negative space; a single-size icon ships at 16 plus a 32 `@2x` file; anything shown in a project browser ships at all five sizes (`@16` to `@256`); a `d_` prefix marks the dark-theme variant (an icon without one serves both themes); a ` On` suffix marks the selected state (`d_Inspector On@2x.png`). Unity's IMGUI does not take SVG, so export transparent PNGs from the registry. Unity reserves blue for controls that can be focused, pressed or selected; Near AI's accent rule agrees. [Unity Foundations: iconography]

## Custom glyphs

Draw a custom glyph only when neither set has a fitting symbol, or when a product theme overrides a registry entry.
- Draw on a 16-unit grid (1-unit margin, 14 live) for inline and toolbar glyphs, or on Material's 24-unit grid for standalone ones.
- Use one ink (`currentColor`), strokes of 1.3–1.8 units with round joins, and the same cap style across a family. Check the stroke at the drawn size against an SF Symbol at Regular and Material weight 400 beside it.
- Build optical centering into the artwork: an asymmetric glyph such as a download arrow sits slightly high in its box.
- On Apple platforms, a glyph that sits beside text ships as a custom SF Symbol made from the SF Symbols app template, so it gains weights, scales and localization. A glyph inside a fixed-size control can be drawn as a shape from path data, as trace-commons does through `SVGPathData`.
- Declare directionality for every custom glyph, mark it decorative, and let the control carry its name.

### Gateway's glyphs (#1146)

The Gateway theme overrides nine registry entries with the #1146 artwork so the macOS, web and desktop shells match. Each lives once in the registry as path data; no shell copies it by hand.

| Glyph | Overrides | Artwork box | Drawn at | Stroke (box units, drawn) |
|---|---|---|---|---|
| `viewMenu` (three lines) | `view-menu` | 14×12 | 14×12 | 1.4 |
| `graph` (frame with a split lower strip) | `graph-strip` | 14×12 | 14×12 | 1.3 |
| `map` (folded map) | `map` | 14×12 | 14×12 | 1.3 |
| `inspector` (frame with a trailing column) | `inspector` | 14×12 | 14×12 | 1.3 |
| `gear` | `settings` | 24×24 | 15 | 1.7, about 1.06pt |
| `chevronDown` | `expand` | 16×16 | 10 | 1.8, about 1.13pt |
| `folder` | `folder` | 24×24 | 13 | 1.8, about 0.98pt |
| `kebab` (three dots, radius 1.6) | `more` | 4×14 | 4×14 | Filled |

The warning triangle (`GlassWarningGlyph`) replaces `exclamationmark.triangle` in Gateway on every shell. It is drawn in a 16-unit box with a 1.4-unit stroke and round caps and joins: a triangle from (8, 1.75) to (15, 14.25) to (1, 14.25), a bar from (8, 6.25) to (8, 9.75), and a filled dot of radius 0.85 at (8, 11.9). It renders at 12pt by default in the foreground color and stays hidden from assistive technology unless the caller passes its word. Like every warning glyph, it appears beside words, in `caution` ink. [trace-commons: Glyphs.swift, Feedback.swift]

## Status glyphs

- Pair every status glyph with words from the copy source: "Needs a look", "Failed", "Verified". The glyph is hidden; the words are read.
- Use the status mark tokens: `caution` for `warning`, `critical` for `error` and `no-proof`, `positive` for `success` and `verified`, `neutral` for off states, `text-secondary` for `info`. Text beside them uses the matching `*-text` token.
- Never prefix a message with "Error:" or "Warning:". The glyph and the tone already say it. (See Writing and content.)
- Never put an error or warning glyph in an empty state. An empty state explains a condition; a notice explains a failure.
- Proof states (`ProofTag`) are verified, pending and no proof. The tag is a dot plus the word; the glyph is optional and only on roomy surfaces such as an `AgentRun` summary. Where a deployment signs its replies, the key-drawn `ProofSeal` takes the dot's place at 14 in the tag and 20 in the header pill (NDS-43); it is decorative, and the word carries the state.
- A consent or review graphic never uses a shield or padlock. Gateway's first run replaced its review-gate shield with a thumbs-up for this reason.

## Third-party tool logos

Products that connect to other agents show those tools by their logos: Claude, Codex, Antigravity, OpenCode and Theia have vector artwork; tools without cleared artwork (Gemini CLI and Cline today) show two-letter initials.
- **Check the trademark before shipping.** Before a vector logo ships on any platform, check its owner's brand and trademark guidelines (permitted uses, colors, minimum size, clear space, required "works with" phrasing) and record the result with the asset. Until the check passes, the tile shows initials.
- **Use it only to name the tool the person connected.** A logo identifies; it never decorates, never appears in a Near AI app icon, splash screen or marketing without written permission, and never suggests a partnership the owner has not agreed to. Two shipped uses stretch this and are recorded as open: Gateway's first run shows found tools as label-less tiles circling the N (their names are in the list beneath), and the Gateway marketing site recolors the logos into its dithered art.
- **Never alter it.** No recoloring beyond the owner's approved one-color version, no glass, no outline, no cropping into a shape other than the neutral tile.
- **The tile.** The tool tile (`size-tool-tile`, 22; 30 large) is a neutral ink-10% square with radius `radius-tile`. The logo sits at 15 (20 in the large tile) in the tool's tint; menu-bar activity rows use 12 in an 18 tile. Tool tints are product tokens, each 3:1 against the tile.
- **Words.** The tile is hidden from assistive technology. The row or control reads the tool's name from the copy source ("Claude Code", "Codex").
- **One source.** Logo paths live once in the registry. trace-commons kept separate macOS and web copies "in step" by hand; the generator ends that.

## App icons

### iOS, iPadOS and macOS

- Build the icon in **Icon Composer** as an `.icon` file on a **1024×1024** canvas; it replaces the AppIcon asset catalog, and Xcode generates the images for older OS versions.
- Compose a background layer and one or more foreground layers in **at most four groups**. Supply layers unmasked and full-bleed; the system masks to its rounded rectangle and adds the Liquid Glass highlights, refraction, translucency, blur and shadow. Pre-masked art breaks the highlights.
- Prefer SVG layers with any text converted to outlines; use PNG only for raster art or mesh gradients. Bake in no shadows, bevels, blur, glow or specular highlights. Keep shapes solid, frontal and bold, with rounded corners and clean edges.
- Check all **six appearances**: default, dark, clear light, clear dark, tinted light and tinted dark. Keep the same features in every one. For mono and tinted, make at least one prominent element white and map the others to greys. Prefer a colored background for dark-mode distinction over pure black.
- On macOS 27 and later the system adds Liquid Glass layering inside icon artwork; refraction annotations have no visible effect on earlier releases. Preview both in Icon Composer.
- watchOS uses a 1088×1088 canvas masked to a circle; visionOS a 1024×1024 background plus one or two layers, masked to a circle; tvOS an 800×480 parallax stack of two to five layers.
- Never put an SF Symbol, a third-party logo or a word in an app icon. A one-letter mnemonic such as the Near AI "N" is fine. [Liquid Glass: app icons] [HIG: app icons]

### Android adaptive icons

Supply separate foreground and background layers, each 108×108 dp. The system masks them to its shape inside the central 72×72 dp, so keep the mark inside the 66 dp safe circle and let the outer 18 dp per side move under parallax. Add a monochrome layer for themed icons (Android 13 and later). The Android 12 splash screen shows the icon and nothing else; brand moments belong in onboarding.

### Web, Windows and Linux

Ship an SVG favicon with a 32px PNG fallback, a 180px `apple-touch-icon`, and web-manifest icons at 192 and 512 plus a `maskable` 512 whose mark stays inside the central 80% circle. Windows MSIX packages need tile assets at 44, 50 and 150 across scales 125–400; Linux needs hicolor PNGs from 16 to 512 plus a scalable SVG. Tray and menu-bar icons are single-ink template images, with one exception: Gateway's macOS status item is a non-template image (the N in the menu bar's own ink beside a four-color micro graph), drawn for both menu-bar appearances and picked as it draws (NDS-33, `StatusItem`).

### Which mark becomes the icon

- Near AI apps build their icon from the tile (NDS-47): a solid `brand-tile` background layer and the kit's "N", unchanged, as one vector foreground layer in `brand-paper`, centered at 58.5% of the tile's width. Never submit the tile file itself; its rounded rectangle is already masked.
- The dark appearance uses `brand-tile-dark` (#024175) behind the same N, not black. Clear and tinted appearances are left to the system.
- Gateway sets the N layer's glass translucency to 0.25; at the 0.5 default the lower half washes to blue.
- macOS 14 and 15 get PNGs from 16 to 1024 and an `.icns` built from the same document. The N must still read at 16.
- A staging build adds an amber hazard ribbon across the top trailing corner, clear of the N, so it reads at 32 (a faint corner at 16).
- The old Trace bracket mark is retired on macOS. The Windows, Linux and Tauri icons still use it until they move to the tile.

## Brand marks

Marks stay out of the icon registry as functional glyphs.

### The Near AI master brand (NDS-8)

| Lockup | Artwork | Colorings | Use |
|---|---|---|---|
| Primary: the "near AI" wordmark | 730×138 | Color ("near" in `brand-ink`, "AI" in `brand-blue`), white & color, black, white | The default: web headers, sign-in, about screens, onboarding |
| Secondary: the "N" monogram with "AI" | 291×136 | The same four | Where the wordmark does not fit: narrow headers, compact toolbars |
| Tile | 400×396 | Color (a `brand-tile` tile with the "N" in `brand-paper`), white & color (a white tile with the "N" in `brand-tile`) | App-icon contexts, avatars, social cards |

- **Clear space.** The kit's `clear-space` files set the minimum. On the primary lockup it equals the width of the n's stem, 29.5 units on a 138-unit-high mark, about one fifth of the height, on every side. Keep at least one fifth of the lockup's height clear around the secondary lockup and the tile too, and never less than the kit draws.
- **Grounds.** The color lockup goes on light grounds, the white & color lockup on dark grounds and dark glass panes. Never place a lockup over busy scene glows without a pane behind it.
- **Size.** The kit sets no minimum. Ask the brand owner before using the wordmark below 72px wide; below that, use the secondary lockup.
- **Never redraw a mark.** Use the kit's artwork through the `Logo` component: the kit files in `assets/Logos`, or, where a mark must animate or take the menu bar's ink, the kit's own path data rendered in code (Gateway's `GlassNearWordmark` and `GlassBrandMarkDrawing`). Never change the paths, recolor beyond the kit's colorings (product accents included), outline, stretch, rotate, add effects or glass, or set "Near AI" in a typeface to imitate the wordmark. A logo is never a button by itself; when it links home, the link carries the name and the focus ring.
- **Motion only at the named moments** (NDS-26): the N draws itself on a welcome, one shine crosses it every 15 s on the first-run Welcome, and it animates as a chat's thinking mark while a reply is worked on. Each has a Reduce Motion end state (see Motion). The wordmark never moves.

### The N alone

The kit's "N" without its tile is a mark of its own (NDS-26):
- **Product mark.** In `brand-blue` beside the wordmark in a masthead (22 beside an 18-tall wordmark), on a chat's welcome (80 on desktop, 64 on phones), as the first-run hub, and as the app tile in Gateway's edge rail.
- **Menu bar.** At 14 in the menu bar's own ink (white on a dark bar, black on a light one, whatever the app's appearance), leading Gateway's status item.
- **Thinking mark.** At 16, animated, in a chat's live reasoning line; the still N under Reduce Motion.
- **Texture.** The faint tiled field under Gateway's flow map.
- **Product glyphs.** A single-ink product glyph may contain the N, as the chat's conversation glyph does (a speech bubble, tail at the bottom trailing corner, with the N inside at 40%). It takes the glyph tokens (`text-secondary` in a list), like any functional glyph. Don't build other glyphs on the N.

### Product marks

- The Near AI wordmark leads product headers (NDS-27): the menu-bar popover header (16 tall), a chat's masthead, a marketing header. A product name sits beside it as a typeset lockup, after a 1px divider, set in the product's display face at the height of the wordmark's "AI" ("Gateway" on the marketing site).
- Product marks sit inside their product or beside the Near AI lockup, never in place of it outside the product.

## Licensing

- **SF Symbols** are licensed for Apple platforms only (NDS-4), like SF Pro. Never export them to SVG or PNG for web, Android, Windows or Linux builds, including a web shell running on a Mac. Never use a symbol or a lookalike in an app icon, a logo or any trademark. Apple-product symbols may be shown but not modified.
- **Material Symbols** are Apache 2.0. Include the license in each product's open-source notices.
- **Third-party logos** belong to their owners; the trademark check above applies on every platform.
- **Near AI and product marks** come only from the kit and the product asset folders.

## Do and don't

- Do reference icons by registry name and let each platform draw its native glyph.
- Do give every icon-only control the same words as its tooltip and accessible name.
- Do match glyph weight to the text beside it, and use the fill variant plus weight for selection.
- Don't show status with a glyph or a color alone.
- Don't use a padlock or shield to suggest a privacy or security promise.
- Don't animate a glyph under Reduce Motion, and never with bounce or wiggle.
- Don't ship SF Symbols off Apple platforms, or a third-party logo before its trademark check.
- Don't redraw or recolor a Near AI or product mark, and animate one only at the moments NDS-26 names.
