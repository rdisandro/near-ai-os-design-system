# Accessibility

Every Near AI surface holds the same floors on every platform, measured against the worst ground glass can show, and checked by tests in each theme. Components carry the semantics of the system controls they stand in for, author no words of their own, and follow the person's settings for text size, motion, transparency and contrast. A product theme can change the accent; it can never lower a floor.

## The floors

| What | Floor | Measured on |
|---|---|---|
| All text: body, labels, placeholders, micro tags, badge counts, links | 4.5:1 | The worst-case ground for its surface |
| Text in the increased-contrast themes (`light-hc`, `dark-hc`) | 7:1 | The worst-case ground, with `menu` the hardest |
| Marks that carry meaning on their own: selected fills, the focus ring, lone status dots, switch and checkbox state, icon-only controls, field boundaries, chart series | 3:1 | The ground they sit on; status marks on `pane-opaque`, series on `surface-chart` |
| Status dots and glyphs beside words | Supplementary | The words carry the meaning; the status mark tokens still clear 3:1 on `pane-opaque` |

There is no large-text exemption and no designer override (NDS-6). Disabled controls are exempt, as WCAG allows, so a disabled control (`opacity-disabled`, 0.45) always has a sentence nearby, at full contrast, saying why it is unavailable.

### How contrast is measured

Contrast uses WCAG 2.x relative luminance with the sRGB linearization threshold 0.04045, from one shared helper per language. Glass shows whatever is behind it, so every ground is composed bottom-up from the worst desktop: pure white under dark glass, #333333 under light glass (light Liquid Glass frosts a black desktop no darker than that). Over it go `glass-veil`, then `pane-fill`, then the tier's fill (`card`, `card-quiet`, `field`, `control`). Floating surfaces start from the desktop and add `popover` or `menu`. This is trace-commons' `FlatThemeContrastTests` model, applied to all six themes; Architecture and theming describes it in full. Every pair and its ratio is recorded in `contrast-report.json`.

### What each theme passes

| Theme | Pairs checked | Pass | Closest text pair | Closest mark pair |
|---|---|---|---|---|
| `light` | 32 | 32 | `text-placeholder-on-opaque` on `pane-opaque`, 4.57 | `toolbar-glyph-off` on a control, 3.03 |
| `dark` | 33 | 33 | `caution-text` on the pane, 4.55 | `toolbar-glyph-off` on a control, 3.00 |
| `light-hc` | 33 | 33 | `text-on-status` on `badge-fill`, 7.13 | `neutral` mark on `pane-opaque`, 3.09 |
| `dark-hc` | 34 | 34 | `text-on-accent` on `accent-pressed`, 7.03 | `edge-hc` on the pane, 3.32 |
| `gateway-light` | 32 | 32 | `text-placeholder-on-opaque` on `pane-opaque`, 4.57 | `toolbar-glyph-off` on a control, 3.03 |
| `gateway-dark` | 33 | 33 | `caution-text` on the pane, 4.55 | `toolbar-glyph-off` on a control, 3.00 |

Focus rings clear 3:1 in every theme: 3.12 light and gateway-light, 3.17 dark and gateway-dark, 4.64 light-hc, 5.62 dark-hc. The dark themes' navy off knob holds 3:1 on its 38% track (3.34 on `pane-opaque`), and a passed proof's `proof-text` holds 5.37 (light) and 7.23 (dark) on `proof-tint`. The status marks clear 3:1 on `pane-opaque` everywhere, and `data-1` to `data-8` clear 3:1 on `surface-chart` in every theme.

