# TextField

A single-line field for a short, specific value such as a handle, a name, an API key or a path, with its label above it.

## When to use

- Use it for answers that fit on one line. Use `TextArea` for anything longer, `NumberField` for numbers, `SearchField` to search or filter, and `Select` when the answer is one of a known set.
- Use the secure variant for passphrases and API keys. It hides what is typed.
- Show a value the person cannot change in a `KeyValueList`. A disabled field is for a value that is editable elsewhere or later.

## Anatomy

1. **Label**: eyebrow type, uppercase, `text-tertiary`, `space-4` above the well. Always present. A field whose label is drawn elsewhere hides it visually and keeps it as the accessible name.
2. **Well**: `field` fill, `radius-control` (11), height `--nr-h-control`, `space-10` horizontal padding, no rim (flat glass).
3. **Text**: the label step at regular weight, `text-primary`.
4. **Prompt**: a hint in `text-placeholder`, which holds 4.5:1 on `field`. It disappears as soon as typing starts, so it never replaces the label.
5. **Affix** (optional): leading or trailing text inside the well (`@`, a domain, a unit) in `text-tertiary`, `space-6` from the text.
6. **Message** (optional): one caption line under the well. Help is `text-tertiary`. A reason for an invalid entry is `critical-text` after a 6pt `critical` dot.

## Sizes by density

| | Compact (macOS) | Regular (web) | Touch iOS | Touch Android | Dense |
|---|---|---|---|---|---|
| Well height | 28 `size-control-large` | 28 | 44 `size-control-touch` | 56 (M3 field minimum) | 20 `size-control-dense` |
| Padding x | 10 | 10 | 10 | 16 | 6 |
| Radius | 11 `radius-control` | 11 | 11 | 11 | 3 `radius-dense` |
| Label | `mac-eyebrow` above | `web-eyebrow` above | `ios-eyebrow` above, or leading in a form row | `android-eyebrow` above | `mac-caption` / `web-caption` beside |
| Text | `mac-label` regular | `web-label` regular | `ios-body` | `android-body` | `mac-caption` / `web-caption` |
| Target | 28 | 28 | 44 | 48 | 20 |

Touch fields use the body step because both platforms' own fields do, and because iOS Safari zooms the page into any field set below 16px.

## Variants

- **Default**: label above the well.
- **Inline** (`.nr-text-field--inline`): label in a column beside the well, for dense inspectors and settings grids. The column is half the row unless the consumer sets `--nr-label-width` (Unity uses a third to two fifths, at least 96).
- **Secure**: `type="password"` or `SecureField`. Offer a reveal button only where the platform does; its name comes from the consumer.
- **With affix**: `.nr-text-field__affix`, with `--leading` for a prefix.

## States

| State | Look | Tokens |
|---|---|---|
| Default | Well fill; the prompt shows while empty | `field`, `text-placeholder` |
| Hover | No fill change; the I-beam cursor is the cue | none |
| Focus | 2px ring 2px outside the well, on pointer and keyboard focus as platforms draw it for fields | `focus-ring` |
| Invalid | 1px ring inside the well (2px in the -hc themes) and the reason in words | `critical`, `critical-text` |
| Disabled | Well at `opacity-disabled`; the message stays readable and says why | `opacity-disabled` |
| Mixed | An em dash "—" as the prompt in `text-secondary`; the consumer's word ("Mixed") is announced | `text-secondary` |
| Increased contrast | A 1px inset edge | `edge-hc` |

## Behavior

- Validate when the person can act on it. Check a format (an email, a URL) when they leave the field. Check a limit they can see (64 characters) while they type. Always say why in words; the ring alone is never enough.
- Enter or blur commits; Esc reverts to the last committed value. A field that drives something slow or destructive commits only then. Every other field may update live. Undo records one entry per commit, never per keystroke.
- Mixed: typing replaces the value on every selected item; Esc leaves them mixed.
- Size the well to the expected text, stack fields vertically with even spacing, and keep widths consistent within a group.
- Mod+F moves focus into the page's `SearchField`.
- Motion: the ring and fills change on `duration-fast` with `ease-standard`. Nothing moves, and Reduce Motion removes the transitions.

## Accessibility

- A native text input named by its label (`<label>`, `aria-labelledby`, `TextField(label, …)`). The prompt is never the name.
- Invalid: `aria-invalid="true"` and `aria-describedby` on the message; announce the message politely when it appears.
- The consumer supplies every word: label, prompt, help, the reason, the mixed word and any button names.
- Contrast: text `text-primary`, prompt `text-placeholder` and messages `text-tertiary` or `critical-text`, each 4.5:1 over the worst-case ground.
- The focus ring is on by default. A product that turns it off with `.nr-focus-off`, as Gateway does, fails WCAG 2.4.7 Focus Visible.
- Touch targets are the whole well: 44 on iOS, 48 on Android.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| `GlassTextField`: native `TextField`/`SecureField` in `.plain` style on the painted well | `TextField` in a `Form` row with the label leading, or with the eyebrow above outside lists; keyboard and content type per value; clear button trailing | `OutlinedTextField` with the eyebrow above (`label = null`), container `field`, unfocused outline transparent, focused `focus-ring`, error `critical`; `supportingText` for the message | `<label class="nr-text-field">` around the label, `.nr-text-field__well` (type class here) and `<input class="nr-text-field__input">` |

## Do and don't

- Do keep a visible label above every field.
- Do name the fix in the reason ("Use 64 characters or fewer.").
- Don't validate on every keystroke before the person has finished, except for a limit they can see.
- Don't split one value across fields or join two values in one.
- Don't mix field styles in a form; this system has one field style.

## Source

`GlassTextField` and `glassFieldWell(invalid:)` in Controls.swift: eyebrow label 4 above a 28 field, `fieldFill`, the prompt ink raised to clear 4.5:1 (owner ruling 2026-10-07), a 1pt invalid ring with the reason beside it from the core, `SecureField` when secure, and a focus binding for Command-F. Added by the parent: the inline and dense layout (Unity Foundations inspector and text field), commit and revert rules (Unity field contract), the mixed value (Unity gap), touch type sizes (HIG text fields, M3 text fields).
