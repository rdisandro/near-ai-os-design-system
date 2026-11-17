# Menu

A floating list of commands or choices opened from a button, a kebab, a split button or a secondary click, which closes when the person picks an item, presses Esc or clicks elsewhere.

## When to use

- Use it for three or more actions related to one control or object: a row's kebab, a toolbar's view options, a context menu.
- Use checkable items for a choice the person makes now and rarely revisits, such as a folder's mode (Ask, Automatic, Never).
- Offer a context menu on every object on desktop, and give every item a home in the menu bar or `CommandPalette` too (NDS-14).
- Use a `Toolbar` for actions people need all the time, and `RadioGroup` or `SegmentedControl` for a choice that should stay visible.
- On compact phone widths, put long action lists in a `Sheet` (M3 breakpoints).

## Anatomy

1. Container: `menu` fill (94%, so rows and pills under it never show through; NDS-24) over `blur-floating`, `radius-card-quiet` (14), `shadow-float`, padding `space-8`. Width at least `size-menu-min-width` (220), at most `size-panel-width` (380).
2. Item: height `--nr-h-control`, padding `space-10`, gap `space-8`, `radius-tile` (14 − 8 = 6, concentric).
3. Check column: `space-12` wide, present on every item of a checkable menu so labels align.
4. Label: body type, one line, ellipsis when long.
5. Trailing: a shortcut or a submenu chevron in `text-tertiary`, at least `space-16` after the label.
6. Section heading (optional): eyebrow type, `text-tertiary`.
7. Separator: 1px `rule`, inset `space-10`, `space-4` above and below.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Item height | 28, `mac-body` | 28, `web-body` | system menu (44) | 48 baseline, 44 vertical menu | 20, `web-label` |
| Container radius | 14 | 14 | system | 16 (M3 vertical) | 14 |
| Glyphs | `size-glyph` | `size-glyph` | SF Symbols | 20dp | `size-glyph` |

## Variants

- **Floating** (default): on the floating layer, anchored to its trigger with `.nr-menu-anchor`.
- **Inline** (`--inline`): rows drawn inside a pane with no fill, blur or shadow; the menu-bar panel's rows.
- **Checkable items**: `menuitemradio` or `menuitemcheckbox` with a check glyph when `aria-checked="true"`.
- **Destructive item** (`--destructive`): `destructive-text`, last, after a separator, and it opens a confirmation.
- **Submenu item**: a trailing chevron; one level only, about five items at most.

## States

| State | Rule |
|---|---|
| Highlighted (hover or keyboard) | `menu-hover` fill with `text-on-accent`; trailing text takes the same ink. In a menu the highlight is the focus indicator, so items draw no ring. |
| Pressed | `accent-pressed` fill. |
| Checked | Check glyph in the check column, `aria-checked="true"`. |
| Disabled | `opacity-disabled`, never highlighted. Menu-bar menus dim unavailable items; context menus and row menus hide them (HIG, NDS-41). |
| Increased contrast | 1px `edge-hc` inset edge on the container. |
| Reduced transparency | On web, Windows, Linux and Android the container turns `pane-opaque` with no blur; on Apple platforms the system applies it (NDS-23). |

## Behavior

- Opens `space-4` below its trigger with trailing edges aligned, and flips above or shifts sideways to stay in the window. A context menu opens at the pointer.
- A menu is never clipped by the card or list it was opened from. Draw it at the nearest ancestor that does not clip (the inspector column, the window), still trailing-aligned with its trigger and never past that ancestor's leading edge. When the trigger is the last thing in a scroll view, add room under it while the menu is open and scroll just far enough to show the menu (`duration-fast`), rather than flipping it over the content above.
- Opened by keyboard, focus lands on the first item. Up and Down move (wrapping), Home and End jump, letters jump to the next matching item, Right opens a submenu, Left closes it, Return or Space activates, Esc closes and returns focus to the trigger.
- Picking an item closes the menu; a multi-select menu stays open.
- Entry is a fade on `duration-standard` with `ease-standard`. On Apple platforms the system menu grows from its button. Under Reduce Motion it appears at once.
- On the web, put the menu in the top layer with the `popover` attribute.

## Accessibility

- Roles: `menu` on the container, `menuitem`, `menuitemradio` or `menuitemcheckbox` on items; the trigger has `aria-haspopup="menu"` and `aria-expanded`, and the menu is labelled by it.
- Headings are presentational text; separators are hidden; glyphs beside labels are decorative.
- The consumer supplies labels, headings and shortcut strings from the command registry (NDS-14). Shortcuts are written `Mod+Key` and rendered per platform: ⌘ glyphs in ⌃⌥⇧⌘ order on Apple, "Ctrl+Shift+C" elsewhere.
- Contrast: `text-on-accent` on `menu-hover` over `menu` measures 5.91:1 light, 7.66:1 dark, 7.46:1 Gateway dark, 7.17:1 light-hc. `destructive-text` holds 7:1 on `menu` in the `-hc` themes.
- Touch items are at least 44pt (Apple) or 48dp (Android); never place two actions in one item.

## Platforms

| | SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|---|
| Menu bar, context menu | native `NSMenu` / `.contextMenu` | `.contextMenu`, `UIMenu` | long-press `DropdownMenu` | `.nr-menu` on `contextmenu` |
| Pull-down from a control | native `Menu`; `GlassMenu` + `GlassMenuItem` when painted on the floating layer | `Menu` (Liquid Glass, morphs from its button) | `DropdownMenu` + `DropdownMenuItem` | `.nr-menu` in `.nr-menu-anchor` |
| Panel rows | `GlassMenuRowStyle` | list rows | list items | `.nr-menu--inline` |

## Do and don't

- Do put frequent items first and keep to about three groups.
- Do give icons to every item in a group or to none.
- Do add "…" to an item that needs more input ("Withdraw contributions…").
- Don't show keyboard shortcuts in context menus (HIG); show them in pull-down menus and the menu bar.
- Don't hide all of a view's actions in one menu.
- Don't nest buttons, switches or fields inside an item.
- Don't let a card's clipping cut a menu off; a menu always floats over everything around its trigger.
- Don't draw two check marks in a checkable menu; on macOS use toggles, not an inline picker inside a menu.

## Source

`GlassMenu`, `GlassMenuItem`, `GlassMenuSeparator` and `GlassMenuRowStyle` in `macos/Sources/TCDesign/Components/Surfaces.swift`: a custom-painted floating menu, minimum width 220, hover in the menu selection color with light text, a checkable item with a leading check, Esc to dismiss. The parent raises the container inset from 5 to `space-8` so item corners stay concentric at `radius-tile`, and sizes items from the density row. Opaque floating fills: owner, 2026-10-05 (web shell) and 2026-10-19 (the "…" menu and the Submit dropdown). Unclipped menus from inside a card: owner, 2026-10-29 (#1902). Headings, trailing shortcuts, submenus and the touch sizes come from HIG Menus and Context menus and M3 vertical menus.
