# Notice

A plate that tells people about the state of a whole section or window: a tone mark, a title, a short summary, an optional fix and a way to acknowledge it. On desktop it floats over the top of its tab and pushes nothing down (NDS-25); in compact web and phone layouts it sits inline above the content.

## When to use

- Health banners: the watcher stopped, a source is down, sign-in is needed, a grant expired.
- A section that failed to load, with Refresh.
- Offers and prompts that need a decision before the person goes on (turn on Private AI, a folder's rule changed).
- Pick the tier by scope:

| Scope | Component | Unity Foundations tier |
|---|---|---|
| One control or one request | `InlineAlert` | Help box |
| A section, pane or window | `Notice` | Help box (section) |
| The result of an action you can undo | `Toast` | Window banner |
| A decision that cannot be undone, or consent | `Modal` confirmation | Dialog |
| A record of operations | Activity log in `AgentRun` | Console |
| Anything while the app is in the background | System notification | |

## Anatomy

1. **Plate.** Popover (desktop default): `pane-opaque`, `radius-card`, padding `space-12`, `shadow-float`, the tab's full width under the tab bar. Inline (compact web, phone): `card-quiet`, `radius-card-quiet`, padding `space-10` x `space-12`.
2. **Tone coin** (popover). 30 across, leading: a `pane-opaque` disc with a 2px ring and the tone's glyph in the tone color (`caution`, `critical`, `neutral`, `positive`), or the tool's logo when a tool is the subject. Inline notices carry the tone as the title's `StatusLabel` dot instead.
3. **Title.** A full sentence in `body-strong` (popover) or the label step semibold in `text-secondary` (inline), with an optional `Tag` after it ("New"). The title states the problem or the offer.
4. **Summary.** Caption step in `text-secondary`: only what the decision needs, in one or two sentences. A consequence that a shared computer turns on stays here, never under Details.
5. **Details** (optional). An `Expander` labelled "Details" holding everything else. Nothing is removed; it moves behind the expander.
6. **Actions** (optional). One primary `Button` for the call to action, then links for Not now, Decline or Dismiss. `space-8` apart, `space-4` more above them.
7. **Close** (popover). A small X `IconButton` at the top trailing corner, named "Close", where the notice only acknowledges. It replaces a Dismiss link; Not now stays a link because it means something different.
8. **Refusal line** (optional). An `InlineAlert` inside the plate when the fix fails.

Parts stack with `space-6`. In a **stack**, popover notices sit with the newest in front and up to two earlier plates peeking `space-8` out behind it (three drawn), each scaled by 1 − 0.04 per level at 90% and 70% opacity. Inline notices sit `card-gap` apart, most severe first.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Placement | Popover over the tab | Popover at expanded and wider; inline below | Inline | Inline | Inline |
| Padding | 12 | 12 (popover), 10 x 12 (inline) | 12 x 16 | 12 x 16 | 8 x 10 |
| Radius | `radius-card` | `radius-card`, `radius-card-quiet` inline | `radius-card-quiet` | `radius-card-quiet` | `radius-control` |
| Title, summary | `mac-body-strong`, `mac-caption` | `web-body-strong`, `web-caption` | `ios-label`, `ios-caption` | `android-label`, `android-caption` | `mac-caption` |
| Buttons | 28 inline | 28 inline | 44 | 40 in a 48 target | 20 |

## Variants

| Tone | Mark | Use | Example title |
|---|---|---|---|
| Caution | `caution` | Something needs a look | The watcher isn't running. |
| Critical | `critical` | Something failed or was refused | History couldn't be read. |
| Neutral | `neutral` | Off, paused, informational, offers | Private AI is available on this Mac. |
| Positive | `positive` | A recovery worth saying, sparingly | Proofs are back for every call. |

- **Health banner.** No actions. It goes away when the condition clears.
- **Offer.** A primary action and a Not now link; the rest of the explanation under Details (Gateway's Private AI offer).
- **Dismissible.** An X (popover) or an acknowledge link (inline).
- **Gate.** No dismiss: the work behind it cannot continue until the person acts (sign in, choose Ask first).
- **Batch.** Repeats of one event collapse into one notice with a count ("3 traces arrived").

## States

- **Shown.** Popover: slides in from the top on `spring-spatial` while any stack holds still; nothing below moves. Inline: appears in place and pushes the content down, with no motion. Under Reduce Motion both appear at once.
- **Acting.** The primary `Button` shows its busy state ("Restarting…"); the notice stays.
- **Fix failed.** The refusal line with the new reason.
- **Resolved.** The notice leaves when the product reports the condition gone. Never on a timer.
- **Increased contrast.** The plate gets the 1px `edge-hc` inset edge.

## Behavior

- Never auto-dismiss. A notice leaves when its condition clears or the person acknowledges it.
- Keep each notice to one condition and say each thing once. Merge repeats into a batch instead of stacking copies.
- Anchor: a stack at a tab's top flows down; a stack at a map's foot flows up. On macOS 26 the plates never merge into one glass group.
- Keyboard: the notice is a region in reading order; Tab reaches its actions and the X. Escape closes the front popover notice when it can be acknowledged. After it closes, focus moves to the next notice, or to the tab's heading when none remain.
- Never present a notice as an alert at launch. Show the held data with the notice over it.

## Accessibility

- Mark it up as a region named by its title (`<section aria-labelledby>`). When it appears while the person is on the page, announce it once in a polite live region; use `role="alert"` only for a gate that stops the work in front of them.
- The title's words carry the tone ("isn't running", "couldn't be read"). The coin or dot is supplementary and hidden from assistive tech.
- The consumer supplies the title, summary, details, Tag, action and Close words from the product's copy.
- Contrast: `text-primary` and `text-secondary` on `pane-opaque` and on `card-quiet` hold 4.5:1 over the worst ground (7:1 in the `-hc` themes); the coin's ring is a 3:1 mark.
- Action targets follow the density's floor.

## Platforms

| | SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|---|
| Build | `GlassPopoverNotice` and its stack over the tab; `GlassNotice` for inline | Custom card at the top of the scroll view or as a `List` section | Custom `Card` with a dot `Row` title (M3 has no banner) | `<section class="nr-notice nr-notice--popover">`, or `.nr-notice` inline |
| Announce | `AccessibilityNotification.Announcement` | `UIAccessibility.post(.announcement)` | `liveRegion = LiveRegionMode.Polite` | `role="status"` region |
| Native? | No | No; never `.alert` for status | No | No |

## Do and don't

- Do write the title as the problem in a sentence, then the cause, then what to do (Problem, cause, solution).
- Do state what happened to the person's data ("nothing was sent", "traces stay on this Mac").
- Do make the call to action primary and every decline a link (NDS-25).
- Don't prefix "Error" or "Warning"; the mark already says it.
- Don't tint the plate by tone, color the body or add a colored left border.
- Don't put a consequence under Details, or use a modal for a status that needs no decision.

## Source

`GlassPopoverNotice` and its stack in `TCDesign/Components/PopoverNotice.swift` (opaque `paneOpaque` plate at `Radius.card`, padding `s6` 12, 30pt coin with a 2pt tone ring, peek 8, three drawn; owner, 2026-10-19, #1481); notice calls to action made primary (owner, 2026-11-02, #1888); the Private AI offer's Details fold (2026-11-02). The inline form is `GlassNotice` in `Components/Containers.swift`. The scope tiers and the Problem, cause, solution formula come from Unity Foundations' errors and messaging; alerts only for decisions, never at launch, from the HIG alerts and feedback pages.
