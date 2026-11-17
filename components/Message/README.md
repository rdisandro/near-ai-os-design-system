# Message

One turn in a conversation with an agent: the person's request, or the agent's answer with its sources, its proof and the actions that refine it.

## When to use

- Every turn in a chat thread, an agent side panel or a run transcript.
- Use `ToolCall` for a turn where the agent asks to act, `AgentRun` for work that outlives the thread, and `Expander` inside the body for reasoning and finished tool-call logs.
- Use `Notice` for system news.

## Anatomy

1. **Thread** (`nr-message-thread`): a column with `space-24` between turns. Turns are capped at `size-readable-width` (680).
2. **User turn**: a `Card` bubble (`card`, `radius-card`, 12/14 padding) on the trailing edge, held `space-48` off the leading edge.
3. **Head** (agent turns): agent tile (`size-tool-tile` 22, `radius-tile`, `accent-tint` ground, `accent-text` initials), agent name (label), time (caption, `text-tertiary`, tabular). The name and model disclose that an agent wrote it. A product with one assistant may hide the head from sight and keep it for assistive tech (`--headless`, NDS-44).
4. **Body**: rendered text with `space-8` between blocks; inline code on `neutral-tint`, `radius-dense`; code blocks use `CodeBlock`.
5. **Citation marker**: a 16 (`size-glyph`) pill on `neutral-tint`, the number in micro type, linked to its source.
6. **Sources**: a quiet card, one row per source (number, title as an `accent-text` link, location in mono `text-tertiary` that truncates), `hairline` between rows.
7. **Proof footer**: `ProofTag` with its info button, the model name in mono (`text-secondary`), then latency (caption). Where replies are signed, the seal-bearing `ProofTag` leads the actions row instead (NDS-43).
8. **Status line** (working): a 12 spinner (2px `rule` ring, quarter arc in the text color, `duration-spin`) and the step in words. A Near AI product may draw its thinking mark instead: the animated N at 16 in the glyph slot, shown only while the model works and gone once answer text streams (NDS-26, NDS-44).
9. **Caret** (streaming): a 2px bar, 1em tall, in the text color at the insertion point, pulsing on `duration-pulse`.
10. **Actions row**: quiet pills `--nr-h-control` tall with 8 sides, a 16 glyph and a label; feedback as icon-only pills; a 1px `rule` separator.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Body | `mac-body` 13 | `web-body` 14 | `ios-body` 17 | `android-body` 16 | `mac-caption` 11 |
| Name, time | `mac-label`, `mac-caption` | `web-label`, `web-caption` | `ios-label`, `ios-caption` | `android-label`, `android-caption` | `mac-label`, `mac-micro` |
| Model | `mac-mono` 11 | `web-mono` 12 | `ios-mono` 13 | `android-mono` 12 | `mac-mono` 11 |
| Action height / target | 28 / 28 | 28 / 28 | 44 / 44 | 44 / 48 | 20 / 20 |

## Variants

- **User** (`nr-message--user`) and **agent** turns.
- **Latest turn**: actions always shown. **Earlier turns**: add `nr-message__actions--reveal`; actions appear on hover or keyboard focus, and stay visible on touch.
- **With sources**, **with a change** (the actions row leads with Undo), **with versions** (Retry keeps earlier answers behind a "2 of 2" pager in the footer).
- **Editing** (user turn): the bubble becomes a `TextArea` with Cancel and Save and resend.
- **Headless** (`nr-message--headless`): the agent head is visually hidden but read by assistive tech, so a single-assistant thread reads as one voice. A turn on the person's side written by an agent keeps its name.
- **With reasoning**: live reasoning shows as the status line with the thinking mark; once settled it is a closed `Expander` with the product's word ("Thoughts") and the caret after it, no glyph.

## States

| State | Shows | Tokens |
|---|---|---|
| Working | head + status line, nothing for the first 200 ms | spinner in `text-secondary`, `rule`; or the thinking mark in `brand-blue` |
| Streaming | caret, footer `ProofTag` Pending, no actions | caret `currentColor` |
| Complete | final proof, model, actions | `text-primary`, `text-tertiary` |
| Stopped | partial text kept, neutral dot + the product's words, Continue and Retry | body `text-secondary`, dot `neutral` |
| Error | one inline alert line under the turn, Retry beside it, held text kept | `critical-text`, dot `critical` |
| Undone | the product's acknowledgement and Redo in the actions row | `text-secondary` |
| Proof unknown | `ProofTag` "Not recorded", never Verified | `neutral-tint` |

