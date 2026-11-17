# Card

A painted container on a pane that holds one topic: a head (icon or eyebrow, title, sub-lines, accessory), optional content and, when the whole card leads somewhere, a chevron.

## When to use

- Group the facts and controls about one thing inside a pane: an account, a model, a mission, an agent run.
- Make the whole card interactive when it opens something (History, Missions). It then holds no other controls.
- Use the quiet card for inspector sections, notices and menus inside a panel.
- Prefer spacing, a `KeyValueList` or a `DataTable` when a card would only add a box around content.
- Cards are the content layer: painted, never blurred, never on glass inside glass (NDS-9). Only a nested card, a quiet card, a well or a `CodeBlock` sits inside a card.
- For a surface that explains how it starts, use `GetStartedCard` (NDS-39).

## Anatomy

1. **Container**: `card` fill, `radius-card` 16, padding `card-padding-y` 12 by `card-padding-x` 14. Quiet: `card-quiet`, `radius-card-quiet` 14, padding 10 by 12. Flush: no padding, for `DataTable` rows.
2. **Icon** (icon card): a 22 glyph (`size-tool-tile`) centred in a 26 column (`size-tool-tile` + `space-4`), `text-secondary`. Its drawn top meets the title's cap height; on web it sits `space-2` below the title's line box. A title-only icon card (no sub-line, no content) centers its title on the icon instead (owner, 2026-11-02).
3. **Eyebrow** (eyebrow card): eyebrow step, uppercase, `text-tertiary`, `space-6` above the title.
4. **Title**: body-strong in an icon card, title step in an eyebrow card, `text-primary`, exposed as a heading.
5. **Sub-lines**: caption step, `text-secondary`, `space-2` apart. Empty lines are left out.
6. **Info glyph**: 12, `text-tertiary`, set after the last word of the last sub-line and kept on its line. Hover shows the fine print; a click pins it in a `Popover` (`size-popover-width` 260).
7. **Accessory**: a tag, the Refresh pill (NDS-36), a small primary Sign in while the card waits on sign-in, or a short caption on the right, centred on the head. A dismissible card puts its close X here instead: a bare 12 glyph in a 20 frame, `text-secondary`, `text-primary` on hover, named "Dismiss" or "Close" by the product.
8. **Content**: `space-8` under the head. In an icon card it aligns with the title (36 in: icon column + `space-10`). Body text sits `space-10` further in than the title and actions; a nested container aligns with the title, and text inside it gets `space-8` more on each side. A quiet card resets the rule.
10. **Nested card** (optional): `card-nested` at `radius-card-quiet`, padding `space-4` by `space-6` or more, holding one detail inside the card (Gateway's "You could make…" estimate beside the Not contributed counts). One level only.
11. **Watermark** (optional, small cards and stat tiles): the card's glyph at 58, rotated −12°, at 55%, bleeding 12 by 14 off the trailing bottom corner, clipped by the card and drawn behind the words in `accent-soft` (Gateway's Home tiles). Decoration only; hidden from assistive tech.
9. **Chevron**: 10, `text-tertiary`, centred on the whole card, `space-12` from the content.

A collection uses `.nr-card-grid`: columns at least 256 wide (4 x `space-64`), `card-gap` 10 apart; `.nr-card--wide` spans the row.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Padding | 12 / 14 | 12 / 14 | 12 / 14 | 12 / 16 | no card: group with spacing or an `Expander` |
| Title (icon card) | `mac-body-strong` | `web-body-strong` | `ios-body-strong` | `android-body-strong` | - |
| Title (eyebrow card) | `mac-title` | `web-title` | `ios-title` | `android-title` | - |
| Sub-line | `mac-caption` | `web-caption` | `ios-caption` | `android-caption` | - |
| Icon / column | 22 / 26 | 22 / 26 | 22 / 26 | 22 / 26 | - |
| Interactive target | whole card | whole card | whole card, at least 44 tall | whole card, at least 48 tall | - |

Radius stays `radius-card` everywhere; on a phone a card that meets the screen edge keeps the `margin-compact` 16 gutter.

## Variants

