# GetStartedCard

The one card for every surface that explains how it starts (NDS-39): a title, an optional lead line, numbered steps of a title over one line, and at most one action. It takes the place of the content it explains while that content is empty, and sample data shown under it sits behind a banner.

## When to use

- A surface that has not started yet and needs a few steps from the person: Insights before any traces, the Private AI tab before a tool is connected, Home's Traces section before a folder is watched.
- One per surface, in place of the content it explains. When that content arrives, the content takes the card's place.
- Not for an empty result ("Nothing is waiting."): use `EmptyState`. Not for an offer that needs a decision now: use `Notice`. Not for a promotion: use the `Card` promotion.

## Anatomy

1. **Card.** `card` fill, `radius-card`, padding `card-padding-y` 12 by `card-padding-x` 14. No icon, no graphic, no gradient.
2. **Title.** The title step (15 semibold on macOS), `text-primary`, exposed as a heading. It starts at the card's leading edge.
3. **Lead line** (optional). Label step, regular, `text-secondary`, `space-4` under the title. One sentence.
4. **Close** (optional). A bare 12 X in a 20 frame at the head's trailing end, `space-8` from the title: `text-secondary`, `text-primary` on hover, named by the product's "Close".
5. **Steps.** Inset `space-10` on both sides, `space-20` apart and `space-20` below the head:
   - a number in an 18 disc: micro step, tabular digits, `accent-text` on `accent-tint`, `space-10` before the text;
   - the step title: label step, semibold, `text-primary`;
   - the step line: label step, regular, `text-secondary`, `space-2` under the title, with the info glyph after its last word when the step has more to say;
   - an optional link: the step's one action as a text link that names its destination ("Open Traces"), then a right arrow glyph, `accent-text`, `space-6` above it.
6. **Sample banner** (with sample content). `caution-tint`, no border, `radius-control`, padding `space-8` by `space-12`: a 14 sample glyph (`testtube.2`) in `caution-text`, the title "Sample data shown below" in label semibold, the line "Your own data will replace it once trace activity is provided." in caption. The sample under it is drawn at 0.55, takes no input and is hidden from assistive tech.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Padding | 12 / 14 | 12 / 14 | 12 / 14 | 12 / 16 | not used |
| Title | `mac-title` | `web-title` | `ios-title` | `android-title` | |
| Step title, line | `mac-label` | `web-label` | `ios-label` | `android-label` | |
| Number | `mac-micro` in 18 | `web-micro` in 18 | `ios-micro` in 22 | `android-micro` in 22 | |
| Close | 20 frame, 28 hit area | 20 frame, 28 hit area | 44 hit area | 48 hit area | |

## Variants

- **Steps only.** The common form: title, steps, one link.
- **With lead line.** One sentence under the title that says what the surface will show ("Once your traces come in, you'll see what you spend and which models work best for each task.").
- **Closable.** With the X. Closing removes it for good on this device; nothing in Settings brings it back, and the surface's own empty state takes over.
- **With sample data.** The banner and the dimmed sample under the card.
- **With an ambient field** (on trial, NDS-40). A dithered pixel field in the card's bottom trailing corner, faded before the text; Gateway draws it on the Private AI guide only. See *Motion*.

## States

| State | Treatment |
|---|---|
| Default | As above |
| Link hover | Underline |
| Close hover | `text-primary` |
| Close pressed | `brightness(0.92)` |
| Focus | 2px `focus-ring`, 2px outside, keyboard only |
| Content arrives | The card leaves and the content takes its place in one step; nothing animates the swap |
| Increased contrast | 1px `edge-hc` inset edge on the card and the banner |

## Behavior

- At most one action per card. A step that would need its own button is written as a step line instead.
- The info glyph opens on hover and pins on click; status, prerequisites and irreversible warnings stay in the step lines, never behind it.
- Closing is a preference, not a decision: no confirmation, no Undo toast. The product stores it per device.
- The card never counts down, never shows progress through the steps, and never ticks a step off for the person.

## Accessibility

- The card is a region named by its title; the steps are an ordered list, so assistive tech reads "1 of 3".
- The number disc is decorative inside the list item; the step title is the item's name and the line its description.
- The close button and every info glyph have names from the product ("Close", "More about Choose what to share").
- The sample is hidden from assistive tech and inert; the banner's words say what it is.
- Contrast: `text-primary`, `text-secondary` and the number's `accent-text` hold 4.5:1 over the worst ground.
- The consumer supplies every word (NDS-16).

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| `GetStartedCard` on `GlassCard`; steps from `InsightsTextWithInfo`; link as `GlassButtonStyle(.link)` with `arrow.right`; close persisted in `UserDefaults` | The same view on the opaque screen pane, steps in a `VStack`, link as a plain `Button` | `Card` with a `Column`; steps as `Row`s; link as `TextButton` with a trailing arrow | `<section class="nr-get-started">` with an `<ol class="nr-get-started__steps">`; `.nr-sample-banner` and `.nr-sample` for sample data |

## Do and don't

- Do write each step as a title over one short line, one idea each.
- Do name the link by where it goes ("Open Traces"), never by the step's title.
- Don't add a graphic, an illustration, a gradient or a second button.
- Don't put a promise in a step ("Your data stays private"); say what the person does and what happens.
- Don't leave sample data unlabelled, or let it take input.

## Source

`GetStartedCard` in `macos/Sources/TraceCommonsApp/Views/GetStartedCard.swift`, shared by the Insights empty state, the Private AI guide and Home's Traces walkthrough (owner, 2026-11-02, #1888); `InsightsSampleBanner` in `Views/InsightsGetStarted.swift` (the owner's banner words, approved); `GlassPixelField` in `TCDesign/Components/PixelField.swift` for the trial field. Gateway draws step numbers in `chartSeries1` (the parent's `data-1`) on a 14% tint of it; the parent uses `accent-text` on `accent-tint` so the digit holds text contrast.
