# ProofTag

A proof label for a model answer or a ledger row: the product's proof word on its tone, a glyph, an optional count, and an info button that explains what was attested.

## When to use

- Under every agent answer (the `Message` proof footer, or leading the reply's action row where replies are signed), on every model row and call in the Private AI ledger (Calls / Verified / Priced), and beside each model in the `PromptComposer` model menu.
- For the deployment as a whole, use the header proof pill: the same tag at header size with the `ProofSeal` as its glyph (NDS-43).
- Proof is shown only with ProofTag. Don't put proof words in a `Tag` or `StatusLabel`, and don't use ProofTag for anything that is not proof.

## Anatomy

1. **Pill**: `radius-pill`, padding 2 top and bottom, 6 leading, 8 trailing, gap 4, micro type.
2. **Glyph**: 10 (`space-10`), one shape per tone (check, clock, cross, arrow leaving, dash), drawn in the word's ink. Supplementary to the word. Where the deployment signs its replies, the glyph is the `ProofSeal` instead: 14 in a reply tag, 20 in the header pill.
3. **Word**: the product's proof word, never authored by the component.
4. **Count** (optional): tabular figures after the word ("Verified 1,262").
5. **Info button** (optional): a 16 (`size-glyph`) circled "i" in `text-tertiary`, 4 after the pill (`nr-proof-tag-group`), with an invisible hit area up to `--nr-target`.
6. **Popover**: the floating layer (`.nr-floating`: `popover` fill, `blur-floating`, `shadow-float`), `size-popover-width` 260 wide, padding 10 / 12 / 12. The word as its title (label), what was proven (caption, `text-secondary`), facts stacked as label (caption, `text-tertiary`) over value (mono, `text-primary`), and a link to the full report. A seal-bearing tag opens the larger proof popover instead (396 for a reply, 372 for the header): the seal, a title, the check list and the proof data (see AI and agent patterns).

## Variants

Tones are fixed. Only `verified` is proof.

| Core label | Gateway word | Tone | Ground / ink | Glyph |
|---|---|---|---|---|
| `verified` | Verified | proof | `proof-tint` / `proof-text` (NDS-43) | check, or the seal |
| `pending` | Pending | caution | `caution-tint` / `caution-text` | clock |
| `gateway_only` | Gateway only | caution | `caution-tint` / `caution-text` | clock |
| `failed` | Check failed | failed: critical with a 1px outline in its ink | `critical-tint` / `critical-text` | cross |
| `outside` | External | critical: left for an outside model, no proof | `critical-tint` / `critical-text` | arrow leaving |
| `unattested` | No proof | neutral | `neutral-tint` / `text-secondary` | dash |
| `unavailable` | Unavailable | neutral | `neutral-tint` / `text-secondary` | dash |
| `unrecorded`, or any label the client doesn't know | Not recorded | neutral | `neutral-tint` / `text-secondary` | dash |

A failed check and an outside call share a hue, so the outline keeps them apart. In a ledger, tags keep the core's fixed order so they never shuffle on reload.

The Near AI chat reads its own words for the same states (NDS-43, NDS-16):

| State | Chat word | Ground / ink |
|---|---|---|
| A reply still streaming | Signing (not a button yet) | `neutral-tint` / `text-secondary` |
| The deployment being checked | Checking | `neutral-tint` / `text-secondary` |
| `verified` | Verified | `proof-tint` / `proof-text` |
| `gateway_only` | Gateway signed | `caution-tint` / `caution-text` |
| `failed` | Check failed, with the outline | `critical-tint` / `critical-text` |
| Not run, or unreadable | Not checked | `neutral-tint` / `text-secondary` |

**Seal variant** (chat). The reply tag is 24 tall, `<tier>-caption` semibold, padding 6 leading and 10 trailing, gap 6, glyph 14, and the whole tag is the popover's button (no separate info button). It leads the reply's action row, followed by a 1 × 16 divider. The header pill is 36 tall on the web, `<tier>-label` semibold, glyph 20; after Verified it folds to the seal alone after 3.6 s unless hovered, focused or open.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Word | `mac-micro` 10 | `web-micro` 11 | `ios-micro` 11 | `android-micro` 11 | `mac-micro` 10 |
| Pill height | 17 | 18 | 17 | 20 | 17 |
| Info button, visual / target | 16 / 28 | 16 / 28 | 16 / 44 | 16 / 48 | 16 / 20 |
| Popover | 260, caption type | 260 | popover on iPad, sheet on iPhone | `RichTooltip` or bottom sheet | 260 |

## States

- **Static**: the pill is not interactive.
- **Info button**: hover `control-hover`; open (`aria-expanded="true"`) keeps `control-hover` and turns the glyph `text-primary`; keyboard focus 2px `focus-ring`, offset 2.
- **Changing**: Pending becomes Verified or Check failed in place when the check finishes; a ledger re-sorts only on reload. The tag itself does not animate. A seal-bearing tag lets its seal stamp in once when the evidence arrives (NDS-43); motion never runs on a timer.
- **Unknown**: a label the client can't read is neutral with the product's unknown word. Never Verified, never blank.
- **Increased contrast**: every pill takes a 1px `edge-hc` inset edge; Check failed takes a 2px outline in its ink. In forced colors each pill draws a 1px CanvasText border.

## Behavior

- With a pointer, hovering the info button shows the popover; a click pins it; Esc or a click outside closes it and returns focus to the button.
- On touch, a tap opens it: a popover on iPad and wide windows, a `Sheet` on phones.
- Fact values are selectable so a measurement can be copied. "Open the report" goes to the product's attestation report.
- The popover opens with the effects spring (`spring-effects`); under Reduce Motion it appears at once.

## Accessibility

- The word and count are the pill's text and are read as-is ("Verified 1,262"). In a table, the column header gives context. The glyph is hidden from assistive tech.
- The info button is named by the consumer ("About Verified") with `aria-expanded` and `aria-controls`. The popover is a non-modal `role="dialog"` with the same name.
- Never color alone: every tone has its word and a distinct glyph, and Check failed has its outline.
- `proof-text` holds 4.5:1 on `proof-tint` (7:1 in the `-hc` themes); `caution-text`, `critical-text` and `text-secondary` hold 4.5:1 on their tints and on every ground `text-primary` uses.
- The header pill announces its new word once through a polite live region; check rows each carry a spoken state word.
- The consumer supplies every word: the proof word, count format, button name, popover title, explanation, fact labels and link.

## Writing

- Words come from the product's core. Gateway's are `proof_verified` to `proof_unrecorded` in `monitor_screens_copy()`.
- The explanation says what was proven and when it was checked: "The computer that answered proved which model and code it ran. The proof matched Near AI's published measurements when it was checked."
- For outside calls, state the consequence: "This call left for an outside model. There is no proof of what ran."
- Never write "secure", "encrypted", "private" as a promise, "routing" or "endpoint".

## Platforms

| | SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|---|
| Pill | `GlassTag(_:tone:)` | custom capsule `Text` + `Image` | `Surface(shape = CircleShape)` with `Text` and `Icon` | `span` |
| Info | `GlassInfoButton` (system popover, pinned on click) | `Button` + `.popover`, sheet on compact width | `TooltipBox` with a persistent `RichTooltip`, or `ModalBottomSheet` | `button aria-expanded` + `popover` |

Custom on every platform; the popover uses each platform's native popover.

## Do and don't

- Do show a tag on every answer and every model row, including No proof and External.
- Do keep the outline on Check failed.
- Do use the proof greens for Verified. Don't use the `positive` mark green as the word's ink; it reads as neon.
- Do let the count stay a plain number; unknown counts are a dash, never zero.
- Don't draw Verified for a label you can't read.
- Don't turn proof into a percentage, score or meter.
- Don't color a whole row or card by its proof. The tag carries it.

## Source

Intentional addition as a component. It generalizes trace-commons' proof tags: `InferenceTabView.tone(_:)` and `InferenceWords.proof(_:)` in InferenceViews.swift draw `GlassTag` (Indicators.swift, where `failed` is the outlined pill "so it is never the same pill as outside") with `GlassInfoButton` (InfoButton.swift); the words come from `monitor_screens_copy()` in crates/trace-commons-contributor/src/preview_copy.rs. It stands alone because proof is Near AI's central claim and must read the same on every surface. The seal variant and the proof roles come from the Near AI chat (`Signature.tsx`, `Shield.tsx` in nearai/LibreChat PR #4, open), where the owner tuned the greens on 2026-11-03. HIG Machine learning supports showing attribution in words people understand instead of confidence numbers, and HIG Generative AI asks products to say where processing happens.
