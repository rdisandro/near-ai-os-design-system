# CommandPalette

A searchable list of every command the product offers, opened with Mod+K, that runs the highlighted command on Return; it renders the same command registry as the macOS menu bar, for web, Windows and Linux where no global menu bar exists (NDS-14).

## When to use

- Use it on web and in the Windows and Linux shells as the complete command inventory, beside visible primary actions.
- Use it as the AI entry: the last row hands the typed words to the assistant ("Ask Near AI about “watch”").
- On macOS and iPadOS the menu bar stays the command inventory; a palette is optional there.
- Don't use it on phones. Use a `SearchField` in a `Sheet`.
- Don't make it the only path to an action. Every command also lives in a menu, toolbar or button.

## Anatomy

1. Container: `menu` fill over `blur-floating`, `radius-card-quiet`, `shadow-float`. Width up to `size-readable-width` (680), centred, `modal-inset-top` (52) below the top of the window.
2. Search row: a magnifier glyph and the field (title type, `text-placeholder` prompt), height `--nr-h-row`, a 1px `rule` under it.
3. List: padding `space-8`; group headings in eyebrow type, `text-tertiary`.
4. Result row: height `--nr-h-row`, `radius-tile`, padding `space-10`; glyph (`size-glyph`, `text-secondary`), title with matched characters at weight 700, optional context in caption type `text-tertiary`, optional keycaps.
5. Keycap: caption type on `neutral-tint`, `radius-tile`, at least `size-control-dense` (20) wide.
6. Footer (optional): key hints in caption type, `text-tertiary`, a `rule` above.
7. Empty row: the consumer's sentence ("No commands match “pase”.") in `text-secondary`.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Row height | 40, `mac-body` | 40, `web-body` | not used | not used | 20, `web-label` |
| Field type | `mac-title` | `web-title` | | | `web-body` |
| Width | up to 680 | up to 680 | | | up to 680 |

## Variants

- **Commands**: the registry's commands, grouped (Commands, Folders, Recent).
- **Ask row**: the last group; runs the assistant with the query.
- **Scoped**: opened with a prefix or from a context ("Folders"), showing one group.

## States

| State | Rule |
|---|---|
| Highlighted row | `menu-hover` with `text-on-accent`; glyph, context and keycaps take the same ink. |
| Pointer over a row | `row-hover`; the keyboard highlight stays where it is until the pointer moves. |
| Unavailable command | Hidden. The registry's enablement decides; a palette never lists a command that cannot run. |
| No results | The empty row, plus the Ask row. |
| Increased contrast | 1px `edge-hc` inset edge. Reduced transparency: `pane-opaque`, no blur. |

## Behavior

- Mod+K opens it (Cmd+K on Apple, Ctrl+K elsewhere); avoid shortcuts browsers reserve. Opening focuses the field and highlights the first result.
- Typing filters with fuzzy matching and bolds the matched characters. Up and Down move the highlight and wrap; Return runs the command and closes; Tab moves to the Ask row; Esc clears the query, and a second Esc closes. A click outside closes. Focus returns to where it was.
- A command that needs confirmation opens its `Modal` as usual; the palette never skips the confirmation ladder (NDS-15).
- Shortcuts are written `Mod+Key` and rendered per platform: glyphs in ⌃⌥⇧⌘ order on Apple, words joined by "+" elsewhere.
- Entry is a fade on `duration-standard` with `ease-standard`; under Reduce Motion it appears at once.

## Accessibility

- The container is a `dialog` with the consumer's label. The field is a `combobox` with `aria-expanded`, `aria-controls` and `aria-activedescendant`; the list is a `listbox` of `option`s with `aria-selected`; each group is a `group` labelled by its heading.
- Keycaps are hidden; each option exposes its shortcut with `aria-keyshortcuts`. Announce the result count politely as it changes.
- Focus stays in the field. The caret and the highlighted row show where input goes, so the palette's own field draws no ring.
- Contrast: `text-on-accent` on `menu-hover` holds 4.5:1 (7:1 in `-hc`); context text uses `text-tertiary`.
- The consumer supplies every title, heading, hint and the empty sentence from the command registry and the product's copy.

## Platforms

| | SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|---|
| Command inventory | the menu bar (`CommandMenu`, `.commands`) | iPadOS menu bar; holding Cmd shows the shortcut list | app bar overflow and menus | `.nr-command-palette` |
| Palette | optional: an `NSPanel` with `.searchable` results | optional with a hardware keyboard | not used on phones; `SearchBar` on large screens with a keyboard | headless combobox in a `<dialog>` |

## Do and don't

- Do build it from the same registry entries (id, title, shortcut, enabled) as the menus.
- Do name commands as actions: a verb, or a verb and an object ("Pause watching").
- Do keep the Ask row last, so commands win ties.
- Don't list commands that cannot run, and don't dim them.
- Don't use the palette to change a setting without showing the result.

## Source

Intentional addition. trace-commons has no command palette; its search uses `GlassTextField` with Command-F, and the macOS menu bar holds the commands. NDS-14 defines one command registry rendered per platform, and HIG The menu bar, Designing for macOS and Keyboards say Windows, Linux and web lack a global menu, so the registry renders there as a command palette with `Mod+Key` shortcuts. Rows and highlight reuse `Menu`; the combobox pattern is WAI-ARIA.
