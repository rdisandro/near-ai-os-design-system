# Modal

A dialog over the whole window that asks for one decision or holds one short task, with a header, a body and a footer of actions, and blocks the window until the person answers.

## When to use

- Confirm an irreversible or consent action (NDS-15): "Turn on Automatic for near-agents?", "Withdraw this trace?".
- Hold a short task that must finish before the person goes on: a passkey step, naming a folder.
- Don't confirm reversible actions. Act at once and offer Undo in a `Toast`.
- Don't put settings in a modal (NDS-21), and don't open one at launch or just to inform; use `InlineAlert` or `Notice`.
- On phones, a long form becomes a `Sheet`; a confirmation becomes the system alert.

## Anatomy

1. Layer: `scrim-modal` over the window content blurred by `blur-scrim`, at `z-scrim`. The modal sits inside an inset of `modal-inset-top` (52) at the top and `modal-inset` (28) on the other sides.
2. Container: `pane-base` with `pane-fill`, `radius-pane`, `shadow-modal`. Width `size-modal-width` (780, every confirmation) or `size-modal-narrow` (450, a short form).
3. Header: title (title type, weight 700) and an optional subtitle (caption type, `text-tertiary`); a small round close `IconButton` named by the product. Padding `space-14` top, `space-10` bottom, `space-16` sides; a 1px `rule` under it.
4. Body: padding `space-14` by `space-16`, `space-12` between blocks. A confirmation's message is body type in `text-secondary`, one paragraph per block. The body scrolls once the modal reaches the window inset; header and footer stay put.
5. Footer: actions trailing, `space-8` apart; an optional leading slot (a consent `Checkbox`). Padding `space-10` top, `space-14` bottom, `space-16` sides; a 1px `rule` over it.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Width | 780 or 450 | 780 or 450, never wider than the window less 28 each side | system alert; `Sheet` for forms | basic dialog 280 to 560 | 450 |
| Title | `mac-title` | `web-title` | system | `android-heading` | `web-body-strong` |
| Action height | 30 (`size-cta-small`) | 30 | 44 | 40 visible in a 48 target | 28 |

Every footer button is the small CTA's height whatever its kind, so Cancel stands as tall as Turn on (owner ruling D-20).

## Variants

- **Confirmation**: title, optional subtitle, message, two or three actions; always the regular width.
- **Form modal**: a short form in the body; regular or narrow.
- **Stacked**: a modal raised from a modal covers it; only the topmost answers keys.

## States

| Action role | Drawn as | Position | Keys |
|---|---|---|---|
| Cancel | glass | leading, left-most | Esc and Mod+. |
| Standard | glass; primary when it is the default or prominent | middle | Return when it is the default |
| Destructive | destructive | trailing, right-most | none, ever |

- Default: only a standard action can answer Return. Never a destructive action, never Cancel.
- Prominent: drawn primary with no Return key, for an action that must never be one keystroke away (an irreversible send).
- Busy (`aria-busy="true"`): the scrim, Esc, the close button and Cancel are inert until the work answers; the acting button shows its progress label ("Withdrawing…").
- A confirm action may be disabled until a required choice is made (a consent checkbox). Cancel is disabled only while busy.
- Increased contrast: a 1px `edge-hc` inset edge on the container.

## Behavior

- Opening fades the layer in on `duration-standard` with `ease-standard`; on Apple platforms the system dialog grows from the button that opened it. Under Reduce Motion it appears at once.
- Focus moves into the modal: the first field of a form, or the default action of a confirmation (Cancel when there is no default). Tab and Shift-Tab cycle inside. Covered content is inert and hidden from assistive tech.
- Esc, Mod+. and a click on the scrim cancel, except while busy or while Cancel is disabled. Closing returns focus to the control that opened the modal.

## Accessibility

- Role `alertdialog` for confirmations and `dialog` for forms, with `aria-modal="true"`, labelled by the title and described by the message.
- Every word comes from the product's copy: title, subtitle, message, action labels and the close button's name (NDS-16). Titles name the decision; action labels repeat its verb.
- Text on `pane-base` follows the pane contrast floors; `text-secondary` holds 4.5:1, 7:1 in the `-hc` themes.
- Touch actions are at least 44pt (Apple) or 48dp (Android).

## Platforms

| | SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|---|
| Confirmation | `GlassConfirmation` via `.glassModal(isPresented:)` under `.glassModalHost()`, replacing `.alert` and `.confirmationDialog` | `.alert` / `.confirmationDialog` (Liquid Glass, morphs from its button) | `AlertDialog` with parent colors | `.nr-modal` in `.nr-modal-layer`, or `<dialog>` with `showModal()` |
| Form | `GlassModal(title:, subtitle:, width:, actions:, busy:, onCancel:)` replacing `.sheet` | `.sheet` | `Dialog` (basic) | same |
| Return / Esc | `.keyboardShortcut(.defaultAction)` / `.cancelAction` | same with a keyboard | n/a | key handlers on the layer |

## Do and don't

- Do write the title as the decision ("Turn on Automatic for near-agents?"), never "Are you sure?".
- Do state what happens to data in the message ("Traces already sent stay sent.").
- Do keep one primary; Cancel leading, the primary or destructive action trailing (NDS-19).
- Don't use Yes, No or OK for a decision.
- Don't offer more than three actions.
- Don't let a scrim click abandon work in flight.

## Source

`GlassModal`, `GlassModalAction` (roles cancel, standard, destructive; `isDefault`, `isProminent`, `isEnabled`), `GlassConfirmation`, `GlassModalBody` and the `.glassModal` host in `macos/Sources/TCDesign/Components/Modal.swift`. The header's 18pt leading inset becomes `space-16` on the step scale. Order and Return rules agree with HIG Alerts and M3 Dialogs; the phone mapping follows HIG Alerts and M3's basic dialog.
