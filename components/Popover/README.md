# Popover

A small floating panel anchored to the control that opened it, for a few related details or one quick task, which closes on an outside click or Esc.

## When to use

- Show details on demand: a row's longer text behind an info glyph, a node card on the trace graph, a model's details.
- Hold one quick task beside its control: a single setting, a short choice.
- Use a `Tooltip` for a name or a shortcut only, a `Menu` for a list of commands, and a `Modal` or `InlineAlert` for warnings.
- On compact widths (phones), use a `Sheet` instead (HIG: no popovers in compact width).
- Show one popover at a time; never open one from another.

## Anatomy

1. Container: `popover` fill over `blur-floating`, `radius-card` (16), `shadow-float`, padding `space-10`, `space-6` between parts. Width fits the content up to `size-popover-width` (260); `--fixed` holds it at 260 so text wraps evenly.
2. Title (optional): body-strong type, `text-primary`.
3. Text: caption or body type in `text-secondary`.
4. Actions (optional): inline `Button`s, trailing, `space-8` apart, `space-4` above.
5. Offset: `space-8` from the source, centred on it (`.nr-popover-anchor`) or start-aligned near a window edge (`--start`). Web and Android draw no arrow; Apple system popovers draw their own.
6. Info glyph (`.nr-popover__info`): a 12px (`space-12`) circled "i" in `text-tertiary`, with a hit area of `--nr-target`. Pinned, the disc fills.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Width | up to 260 | up to 260 | iPad regular width only; a `Sheet` in compact | none in M3; a `Sheet` or a persistent rich tooltip | up to 260 |
| Text | `mac-caption` | `web-caption` or `web-body` | system | | `web-caption` |
| Info glyph hit area | 28 | 28 | 44 | 48 | 20 |

## Variants

- **Info popover**: opened from the info glyph after a row's title. Hover shows it; a click or Space pins it until an outside click or Esc.
- **Node card**: a title, a line of facts and one action ("Step 6 · web search", Look inside).
- **Quick setting**: one or two controls; changes apply at once and are kept when it closes.

## States

| State | Rule |
|---|---|
| Shown on hover | Info popover only, after the tooltip delay; leaves when the pointer leaves both the glyph and the popover. |
| Pinned | `aria-expanded="true"` on the glyph; the glyph turns `text-primary` and its disc fills. |
| Dismissed | Outside click, Esc, or picking an action. |
| Increased contrast | 1px `edge-hc` inset edge. Reduced transparency: `pane-opaque`, no blur. |

## Behavior

- Anchored to its source and flipped or shifted to stay inside the window; it never covers its source.
- It is nonmodal: Tab moves from the source into the popover and on; Esc closes it and returns focus to the source.
- Edits in a quick-setting popover are saved when it closes; only an explicit Cancel discards them (HIG).
- Entry is a fade on `duration-standard` with `ease-standard`; Apple system popovers grow from their source. Under Reduce Motion it appears at once.
- On the web, use the `popover` attribute so it sits in the top layer, and anchor positioning or a positioning library to place it.

## Accessibility

- The container is a nonmodal `dialog` labelled by its title or by its source.
- The info glyph is a button named by the product ("More about trace text"). The same text is the glyph's description (`aria-describedby`, or SwiftUI `accessibilityValue`), so screen reader users get it without opening the popover.
- Text uses `text-secondary` on `popover`, measured over the worst ground behind the blur.
- The consumer supplies every word: title, text, action labels and the glyph's name.

## Platforms

| | SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|---|
| Info popover | `GlassInfoButton(label, text:)`: a system `.popover`, 260 wide | `.popover` on iPad; adapts to a sheet in compact width | `TooltipBox` with a persistent `RichTooltip` | `.nr-popover__info` + `.nr-popover--fixed` |
| Custom popover | `GlassPopover(onDismiss:)` painted on the floating layer | `.popover(isPresented:)` | `Popup` with parent styling | `.nr-popover` in `.nr-popover-anchor` |

## Do and don't

- Do keep it small: a few lines and at most one or two actions.
- Do keep the text reachable without hover (the glyph's description).
- Don't put a warning or a required decision in a popover.
- Don't cascade popovers, and don't open one over a `Menu`.
- Don't say "popover" in copy or help.

## Source

`GlassPopover` in `macos/Sources/TCDesign/Components/Surfaces.swift` (popover tier, 10pt padding, floating, Esc dismisses, one container for VoiceOver) and `GlassInfoButton` in `InfoButton.swift` (owner, 2026-10-08: hover shows, click pins, 260 wide, label then text read as the value). Placement, single-popover and autosave rules come from HIG Popovers; flipping and outside-click dismissal from Unity App UI's Popover; M3 rich tooltips map here.
