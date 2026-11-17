# Badge

A small red count of decisions a person owes, placed on the tab, menu-bar item or app icon that leads to them; it reads 99+ past the cap and a dash when the count is unknown.

## When to use

- Only for decisions owed: traces waiting to be submitted, approvals an agent is blocked on, consent a run needs.
- Never for queue depth, credit, totals, unread news or promotion. Those are values in the content.
- Zero draws nothing.
- Use a `StatusLabel` dot (with words in the host's accessible value) for attention without a count. There is no dot-only badge.

## Anatomy

1. **Container.** A capsule (`radius-pill`) in `badge-fill`, height 16 (`space-16`), minimum width 16, horizontal padding `space-4`.
2. **Count.** The micro step in `text-on-status`, tabular numerals.
3. **Placement.** Inline after the host's label, `space-4` to `space-8` from it; or anchored over a glyph's top trailing corner, offset `space-4` up and `space-6` past the edge.

The **subtle** badge is 14 tall (`space-14`) on `toggle-off` (the 16% ink) and takes its host's ink. It sits inside a tab or segment where a red pill would shout.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Height, min width | 16 | 16 | System (`.badge`) or 16 | 16 (M3 large badge) | 14 (subtle) |
| Padding | 0 x 4 | 0 x 4 | 0 x 4 | 0 x 4 | 0 x 4 |
| Count | `mac-micro` | `web-micro` | `ios-micro` | `android-micro` | `mac-micro` |
| Max characters | 3 (`99+`) | 3 | 3 | 3 | 3 |

## Variants

- **Count.** Red pill on a tab title, a rail item or a menu-bar item.
- **Subtle.** The 16% ink pill inside a segment or a selected tab.
- **Anchored.** Over a glyph (a toolbar icon). The host is the glyph's container (`nr-badge__host`).
- **Status item** (macOS menu bar, NDS-33). Drawn inside the `StatusItem` image, after its graph: 11 tall with a 7pt figure and a 2.5 inset, matched to other menu-bar apps. Hidden at zero **and when unknown**: the status item draws its attention mark instead, because a dash in the menu bar reads as a glyph, not a count.

## States

| Count | Draws | Read as (from product copy) |
|---|---|---|
| 0 | Nothing | Nothing (the host reads its name) |
| 1 to 99 | The number | "3 decisions waiting" |
| Over 99 | `99+` | "More than 99 decisions waiting" |
| Unknown | `—` in the same pill (in the status item: no badge, the attention mark) | "Decisions waiting: unavailable" |

- An unknown count keeps the pill so the surface never reads as "nothing owed" when the product cannot tell. It never shows 0. The status item is the one exception: it hides the badge and shows its attention mark, which says the same thing.
- A failed refresh keeps the last count only while the product still considers it fresh; after that it draws the dash.
- Under the `-hc` themes `badge-fill` darkens and the count turns white (`text-on-status` changes with it).
- Not interactive: no hover, pressed or focus. The host owns those.

## Behavior

- The count changes in place with no motion: no bounce, pop or pulse, on any setting.
- The badge clears when the decisions are made, not when the person opens the tab. Owed decisions are not "unread".
- Keep the badge's position fixed as the count grows; it widens toward the trailing edge.
- Mirror the anchored offset in right-to-left layouts.

## Accessibility

- The host carries the name and the count: "Traces, 3 decisions waiting". On web, hide the badge (`aria-hidden`) and give the host visually hidden text or an `aria-label`; on Apple platforms set the host's `accessibilityValue`; in Compose set `contentDescription` on the `Badge`.
- The consumer supplies every word, including the unknown word. The number never stands alone.
- Contrast: `text-on-status` on `badge-fill` holds 4.86:1 in light and 7.04:1 in dark; the fill holds 3:1 against the grounds it sits on.
- A badge is not a target and never shrinks its host's target.

## Platforms

| | SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|---|
| In tabs and segments | Custom `GlassBadge` | `.badge(n)` on `TabView` items (native, system red) | `BadgedBox { Badge(containerColor, contentColor) { Text("3") } }` | `<span class="nr-badge">` |
| On toolbar items | `.badge(n)` on toolbar items (macOS 26), `NSItemBadge.count` in AppKit | `.badge(n)` | `BadgedBox` on the `IconButton` | `.nr-badge--anchored` |
| App icon, menu bar | `NSDockTile.badgeLabel`; the status item draws its own count at 11 (`GlassMenuBarStrip`) | `setBadgeCount` | Launcher badge from the notification channel | Not used |
| Native? | Native on Dock and toolbars, custom in tabs | Native | Native | Custom |

## Do and don't

- Do count only what needs the person's decision.
- Do pair the badge with words in the host's accessible name.
- Don't show 0, and don't show a number while the count is unknown.
- Don't badge more than one destination for the same decisions.
- Don't use a badge for marketing, tips or new features.
- Don't add a second color or a glyph to the badge.

## Source

`GlassBadge` in `Components/Indicators.swift` (decisions owed; `badgeFill` with `textOnStatus`; 16 minimum or 14 subtle; cap 99 then `99+`; nil draws a dash; VoiceOver reads the caller's label) and the segment badge rules in `Components/Navigation.swift` ("Never queue depth or credit", `.count(0)` draws none, `.unknown` draws a dash). M3 badges (16dp large badge, 4dp padding, at most four characters) set the Android fit; the HIG `.badge` modifier is the native iOS path. The status-item badge (11 tall, 7pt figure, 2.5 inset, hidden at zero or unknown with an attention mark) is `GlassMenuBarStrip` in `Components/MenuBarPanel.swift` (owner, 2026-10-21, #1539).
