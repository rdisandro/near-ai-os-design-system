# ToolCall

An agent's request to act for the person: exactly what it will do, what happens to their data or work, and the answers Allow once, Always allow and Deny, with stricter handling for irreversible and destructive actions.

## When to use

- Whenever an agent wants a tool with effects outside the conversation: writing or deleting files, running commands, pushing code, sending messages, sharing data, spending money.
- Not for tools the person already allowed always. Those act at once, show a resolved row with Undo, and log in an `Expander` inside the `Message`.
- Use `Modal` only when the request must block the whole window, such as a checkbox-gated consent the product requires in a dialog.

## Anatomy

1. **Card** (`Card`), `card-gap` 10 between parts, inline in the thread.
2. **Head**: tool tile (`size-tool-tile` 22, `neutral-tint`, glyph in `text-secondary`); title as a sentence naming the agent and the action ("near-agents wants to edit 3 files", body strong); meta line with a `caution` dot, the product's "Needs your answer" and the tool id in mono (`text-tertiary`).
3. **Exact action**: mono on `consent` ground, `radius-control`, padding 8 / 10. The command, file list with line counts, recipients or amount. Wraps, never truncates.
4. **Consequence** (body, `text-primary`): what changes, who sees it, and whether it can be undone.
5. **Scope note** (caption, `text-tertiary`): what Always allow covers and where to change it, or why it is not offered.
6. **Consent gate** (optional): a `Checkbox` row; the confirming button stays `aria-disabled` until it is ticked.
7. **Actions**: right-aligned, Deny leading, Always allow next, the confirming action trailing (NDS-19). Pills `--nr-h-control` tall.
8. **Resolved row**: a quiet card with dot, outcome, object (caption or mono), time (tabular) and one link (Undo or Change).

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Title | `mac-body-strong` 13 | `web-body-strong` 14 | `ios-body-strong` 17 | `android-body-strong` 16 | `mac-label` 12 |
| Consequence | `mac-body` 13 | `web-body` 14 | `ios-body` 17 | `android-body` 16 | `mac-caption` 11 |
| Exact action | `mac-mono` 11 | `web-mono` 12 | `ios-mono` 13 | `android-mono` 12 | `mac-mono` 11 |
| Buttons / target | 28 / 28 | 28 / 28 | 44 / 44 | 44 / 48 | 20 / 20 |

In touch density the actions stack full width, the confirming action on top.

## Variants: the confirmation ladder (NDS-15)

| Kind | Example | Buttons | Answers Return | Always allow |
|---|---|---|---|---|
| Reversible | edit 3 files, with a checkpoint | Deny, Always allow, **Allow once** (`accent`) | Allow once | offered, scoped |
| Irreversible send | push a branch, send an email, post a reply | Deny, **Push** (`accent`, prominent) | nothing | never |
| Destructive | delete 214 files | Deny, **Delete 214 files** (`destructive-text` on `control`) | nothing | never |
| Consent | share a trace with the server that receives your traces | Deny, **Submit** (`accent`, after the gate) | nothing | never |
| Purchase | buy usage for a run | Deny, **Open checkout** | nothing | never; the person pays in the product's checkout |

Destructive is never the default. Agent actions ask the first time even when reversible, because the person didn't start them; after Always allow they act at once and offer Undo.

## States

| State | Shows |
|---|---|
| Needs your answer | `caution` dot; the run waits (`AgentRun` shows Needs you) |
| Answering | buttons inert, the chosen button shows the product's busy words |
| Allowed once, Always allowed | resolved row, `positive` dot; Undo while the change can be reverted, Change for Always |
| Denied | resolved row, `neutral` dot; the agent is told and continues or stops |
| Expired | resolved row, `neutral` dot and the product's words; the run stays paused |
| Failed | the tool ran and failed: a `critical-text` line with a `critical` dot (`nr-tool-call__alert`) and Retry |
| Gate unticked | confirming button `aria-disabled` |

Buttons: hover `control-hover`, pressed `brightness(0.92)` (accent: `accent-pressed`), disabled `opacity-disabled`, focus 2px `focus-ring` offset 2. Under `-hc` themes buttons and the exact-action block take the 1px `edge-hc` edge.

## Behavior

- **Focus**: the card never takes focus. It is announced politely and the composer keeps focus; Tab reaches the card's buttons.
- **Keys**: with focus inside the card, Return answers only a reversible Allow once; Esc means Deny. Irreversible, destructive, consent and purchase actions have no shortcut.
- **Away from the app**: a notification may offer Allow once and Deny for reversible requests only. Anything that can't be undone opens the app to this card. A Live Activity offers at most Review.
- **Always allow** is scoped to this agent, tool and folder, says so in the scope note, and is revocable in Settings; the resolved row links there with Change.
- **Queue**: several pending calls from one run show one card at a time with the product's "1 of 3".
- **Motion**: the card enters and later folds into its resolved row on `spring-spatial`; under Reduce Motion it swaps without movement.

## Accessibility

- The card is a `section` with `role="group"`, named by its title and described by the consequence. Reading order: title, exact action, consequence, scope, buttons.
- Announce arrival once, politely: "near-agents needs your answer: push a branch."
- The exact action is selectable text, read in full.
- In a queue, button names carry the object ("Allow near-agents to edit 3 files once").
- The destructive verb and count stay in the button label. `destructive-text` holds 4.5:1 on `control`.
- The consumer supplies every word: title, status words, tool id, exact action, consequence, scope note, gate sentence and labels.

## Platforms

| | SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|---|
| In thread | custom card | custom card | custom card | `section role="group"` |
| Siri, Shortcuts | App Intents `requestConfirmation`: a confirmation snippet, Cancel left, the verb right | same, view up to 400 pt | none | none |
| Notification | `UNNotificationAction` Allow once and Deny; others `.foreground` | same | notification actions, reversible only | Notifications API opens the card |
| Destructive button | `Button(role: .destructive)` | same | `TextButton` in the error color role | `button` |

## Do and don't

- Do show the exact command, files, recipients or amount.
- Do say whether it can be undone, and offer Undo afterwards when it can.
- Do keep Deny leading and always available.
- Don't offer Always allow for anything irreversible, destructive, consent or a purchase.
- Don't let an irreversible or destructive action answer Return or a notification tap.
- Don't tint the card or give it a colored edge; the dot and words carry "needs you".
- Don't write "safe" or "secure". State the data consequence.

## Source

Intentional addition: trace-commons has no agent-permission surface, but its confirmation ladder is the model. `GlassModalAction` roles with `isDefault` and `isProminent` (Modal.swift) give Return only to reversible actions and keep irreversible sends prominent without Return; checkbox-gated consent comes from `GlassCheckRow` (Forms.swift) and witness review (PreviewSheet.swift); the exact-action block from `GlassConsentBlock` and `GlassCode`; the copy guide's "move essential context beside the action". HIG Generative AI says to get permission before irreversible tasks and never to automate destructive actions or purchases; HIG Snippets set Cancel left and a specific verb right; HIG Live Activities and Notifications limit controls away from the app.
