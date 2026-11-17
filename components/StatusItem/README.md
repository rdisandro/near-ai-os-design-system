# StatusItem

The status item is a macOS app's place in the menu bar: the Near AI N, a micro bar graph of the last 24 hours and a badge for decisions owed, in one image with nothing filled behind it. Clicking it opens the menu-bar panel (NDS-33).

## When to use

- An app whose job is ambient, such as Gateway watching folders and answering Private AI calls, that shows its state at a glance from the menu bar. On by default only for such apps, with a switch in Settings to remove it.
- One per app. It opens the menu-bar glass panel (see Desktop patterns); it is never the only way to reach anything.
- Not on Windows or Linux, whose tray icons stay a single-ink template image, and not on iOS, iPadOS, Android or the web.

## Anatomy

1. **Item** `.nr-status-item`: 22 tall (`space-20` + `space-2`), the parts `space-4` apart, no fill and no capsule behind them.
2. **Mark** `.nr-status-item__mark`: the N from the logo kit's own paths at 14 (`space-14`), in the menu bar's ink: white on a dark bar, black on a light one.
3. **Graph** `.nr-status-item__graph`: 17 by 17 (`space-16` + 1), the last 24 hours in six 4-hour steps. Each step is two touching 1pt bars, Private AI on the left and traces on the right, with 1 between steps; a 1pt center line divides up from down, leaving 8 of reach each way.
   - Private AI: verified calls up, all calls down.
   - Traces: shared up, kept down.
   - Private AI and traces are scaled separately; a step with any count is at least 1pt. Bars land on whole points so they stay crisp on a 1x display.
4. **Badge slot** `.nr-status-item__badge`: right after the graph, 11 tall (`space-10` + 1), a 7pt bold figure (`space-6` + 1), 2.5 inset, `badge-fill` with `text-on-status`. It caps at 99+ and is hidden at zero and when unknown (see `Badge`).
5. **Attention mark** `.nr-status-item__attention`: an 8 ring in the bar's ink, in the badge slot when something needs a look or the count is unknown.

## Sizes by density

| | compact (macOS) | regular, touch, dense |
|---|---|---|
| Item height | 22 | not used |
| Mark | 14 | |
| Graph | 17 × 17, six steps of two 1pt bars | |
| Badge | 11 tall, 7pt figure, 2.5 inset | |

## Variants

- **Live**: the mark, the graph and, when decisions are owed, the badge.
- **Paused** (`--paused`): watching is paused, so the trace bars draw in `neutral`; Private AI keeps its colors.
- **Attention**: the badge slot holds the attention mark (the product needs a look, or the count is unknown).
- **Unavailable**: the service is not answering. The graph draws its center line only, with no bars, and the attention mark shows; no badge.

The four series colors are Gateway's own product values, each measured at 3:1 on both bar appearances (dark / light): shared #b08bff / #7a2cf5, kept #6aa6ff / #2f6bc4, verified #30d158 / #1a8f4c, calls #ffb340 / #a97200. They are not parent roles. This page draws them with parent roles in the same places (`data-1` shared, `data-2` kept, `positive` verified, `caution` calls); a product that ships a status item supplies its own four values and measures them on both bars.

## States

| State | Treatment |
|---|---|
| Live, nothing owed | mark and graph, an empty badge slot |
| Decisions owed | the badge with the count, 99+ past 99 |
| Paused | trace bars `neutral`; the badge unchanged |
| Unknown Private AI data | no Private AI bars, never flat bars and never zeros |
| Unavailable | center line only, the attention mark, no badge |
| Menu open | the system's own highlight behind the item |

## Behavior

- The image is drawn for both menu-bar appearances and picked as it draws. It follows the menu bar, not the app: an app forced to Light still draws white on a dark bar.
- Clicking opens the menu-bar panel; the badge and the graph are not separate targets.
- The graph moves on with time and redraws in place, with no animation, and never pulses for attention. The badge changes in place with no motion.
- Never rely on it being visible: a notch or a crowded bar hides it. Every command it leads to also lives in the main window and the Dock menu.

## Accessibility

- The item has one accessibility label and help text from the product's copy source ("Near.ai, 3 decisions waiting"). VoiceOver reads the full count, never "99+".
- The graph is described in words in the label or help ("Watching paused"); its colors never carry meaning alone, and the panel it opens shows the same data with a legend.
- The ink follows the bar, so the mark holds contrast on both appearances; each series color holds 3:1 on both bars.
- **The product supplies**: the label and help text, the counts, the four series colors and its attention rule.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| `NSStatusItem` with a non-template image drawn per appearance (`GlassMenuBarStrip`) | Not available: widgets and Live Activities | Not available: a notification | Not available; the Windows and Linux shells use a single-ink template tray icon |

## Do and don't

- Do keep it to the mark, the graph and the badge.
- Do follow the menu bar's appearance, and draw nothing behind the parts.
- Don't draw unknown data as zero or as activity.
- Don't badge anything but decisions owed, and don't show a dash in the menu bar.
- Don't animate it to draw attention.

## Source

`GlassMenuBarStrip` in `macos/Sources/TCDesign/Components/MenuBarPanel.swift` (owner, 2026-10-21, #1539): the N mark at 14 on the left with 4 between, the graph on the right, the capsule fill and its `menuStripTint` removed; `menuItemMark` #ffffff / #000000; six 4-hour steps of two touching 1pt bars, 17pt wide, Private AI (verified up, calls down) and traces (shared up, kept down) scaled separately; `menuStripShared`, `menuStripKept`, `menuStripVerified`, `menuStripCalls`; the badge at 11pt with a 7pt figure and a 2.5 inset, capped at 99+, hidden at zero or unknown, with an attention mark; the graph's top rounded down so the center line stays crisp at 1x (review fix). The span is 24 hours because the Private AI record keeps 24 hours of calls.
