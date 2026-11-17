# ConsentBlock

The product's consent sentence, verbatim, on a quiet ground directly above the action it governs, so people read what will happen to their data before they send, share or run.

## When to use

- Before any action that sends data off the device or out of Near AI Cloud, publishes it, or cannot be undone: Submit, Go public, Run with an outside model, Share this conversation.
- Use it once per action, in the same place on every platform.
- Use `Notice` for status and warnings, `InlineAlert` for a failure, and an `ActionBar` note for a short remark about the action that is not consent.

## Anatomy

1. **Block**: `consent` fill, `radius-card-quiet` 14, padding `space-10` by `space-12`, no edge in flat glass, at most `size-readable-width` 680 wide.
2. **Sentence**: the product's consent text exactly as its copy source holds it, body step, `text-primary`, never truncated or paraphrased.
3. **Check** (gated variant): under a 1px `hairline`, `space-10` above and below it, a `Checkbox` (`size-checkbox`, `accent`) and its label in the label step. The action stays disabled until it is checked.
4. **Action**: the `ActionBar` directly under the block. In an `ActionBar` the block takes the notes slot, `space-20` above the button row. Cancel leads, the action trails (NDS-19).

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Padding | 10 / 12 | 10 / 12 | 12 / 16 | 12 / 16 | 10 / 12 (never denser) |
| Sentence type | `mac-body` | `web-body` | `ios-body` | `android-body` | `web-body` |
| Check row | 15 box, label `mac-label` | 15 box, `web-label` | 22 box in a 44 row | 18 box in a 48 row | as regular |
| Width | the action column | up to 680 | full width less `margin-compact` | full width less 16 | as regular |

The block never shrinks its type to fit: on a narrow screen the sentence wraps and the sheet scrolls.

## Variants

- **Plain**: the sentence above the action. Gateway's review uses this form; its sentence says that nothing checks whether you looked, so no checkbox stands in for reading.
- **Gated**: the sentence plus a checkbox that names the decision ("Send this run to the outside provider"). Use it for consent that must be affirmed each time: going public, admitting a witness, sending to an outside model.
- **In a notification or menu-bar panel**: the same sentence as the body, with one action that opens the full review ("Look, then decide"), never a second way to approve.

## States

| State | Treatment |
|---|---|
| Default | `consent` fill, `text-primary` |
| Unchecked (gated) | the action is disabled at `opacity-disabled`; the block says what the box decides |
| Checked (gated) | the action enables; unchecking disables it again |
| Words missing | if the product has no sentence for this action, the action stays disabled with the product's reason; a component never writes a substitute |
| Busy | while sending, the block stays and the action shows its busy state; Cancel stops what can be stopped |
| Increased contrast | 1px `edge-hc` inset edge |

## Behavior

- The irreversible action is drawn prominent (primary) but never answers Return; people click or tap it, or Tab to it and press Space (NDS-15).
- The block is static text: it is never collapsed into an `Expander`, a tooltip or a link to a policy.
- If the words change between versions, the new words show the next time; nothing caches an old sentence.
- On touch the action sits under the block in the sheet's footer and scrolls with it only when the sheet is taller than the screen.
- Nothing moves.

## Accessibility

- The action's `aria-describedby` points at the sentence, so screen readers read the consent when focus reaches the action. On Apple platforms set the sentence as the button's accessibility hint.
- The gated checkbox has a real label; its state is native ("checked", "not checked").
- `text-primary` on `consent` holds 4.5:1 over the worst ground.
- The consumer supplies the sentence, the checkbox label and the action's verb. The component authors no words, and its content is never translated or edited by a design layer.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| `GlassConsentBlock(text)` above the `GlassActionBar`; prominent button without `.keyboardShortcut(.defaultAction)` | The same view in the sheet footer area; `.accessibilityHint(sentence)` on the action | A `Surface(color = consent, shape = 14dp)` with `Text`; `Checkbox` row; the confirm `Button` gets `semantics { contentDescription }` plus the sentence | `<div class="nr-consent-block">` (or `<p>`), `.nr-consent-block__check`, then `.nr-action-bar` |

## Do and don't

- Do show the product's sentence word for word. Don't summarize, shorten or restyle it as a warning.
- Do place it directly above the action it governs. Don't place it at the top of a long sheet.
- Do state the data consequence ("leave this machine", "kept by the provider"). Don't promise privacy or safety.
- Do disable a gated action until the box is checked. Don't pre-check the box.

## Source

`GlassConsentBlock` in Containers.swift (the core's consent sentence verbatim, directly above Submit, `consentFill`, 10 by 12 padding); the sentence and the single-action notification rule in the Rust core's consent_copy.rs (`GATE_STATEMENT`, "Look, then decide"); the confirmation ladder and checkbox-gated consent [trace-commons §4.5, §5.16 item 11]. HIG privacy and generative AI guidance on stating what is shared.
