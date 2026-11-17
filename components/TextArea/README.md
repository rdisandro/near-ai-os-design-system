# TextArea

A multi-line field for text that can run past one line, such as a note for reviewers, a bio or an agent's instructions; it grows with its text to a limit, then scrolls.

## When to use

- Use it for notes, descriptions and standing instructions.
- Use `TextField` for one line, and `PromptComposer` for a message to an agent.
- Show code or logs in a `CodeBlock`; a text area is for prose the person writes.

## Anatomy

1. **Label**: eyebrow type, uppercase, `text-tertiary`, `space-4` above.
2. **Well**: `field` fill, `radius-control`, padding `space-8` vertical and `space-10` horizontal. The minimum height is two control heights, `calc(var(--nr-h-control) * 2)` (56 at regular, the source's minimum). The maximum is five control heights (140), after which it scrolls.
3. **Text**: the label step at regular weight, `text-primary`; the body step on touch.
4. **Prompt**: `text-placeholder`, top leading, where the text will start.
5. **Footer** (optional): the message leading and the counter trailing, caption type. The counter reads `n/max` in tabular `text-tertiary`. Over the limit, both turn `critical-text`.

## Sizes by density

| | Compact (macOS) | Regular (web) | Touch iOS | Touch Android | Dense |
|---|---|---|---|---|---|
| Minimum height | 56 | 56 | 88 | 88 | 40 |
| Maximum height | 140 | 140 | 220 | 220 | 100 |
| Padding | 8 / 10 | 8 / 10 | 8 / 10 | 16 (M3) | 4 / 6 |
| Radius | 11 | 11 | 11 | 11 | 3 `radius-dense` |
| Text | `mac-label` regular | `web-label` regular | `ios-body` | `android-body` | `web-caption` |

## Variants

- **Growing** (default): grows line by line from the minimum, then scrolls at the maximum.
- **Fixed**: a set height that scrolls from the start, for long text in a layout that must not move. M3 prefers this on the web.
- **With counter**: for a limit the person can see. The product decides what is counted (characters, or bytes as Gateway's bio does) and supplies the numbers.

## States

Default, focus, invalid, disabled, mixed and increased contrast follow `TextField` with the same tokens. The invalid ring goes round the whole well. Over a limit, the counter turns `critical-text` and the message gives the limit ("Use 280 characters or fewer.").

## Behavior

- Return inserts a line break. Mod+Return runs the surface's primary action when it has one. Esc reverts an inline edit to its last committed text.
- Keep text typed past the limit and mark it invalid. Never cut it off silently.
- Commit on blur or with the surface's action, as a single undo entry.
- The height change follows the text with no animation.

## Accessibility

- A native `<textarea>` or `TextEditor` named by its label.
- `aria-describedby` lists the message and the counter. Announce the count politely at a threshold the product sets (for example 20 left) and when it goes over, never on every keystroke.
- The consumer supplies the label, prompt, message and counter text.
- Contrast and the focus rule are as in `TextField`.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| `GlassTextArea`: `TextEditor` in the field well with a prompt overlay | `TextField(axis: .vertical)` with a `lineLimit` range, or `TextEditor` for long text | `OutlinedTextField(singleLine = false, minLines, maxLines)` with the eyebrow above | `<textarea class="nr-text-area__input">` with the type class on it; `field-sizing: content` grows it, and browsers without it show the `rows` height |

## Do and don't

- Do give the limit up front when there is one, with a counter.
- Do size the minimum to the answer you expect.
- Don't use it for a single line.
- Don't let it grow without a maximum inside a pane; the actions below must stay in view.

## Source

`GlassTextArea` in Forms.swift: the text field's well, at least 56 tall, growing with its text, the prompt overlay and the same invalid ring. The review card's optional note (at most 140 tall with an n/max counter) in SessionReviewCard.swift and the bio's /280 counter in Settings. Added by the parent: the maximum height in control units, touch and dense sizes, and the counter announcement rule.