Actions: hover `control-hover`, pressed `brightness(0.92)`, disabled `opacity-disabled`, keyboard focus 2px `focus-ring` offset 2. Under `-hc` themes actions, citation pills and inline code take the 1px `edge-hc` edge.

## Behavior

- **Focus and scroll**: output never moves focus. The thread follows new text only while it is scrolled to the bottom; once the person scrolls up it stops following and offers a jump to the latest turn.
- **Stop**: Esc and Mod+. stop the answer (NDS-14). The text so far stays, with Continue and Retry.
- **Copy** copies Markdown and announces the product's acknowledgement. **Retry** reruns the request with the same model and context and keeps the earlier answer as a version. **Edit** reruns from that user turn; later turns become an earlier version. **Undo** reverts the change set this turn applied and names it ("Undo model change in config.toml"); Mod+Z does the same while focus is in the thread. Each correction shows that it took effect.
- **Feedback** is voluntary and never blocks the next turn. Each control states its consequence in its tooltip ("Sends this rating to Near AI, without the conversation"). The choice holds and shows as selected.
- **Citations**: activating a marker scrolls to its source row and highlights it; on phones it opens the sources in a `Sheet`.
- **Motion**: action reveal fades on `duration-fast` `ease-standard`. Under Reduce Motion the caret, spinner and thinking mark hold still; the words carry the state.

## Accessibility

- The thread is `role="log"` with polite announcements. Each turn is an `article` named by author and time ("near-agents, 14:01").
- While streaming, the turn has `aria-busy="true"` and the status line is `role="status"`. Announce the finished answer once, or at most sentence by sentence, never token by token. The error line is `role="alert"`, once.
- Long answers use real headings and lists. Citation markers have names ("Source 1, calls ledger"). The caret, spinner and avatar are hidden from assistive tech.
- Repeated actions carry their object: "Copy answer", "Retry answer", "Undo model change in config.toml".
- The consumer supplies every word: author, initials, time, body, source titles and locations, status text, action labels, tooltips, alerts and the proof word.
- Text tokens (`text-primary`, `-secondary`, `-tertiary`, `critical-text`) hold 4.5:1 on the worst ground. Dots are supplementary.
- Actions reach `--nr-target` through an invisible hit area: 28 pointer, 44 Apple touch, 48 Android and touch web.

## Platforms

| | SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|---|
| Thread | `ScrollView` + `LazyVStack`, `defaultScrollAnchor(.bottom)` | same, `.scrollDismissesKeyboard(.interactively)` | `LazyColumn(reverseLayout = true)` | `div role="log"` |
| Body | `Text(AttributedString(markdown:))`, `.textSelection(.enabled)` | same | `SelectionContainer` + Markdown renderer | sanitized Markdown to HTML |
| Actions | glass buttons with `.help`, plus a context menu on the turn | `.contextMenu` with the same items; the row on the latest turn | `IconButton`s, `DropdownMenu` on long press | buttons in a `role="group"` |
| Announce | `AccessibilityNotification.Announcement` | same | `liveRegion = LiveRegionMode.Polite` | polite live region |

Custom on every platform.

## Do and don't

- Do put Copy, Retry, Edit and Undo beside the result they act on.
- Do show the model and its proof on every agent answer, including "No proof".
- Do write the step being done ("Reading 4 traces in near-agents…"). Never "Thinking…" or "Processing…" alone; the Near AI chat still shows its tool's stock "Thinking…" beside the thinking mark, an open gap.
- Don't move focus or jump the scroll when output arrives.
- Don't show a confidence percentage. Give the reason ("The ledger shows 18 pending") or nothing.
- Don't draw an error as an empty bubble or a red card. One critical line under the turn, Retry beside it.
- Don't write "secure", "encrypted" or "private" in an answer's chrome. State where the message went.

## Source

Intentional addition: trace-commons has no conversation surface, and Near AI's agents need one everywhere. The headless variant, the thinking mark and the Thoughts disclosure come from the Near AI chat (nearai/LibreChat PR #5, open; owner, 2026-11-03). Parts come from TCDesign: `GlassAlert` and `GlassCode` (StatCard.swift), `GlassCard` (Containers.swift), `GlassSpinner` (Feedback.swift) and the Private AI proof tags (InferenceViews.swift, via `ProofTag`). Behavior follows HIG Generative AI (identify AI use; Edit, Undo, Retry and Adjust next to results; specific progress text; voluntary feedback), HIG Machine learning (feedback names its consequence; confidence as reasons, not percentages), HIG focus and keyboards (never move focus; Esc and Cmd-. cancel), Unity App UI `ThreadMessage` and `CodeBlock` (message states, reactions bar, copy button) and the M3 loading indicator (show nothing under 200 ms).
