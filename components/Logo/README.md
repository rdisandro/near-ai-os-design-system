# Logo

The Near AI master-brand lockups from the logo kit, placed on the right ground for the theme, plus the kit's "N" on its own.

## When to use
Use the primary wordmark wherever Near AI introduces itself: the web app header, sign-in, about and settings screens, onboarding, marketing. Use the secondary lockup when the wordmark does not fit (headers under 600px, compact toolbars). Use the tile only where an app icon would appear.

The wordmark leads product headers too (NDS-27): the menu-bar popover header, a chat's masthead, a marketing header. A product name sits beside it as a typeset lockup ("Gateway"), never in its place.

Use the N alone (NDS-26) as a product mark: beside the wordmark in a masthead, on a chat's welcome, as first run's hub, as the edge rail's app tile, and in the menu bar.

## Anatomy
1. Lockup image: an uploaded SVG asset from the kit. Where a mark must animate or take the menu bar's ink, render the kit's own path data in code (`GlassNearWordmark`, `GlassBrandMarkDrawing`); never change the paths.
2. Clear space: the margin drawn in the kit's clear-space files, about one fifth of the lockup's height on every side.
3. Ground: `brand-paper`, a light pane, or any light theme ground for the color lockup; `brand-ink`, a dark pane, or any dark theme ground for the white-and-color lockup.
4. **Product lockup** (optional): a 1px divider in `rule` (slate on the marketing void), then the product name typeset in the product's display face at the height of the wordmark's "AI", one space of clear space either side of the divider.

## Sizes by density
| Context | Primary (730 by 138) | Secondary (291 by 136) | Tile (400 by 396) | N alone |
|---|---|---|---|---|
| Web header (regular) | 24px tall | 24px tall | n/a | |
| Chat masthead (regular) | 18px tall | | | 22, before the wordmark, 8 apart |
| Menu-bar popover header (compact) | 16pt tall, about 85 wide | | | |
| Menu bar status item | | | | 14pt, the menu bar's ink |
| Marketing header | 17px tall, with the product name | | | |
| Desktop about window (compact) | 28px tall | 28px tall | 64px | |
| Phone header (touch) | 20px tall | 24px tall | n/a | |
| Sign-in and onboarding hero | 40 to 56px tall | 48px tall | 96px | Chat welcome 80 (64 on phones) |
| Thinking mark | | | | 16 |

The kit sets no minimum size; ask the brand owner before going below 72px wide for the wordmark. The 16pt panel header is above that.

## Variants
- `color`: light grounds. `white-color`: dark grounds. Theme switching picks between them (`.nr-logo--for-light`, `.nr-logo--for-dark`).
- `black` and `white`: single ink, for one-color contexts only, and the menu bar.
- `tile` (a `brand-tile` tile with a `brand-paper` "N") and `tile-white-color` (a white tile with a `brand-tile` "N"): app-icon contexts.
- **N alone**: the kit's "N" without its tile, in `brand-blue` on any ground (`#0070c6` is allowed on light pages, as Gateway's first run draws it), or in the menu bar's single ink.

## States
None. A logo is never a button by itself; when it links home, the link's focus ring (`focus-ring`) draws around the clear-space box.

## Behavior
The wordmark never moves. The N moves only at the moments NDS-26 names, each with a Reduce Motion end state (see Motion):
- **Drawn on**: a marker stroke inks the N along its center line from inside the lower-left hook, 1 s, with a pen-tip dot at the stroke's front (first-run Welcome, a chat's welcome).
- **Shine**: one soft band crosses the N about 1.5 s after the Welcome opens, then every 15 s.
- **Thinking**: the N turns and beats while a light chases its stroke, only while a reply is being worked on.
- **Hub**: on first run the N is a shared actor that moves between steps and finally flies toward the menu bar.

No lockup takes a glass effect. An app icon gets the system's glass from Icon Composer; that is the icon, not the mark.

## Accessibility
`alt="Near AI"` on the image; when the logo is a home link, the link's accessible name is "Near AI, home" (with a product lockup, "Near AI Gateway, home"). Decorative repeats (a footer under a header that already names Near AI, the N on a welcome, the thinking mark) take `alt=""` or are hidden from assistive tech; the words around them carry the meaning.

## Platforms
| macOS (SwiftUI/AppKit) | iOS/iPadOS | Android (Compose) | Web |
|---|---|---|---|
| Asset catalog SVG (single-scale, preserve vector data), `Image("near-ai-primary-color")` with a dark appearance variant; `GlassNearWordmark` and `GlassBrandMarkDrawing` where the mark draws from path data | Same asset catalog | Vector drawable converted from the SVG, `painterResource` with a `-night` variant | `<img src>` of the uploaded asset; swap by theme with `.nr-logo--for-light` / `.nr-logo--for-dark`; inline SVG from the kit's paths only where it animates |

## Do and don't
- Do keep the kit's clear space on every side.
- Do use the white-and-color lockup on glass panes in the dark themes.
- Do lead a product header with the wordmark and set the product's name beside it.
- Don't recolor the wordmark with a product accent (Gateway purple included).
- Don't set "Near AI" in type to imitate the wordmark.
- Don't place a lockup over busy scene glows without a pane behind it.
- Don't animate the N anywhere NDS-26 does not name, or loop its motion behind text people are reading.

## Source
Intentional addition: the Near AI logo kit (Primary, Secondary, Tertiary, with clear-space guides), supplied by the owner (decision NDS-8). trace-commons first used the "N" as a map texture (`GlassBrandMark`); since 2026-10-21 it also draws the N in the menu bar, on first run (`GlassBrandMarkDrawing`) and the wordmark in the popover header (`GlassNearWordmark`). The Near AI chat (nearai/LibreChat PR #5) adds the masthead lockup, the welcome draw-on and the thinking mark.