In `light-hc` the badge turns deep red (`badge-fill` #b01218) with a white count (`text-on-status` #ffffff) at 7.1:1, because a dark count on a light red tops out near 5:1.

### Flagged values

A product theme's source value that misses a floor stays exact, flagged in its token note, and blocks that theme from shipping under the parent until it is fixed (NDS-6). None is flagged today. Gateway's two were its dark purple selected fill (1.09:1), which left when it took the parent accent (NDS-22), and its hidden-toolbar glyph (2.27:1 light, 2.63:1 dark), which took the parent's greys (NDS-50).

## Focus

The parent specifies a focus ring and turns it on by default (NDS-5): 2px solid `focus-ring`, 2px outside the control, following its shape (radius = the control's radius + 2), shown for keyboard focus only (`:focus-visible` on the web; the system focus effect under Full Keyboard Access on Apple platforms).
- Text fields, buttons, switches and tabs show the ring. Lists, trees and tables show focus as a full-row highlight (`selection` with `text-on-accent`), never as a ring around each row. [HIG: focus and selection]
- A product may turn the ring off with `.nr-focus-off` on the web or `.focusEffectDisabled()` in SwiftUI. Gateway does, by owner ruling on 2026-10-11. **Turning the focus ring off fails WCAG 2.4.7 (Focus Visible).** A product that does so still keeps focus order, Full Keyboard Access and the list selection highlight working.
- Never move focus without a person's action. Streaming output, new messages and finished agent runs never take focus from the composer.
- A modal, sheet or popover sets its initial focus and returns focus to its trigger when it closes.
- Sticky bars, toasts and floating toolbars never cover the focused element (WCAG 2.4.11).

## Keyboard

| Key | Does |
|---|---|
| Tab, Shift-Tab | Moves between components (one stop each) |
| Arrow keys | Move within a component: list rows, tree items (Left and Right collapse and expand), radio options, segments, tabs, menu items |
| Home, End | First and last item in a list or menu |
| Space | Activates a button, toggles a checkbox or switch, opens a picker |
| Return | Activates the focused button or row; in a modal, takes the default button |
| Escape | Closes the topmost menu, popover, sheet or modal and returns focus; reverts an edit in progress in a dense field; goes back one level in a breadcrumb |
| Mod+. and Escape | Stop a running generation (NDS-14) |
| Mod+F, Mod+1…n, Mod+, | Search, tabs in order, Settings |

- **One tab stop per composite.** A list, tree, radio group, segmented control or tab row is one stop; arrows move inside it and typeahead jumps by name. A row is never its own tab stop (trace-commons tests this).
- **Return takes the default, and the default is never destructive.** It is never Cancel either. An irreversible send or consent action is drawn prominent but never answers Return (NDS-15), and a send such as Submit has no shortcut at all. Only the topmost modal answers keys.
- **macOS.** Full Keyboard Access must reach every control, and the menu bar lists every command so nothing needs a pointer (Navigation and commands).
- **iPadOS.** Use focus groups: Tab moves between groups (sidebar, list, composer), arrows move within one. Implement keyboard navigation only for text fields, text views, sidebars and collections, and leave buttons, segmented controls and switches to Full Keyboard Access. Order groups with `focusGroupIdentifier` and mark each group's primary item with `UIFocusGroupPriority`.
- **Web, Windows and Linux.** Every control is reachable by Tab with a visible indicator (WCAG 2.1.1). Use roving `tabindex` inside composites. Keep disabled items in toolbars and menus discoverable with `aria-disabled="true"`; use `disabled` elsewhere. No keyboard traps.
- **Android.** Hardware keyboards and D-pads follow the same model; Compose focus order follows reading order, adjusted with `focusProperties`.
- **Shortcuts** are written `Mod+Key` (Cmd on Apple, Ctrl elsewhere). Never override a system shortcut. A single-key shortcut is either remappable or active only while its component has focus (WCAG 2.1.4).

## Screen readers

VoiceOver (Apple), TalkBack (Android), and NVDA, JAWS and Narrator on the Windows shell all read the same structure.
- **Components author no words** (NDS-16). The consumer passes the label, value, hint and state words from the copy source; the component wires them into the platform API. A missing word renders empty and fails review; a component never invents a fallback.
- **Native representations.** A custom control declares the semantics of the system control it replaces. In SwiftUI, give it an `accessibilityRepresentation` built from the native `Toggle`, `Picker` or `Button`, so VoiceOver speaks "checked", "mixed", "expanded" or "2 of 3" in the person's language. On the web use native elements first (`button`, `input type="checkbox"`, `dialog`, `details`) and the WAI-ARIA patterns only for composites with no native element (tree, tablist, listbox, menu). In Compose set `Role`, `toggleableState` and `stateDescription`, the last from the copy source.
- **Headings.** Mark screen, pane and card titles as headings (`.isHeader`, `heading()`, `h1`–`h6`), one `h1` per page, levels in order. A heading's words match the navigation label that leads to it. Tree depth may map to heading levels where it organizes the page (Gateway's folders and traces).
- **Landmarks on the web.** Use `banner`, `navigation`, `main`, `complementary`, `search`, `contentinfo`, and labeled `region` and `form`.
- **Grouping.** A list row, card, legend cell or `StatCard` is one element with a combined label (`.accessibilityElement(children: .combine)`, `Modifier.semantics(mergeDescendants = true)`, a single accessible name on the web). Notices, menus and modals are containers; a modal is marked modal (`.isModal`, `aria-modal="true"`).
- **Status in words.** Status dots and decorative glyphs are hidden; the word is read. An unknown value reads the product's unknown word ("unavailable"), never "dash" and never zero.
- **Icon-only controls.** The accessible name equals the tooltip and the copy string. Repeated controls are distinguishable: "Save episode assessment", "Refresh saved specifications", never three buttons called "Save".
- **Live content.** Announce streaming AI text politely at sentence or paragraph boundaries, never per token; announce when a run finishes or stops; make blocking errors assertive and nothing else. Use `AccessibilityNotification.Announcement` on Apple, `aria-live="polite"` on the web, and `liveRegion` in Compose.
- **Charts need words.** Each bar or bucket is one element with a description, or the chart offers a table view (NDS-20); on Apple, add an `AXChartDescriptor` so Audio Graphs can play it. A chart hidden from assistive technology sits next to a text alternative. As trace-commons puts it, "the bars are a picture, and a picture needs its words." See `BarGraph`.
- **Images.** Alt text describes what the image shows; decorative images take `alt=""` or `accessibilityHidden(true)`.

## Touch and pointer targets

| Input | Token | Recommended | Minimum |
|---|---|---|---|
| Touch on iOS and iPadOS | `target-touch-apple` | 44 | 28 |
| Touch on Android and touch web | `target-touch-android` | 48 | 48, with 8 between targets |
| Gaze and pinch on visionOS | `target-spatial` | 60 | Centers 60 apart |
| Pointer on macOS and desktop web | `target-pointer` | 28 | 20 |

- The visible control may be smaller than its target; the hit area extends invisibly to the target size and never over a neighbor (see Layout, density and targets). trace-commons' small controls (the 22×24 kebab, the refresh pill, the 12pt info glyph, the 15pt checkbox) all get hit areas.
- On the web, WCAG 2.5.8 asks for 24×24 CSS px. A smaller pointer target passes only by spacing: a 24px circle centered on it must not touch another target or its circle. In dense toolbars that means at least 4px between 20px buttons.
- The dense tier (`.nr-dense`, 20px rows) is for pointer input only. Touch density never shrinks below the touch floor.
- Every gesture has an on-screen alternative: swipe actions also sit in the row's menu, drag-to-reorder also exists as Move commands, pinch-to-zoom also has buttons (WCAG 2.5.7). No custom multi-finger gestures.

## Text size

| Platform | The person's setting | How components follow it |
|---|---|---|
| iOS, iPadOS | Dynamic Type, xSmall to xxxLarge and AX1 to AX5 (body 14 to 53pt; Large, the default, is 17) | `ios-*` styles map to text styles; custom sizes scale with `UIFontMetrics` or `relativeTo:` |
| macOS | The system text size, through text styles | Every `mac-*` step is a macOS text style at its default size; long reading views (transcripts, the review sheet) also offer View > Bigger and Smaller |
| Android | Font scale, up to 200% | `sp` for text; text and line height scale while padding and gaps stay at 1× |
| Web, Windows and Linux shells | Browser zoom and default font size | `rem` sizes; 200% zoom with no loss (WCAG 1.4.4); reflow at 320 CSS px (1.4.10); user text-spacing overrides (1.4.12) |
| visionOS | Dynamic Type | As iOS, with the bolder visionOS styles |

- Controls use minimum heights (`size-control`, `size-cta`, `size-list-row` are floors), so labels grow and wrap. Fixed sizes are for glyphs inside fixed-size controls only.
- Truncate only when the full text stays reachable (a tooltip on pointer, an expansion on focus, a full-text view). Never truncate a button label.
- At accessibility sizes, stack inline glyphs and timestamps under the text, drop to fewer columns, and keep primary content at the top (`isAccessibilityCategory`).
- Bold Text comes free with the system faces; keep it working by never hard-coding weights below the style's.
- Test at AX5 on iOS, 200% on Android and the web, and the largest macOS text size. See Typography.

## Motion

Nothing moves under Reduce Motion (NDS-11). The settings arrive as `accessibilityReduceMotion` (and `accessibilityPrefersCrossFadeTransitions`) on Apple, Android's remove-animations setting, and `prefers-reduced-motion` on the web, which also carries Windows' "Animation effects" off. Under them, movement becomes an instant change or a `duration-fast` fade; spinners stand still beside their words; skeletons stop pulsing; symbol effects stop; looping decoration holds one frame; auto-scroll jumps; streaming text lands in chunks. See Motion for the full list.

Beyond Reduce Motion:
- Nothing flashes more than three times a second (WCAG 2.3.1), and nothing plays on its own.
- Never auto-dismiss an error. A `Toast` with Undo or Retry pauses while hovered or focused, uses the platform's recommended timeout (Android `getRecommendedTimeoutMillis`), and its action stays reachable elsewhere (Edit > Undo, Mod+Z).
- Never put a decision on a timer. Undo counts up from a real instant ("approved 12s ago"), never down to a deadline the app cannot see.

## Transparency, contrast and glass settings

### Reduce Transparency

On Apple platforms Reduce Transparency is the system's to apply (NDS-23): the native material frosts itself, and the painted veil and fill stay on top unchanged, following Apple's guidance. Where a product paints its own glass, read the setting (`prefers-reduced-transparency: reduce` on the web, the shells' own flags) and paint every pane and floating surface `pane-opaque` with no blur; cards and controls keep their painted fills on top. Android has no such setting; the Android stack paints `pane-base` below API 31 and `pane-opaque` in battery saver. The Windows shell paints `pane-opaque` when the system's transparency effects are off. Test Reduce Transparency and Increase Contrast separately and together, in both appearances. See Glass and materials.

### Increase Contrast and the `-hc` themes

Increased contrast follows the system (NDS-17): Increase Contrast on Apple platforms (`colorSchemeContrast == .increased`), the contrast level and high-contrast text on Android, and `prefers-contrast: more` on the web. It selects `light-hc` or `dark-hc`:
- text roles solve to 7:1 on every ground, and the light accent darkens to #01599f;
- the veil deepens to 90% and card, field and control fills rise;
- every painted surface, control and field gains a 1px `edge-hc` edge, and `hairline` and `rule` darken (black 45% in light-hc);
- system glass gets its own contrasting border from the OS, so never add `edge-hc` to it.

On macOS 27 and iOS, Show Borders (`accessibilityShowBorders`) asks for visible edges on custom interactive controls even without Increase Contrast; draw `edge-hc` on controls and fields when it is on.

### Forced colors on Windows

In the Windows shell, `@media (forced-colors: active)` replaces the palette with the person's system colors:
- panes, floating surfaces and cards become `Canvas` with a 1px `CanvasText` border; shadows and `backdrop-filter` go;
- text is `CanvasText`, controls `ButtonFace` and `ButtonText`, selection `Highlight` and `HighlightText`, disabled items `GrayText`, links `LinkText`;
- the focus ring stays an `outline`, which the system recolors and keeps visible;
- glyphs use `currentColor` so they follow; status dots draw in `CanvasText` (the words carry the meaning);
- charts set `forced-color-adjust: none` on the plot only, and keep their labels.

Native Windows controls use the platform's high-contrast resources.

### Clear and Tinted glass

Apple's Liquid Glass setting (Clear or Tinted from the 26.1 releases; a continuous slider from most transparent to most tinted on 27) changes system glass: toolbars, tab bars and system sheets. Near AI's painted glass (NDS-7) does not follow it, because no public API reports the value. Legibility never depends on the setting, since the veil is measured at the worst case. Test both ends: with Tinted, system bars read denser than the painted panes beside them, an accepted trade-off.

## Color and color-vision safety

- **Status is a dot or a glyph plus words** (`StatusLabel`, `Tag`, `Notice`), never color alone. A failed `Tag` adds an outline so it differs in shape too.
- **Selection uses a second cue**: label weight, a checkmark, or a filled glyph, alongside the fill.
- **Links inside running text are underlined.** Standalone links (Dismiss, Look inside) can rely on position and wording.
- **Charts** use `data-1` to `data-8` in fixed order, validated for protanopia and deuteranopia on adjacent pairs and at 3:1 on `surface-chart`. Charts with two or more series carry a legend or direct labels; line charts with three or more series add markers or dash patterns; values never live only in a tooltip. A reduced companion series (`opacity-series-reduced`) still clears 3:1. See Color and Forms and data.
- Green and red statuses differ in lightness as well as hue, and always carry words.

## Hover, gestures and time

Hover is never the only way to reach anything (see Layout, density and targets).

| Hover behavior | Equivalent |
|---|---|
| Info text on an info glyph | The glyph is a real button: click or Return pins the popover, focus shows it, Escape closes it |
| Menu-bar state pills expand on hover | They expand on focus and on click |
| The edge rail opens on hover | Its handle has an accessibility action and a keyboard command; everything it shows is also in the app |
| Map nodes show node cards on hover | Nodes are focusable; focus and tap show the card |
| Bar values appear on hover | Each bar is an element with its value in words; a table view lists them all |
| Tooltips name icon-only controls | The same words are the accessible name; touch shows them on long press |

Content that appears on hover or focus can be dismissed with Escape, can be hovered without vanishing, and stays until the person moves away (WCAG 1.4.13). Consequences, scope and destructive effects always sit in visible copy beside the action; a tooltip or accessible name alone is not enough (see Writing and content).

## Testing

### Automated, on every change

- **Contrast suites per theme.** Port trace-commons' suites (`TextContrastTests`, `LightContrastGroundsTests`, `FlatThemeContrastTests`, `AccentFillContrastTests`, `SwitchContrastTests`, `SelectionContrastTests`, `ToolbarGlyphContrastTests`, `ChartSeriesContrastTests`, the placeholder check in `FormControlTests`) to run over every theme in `tokens.json`, the `-hc` themes included, and write `contrast-report.json`. A failing pair fails the build unless it is on the flagged list, and the flagged list can only shrink.
- **Component contracts.** Components author no words; a list row is not a tab stop; Escape and Return follow the modal rules; every animation has a Reduce Motion path; controls grow with text (trace-commons' `LargeTextTests`); every hit area meets its target token; every status dot is followed by words; wording ratchets hold their baselines.
- **Web.** Run axe-core on every component preview in all six themes and under forced-colors emulation; run a Playwright keyboard pass that asserts focus order and that every control is reachable; snapshot with `prefers-reduced-motion` and `prefers-contrast` emulated.
- **Apple.** Run `performAccessibilityAudit()` in XCUITests per screen; snapshot at AX5.
- **Android.** Enable the Accessibility Test Framework checks in Espresso and Compose UI tests.
- Make the accessibility suites required checks, so a regression never lands on the main branch first.

### Manual, before each release

- A VoiceOver pass on macOS and iOS (rotor headings, labels, values in words, modals contained), a TalkBack pass on Android, and an NVDA pass on the Windows shell.
- A keyboard-only walk through every screen, checking focus order and visibility, plus Full Keyboard Access on Mac and iPad.
- The settings matrix: Increase Contrast and Reduce Transparency separately and together in both appearances; Reduce Motion; AX5; Android at 200%; the browser at 200% and at 320px; forced colors; the Clear and Tinted ends.
- Glass on a device over pure white and pure black wallpapers, recording the measured values for each shipped shell.
- A color-vision simulation of every chart and status-heavy screen.

[trace-commons: §7 accessibility rules and tests] [HIG: accessibility, focus and selection, keyboards] [Liquid Glass: accessibility] [M3: accessibility] [material-web: accessibility] [Unity Foundations: accessibility]