- **Card**, **quiet card**, **flush card** (tables).
- **Interactive**: the card is one `<a>` or `<button>` (`.nr-card--interactive`), with a chevron when it is a way into somewhere (`.nr-card--chevron`).
- **Icon card**: the house head (`.nr-card__head--icon`). Use it for Home-style cards and account cards.
- **Eyebrow card**: eyebrow over an optional title, accessory top right.
- **Dismissible**: a close X in the accessory slot; closing is remembered for the product's stated scope (Gateway: for good on this Mac).
- **Promotion** (`.nr-card--promo`): the card fill under a one-hue `accent-tint` wash, a soft spotlight at the top leading corner, a thin `accent-tint` inner rule, and the icon in `accent-text`. The default treatment is spotlight; the product may move the light with the pointer by setting `--nr-promo-x` and `--nr-promo-y`. `.nr-card--promo-tint` is the still tint alone. Aurora, shimmer and glow border are Classic product treatments, not parent defaults; Gateway removed its card shimmer (owner, 2026-11-02; NDS-40). One promotion per screen.
- **Gateway's hero promotions** (current state, not a parent rule): Home's Campaign, Missions and Insights cards draw two-stop gradients at 120° (#0057b0 to #0091fd, #06264a to #035ca3, #073b55 to #1f7aa8) with white ink, a white pill button and a graphic bleeding off the trailing and bottom edges. They break "one promotion per screen" and "no two-hue gradient", and stay a product exception until the owner rules.

## States

| State | Treatment |
|---|---|
| Default | `card` (quiet: `card-quiet`) |
| Hover (interactive only) | `card-hover` replaces the fill on `duration-fast` `ease-standard`. A promotion deepens its spotlight instead, never a white wash. |
| Pressed | `brightness(0.92)` on the fill, never a fade |
| Focus | 2px `focus-ring`, 2px outside, keyboard only |
| Disabled (interactive) | whole card at `opacity-disabled`, no hover; the sub-line says why |
| Loading | the head stays; the sub-line carries the product's loading line; held data is never replaced by a skeleton |
| Unknown | figures read "—" or the product's unknown word, never zero |
| Increased contrast | 1px `edge-hc` inset edge (the promotion's accent rule gives way to it) |

## Behavior

- An interactive card is one tab stop; Return or Space opens it. It contains no buttons, switches or links, so there is never an action on an actionable surface.
- A static card is not a tab stop; its own controls are, in reading order.
- The info glyph opens on hover, pins on click or Return, and closes on Esc or a click outside.
- Fills fade on `duration-fast`; nothing moves, lifts or casts a shadow on hover. Under Reduce Motion the promotion's light holds still at its corner.
- Touch: the whole card is the target; the pressed fill shows on touch-down; there is no hover.

## Accessibility

- The title is a heading at the level the screen's outline needs. An interactive card's name is its title; its first sub-line is its description.
- Icon and chevron are decorative and hidden. The info glyph has its own name from the product, never the card's title.
- Text tokens hold 4.5:1 on `card` and `card-quiet` over the worst ground (contrast report). The promotion tint sits under the words, so the same text tokens apply.
- The consumer supplies every word: eyebrow, title, sub-lines, info text, accessory. The component authors none.
- Turning the focus ring off with `.nr-focus-off` (Gateway does) fails WCAG 2.4.7.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| Custom: `GlassCard`, `GlassIconCard`, `GlassEyebrowCard`, `GlassPromoCard` on a continuous `RoundedRectangle`; interactive cards sit in a `Button` with the press style | The same views on the opaque screen pane; settings-like content uses an inset grouped `List` section instead | Filled `Card` with `containerColor` = `card`, 16dp shape, no elevation; the `onClick` overload for interactive cards | `<article class="nr-card">`; `<a>` or `<button class="nr-card nr-card--interactive">`; `.nr-card-grid` for collections |

## Do and don't

- Do give an interactive card one destination. Don't put buttons inside it.
- Do use a quiet card for a secondary section, and `card-nested` for one detail inside a card (NDS-38). Don't nest deeper than that.
- Do carry status as a dot and words in the accessory. Don't tint a card by status or give it a colored side border.
- Do keep one promotion per screen. Don't use the promotion for warnings or decoration, and don't use a two-hue gradient.
- Don't use a chevron to unfold content in place; a chevron means the card goes somewhere.

## Source

`GlassCard`, `GlassIconCard` (`centersTitle`, owner 2026-11-02), `GlassEyebrowCard`, `GlassChevron` in Containers.swift; `cardNested` (owner, 2026-10-22, #1585); the watermark from Home's stat tiles (#1460); the hero cards in HeroCard.swift (#1745); `GlassPromoCard` and `GlassPromoTreatment` in Styling/GlassPromo.swift; the adaptive card grid in Gallery/GlassGallery.swift. Interaction model from M3 cards (actionable or container, never both).
