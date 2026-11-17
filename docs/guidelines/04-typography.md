# Typography

One step scale, four platform tiers, each platform's own faces. A step names a job (`label`, `body`, `heading`); the tier decides its size on that platform. Write `web-body` on the web and `ios-body` on an iPhone; the job and the hierarchy stay the same.

## Faces

| Platform | Text | Monospace | Notes |
|---|---|---|---|
| macOS, iOS, iPadOS, visionOS | SF Pro (system) | SF Mono | Through the system font APIs only. SF is licensed for Apple platforms; never bundle or serve it. |
| Android | Roboto Flex (system Roboto where Flex is absent) | Roboto Mono | Google Sans Flex is acceptable for hero type on Android if the product licenses it. |
| Windows | Segoe UI Variable Text (Display at 20pt and up) | Cascadia Mono | System fonts; no download. |
| Web, Linux | `system-ui` stack: SF on Apple, Segoe UI Variable on Windows, Roboto on Android and ChromeOS, Noto Sans, Ubuntu or Cantarell on Linux | `ui-monospace` stack | `--font-web`, `--font-mono` |

There is no bundled brand typeface in any app (NDS-4). The "near AI" wordmark is artwork from the logo kit; never set "Near AI" in type to imitate it.

**Marketing pages are the exception** (NDS-45). On the owner's request ("apply the Near AI brand fonts"), marketing sites use the near.ai/brand faces, loaded with system fallbacks:

| Face | Weights | Use |
|---|---|---|
| Schibsted Grotesk | 500, 600 | Headlines and titles, at −0.03 to −0.04em; the typeset product name beside the wordmark |
| Mona Sans | 400, 500, 600 | Ledes, body and buttons |
| JetBrains Mono | 400, 500 | Nav links, labels, code, terminal text and figures |

The Near AI chat moved off these faces to the system stack when it took this system's theme. App surfaces, product tours that replay an app, and anything inside a product use the platform faces only. See Web patterns for the marketing type ladder.

## The scale

| Step | Job | Compact: macOS (`mac-`) | Regular: web (`web-`) | Touch: iOS (`ios-`) | Touch: Android (`android-`) |
|---|---|---|---|---|---|
| `micro` | Tag and badge words, tick labels | 10/13 bold · caption2 | 11/14 bold | 11/13 bold · caption2 | 11/16 medium · labelSmall |
| `eyebrow` | Uppercase labels over cards and fields | 10/14 bold, +0.8 tracking · caption2 | 11/16 bold, +0.8 | 12/16 bold, +0.8 · caption1 | 12/16 bold, +0.8 · labelMedium (emphasized) |
| `caption` | Sub-lines, helper text, timestamps, inline alerts | 11/16 · subheadline | 12/16 | 13/18 · footnote | 12/16 · bodySmall |
| `label` | Control labels, field text, segments | 12/16 medium · callout | 13/18 medium | 15/20 medium · subheadline | 14/20 medium · labelLarge |
| `body` | Running text, list titles | 13/18 · body | 14/20 | 17/22 · body | 16/24 · bodyLarge |
| `body-strong` | Row titles, primary button labels, card titles | 13/18 semibold · body | 14/20 semibold | 17/22 semibold · headline | 16/24 medium · titleMedium |
| `title` | Card and modal titles | 15/20 semibold · title3 | 16/22 semibold | 20/25 semibold · title3 | 22/28 · titleLarge |
| `heading` | Pane and screen headings | 17/22 semibold · title2 | 20/26 semibold | 22/28 bold · title2 | 24/32 · headlineSmall |
| `display` | One headline per screen | 22/28 bold, -0.22 · title | 28/34 bold, -0.28 | 28/34 bold · title1 | 28/36 · headlineMedium |
| `number` | Hero figures and balances (tabular) | 26/34 bold · largeTitle | 32/40 bold | 34/41 bold · largeTitle | 32/40 medium · headlineLarge |
| `mono` | Paths, hashes, sizes, figures that leave the device | 11/16 SF Mono | 12/18 | 13/18 SF Mono · footnote | 12/16 Roboto Mono |

Sizes are size/line height in pt, px or sp. iOS tracking follows Apple's SF Pro tracking table at each size (for example -0.43 at 17pt, -0.23 at 15pt, +0.38 at 28pt); the tokens carry it. Two hero styles sit outside the tiers: `hero-display` 57/64 bold and `hero-figure` 45/52 bold, for one or two hero moments per product (a sign-in welcome, a launch page), never inside tools.

Two welcome styles are set by owner decisions rather than the scale:
- **Chat welcome title** (NDS-44): 28/34 semibold with tight tracking (24 on phones), over a 16/18 subtitle in `text-secondary`.
- **First-run step titles** (NDS-32): one line in two weights, a light lead and a bold phrase ("Connect your **tools**"), centered under the graphic, no period. First run's stage buttons are 13 semibold at 34 tall, lighter than the app's bold call to action.

## Rules

- **Map steps to text styles so type scales with the person's setting.** On macOS each step is a macOS text style at its default size, so the whole scale follows the system text-size setting; trace-commons enforces this with a token test. On iOS and iPadOS each step is a Dynamic Type style and grows from xSmall to AX5 (body reaches 53/62 at AX5). On Android use `sp` and the M3 roles. On the web use `rem` with a 16px root.
- **Controls use minimum heights, not fixed ones,** so a label can grow with the text size. Truncate only the middle of file paths, never a button label.
- **Fixed point sizes are for glyphs only.** A symbol inside a fixed-size control can take a fixed size; words never do.
- **Weights.** Regular for reading, medium for control labels, semibold for emphasis and titles, bold for display, numbers, micro and eyebrows. Never use light or thin weights in UI; they fail on glass. First-run titles draw their lead in a lighter weight only on the opaque first-run scene, at title size.
- **Emphasis by weight first.** Emphasized variants (iOS emphasized styles, M3 emphasized roles) change weight only. Never emphasize with color.
- **Numbers.** Use tabular digits (`font-variant-numeric: tabular-nums`, `.monospacedDigit()`) wherever figures line up or update live. Figures that describe what leaves the device (sizes, counts sent, hashes) are `mono`; prose never is.
- **Eyebrows** are uppercase with +0.8 tracking (+1 on a section rule). Keep them to two or three words. Marketing pages use none (NDS-45).
- **Line length.** Keep running text under about 65 characters (`size-readable-width` 680 at web body). Wider panes widen the margins, not the measure.
- **Minimum sizes.** Never below the platform minimum: 10pt macOS, 11pt iOS and iPadOS, 12pt visionOS and watchOS, 11sp Android, 11px web.
- **Contrast.** All text uses the text roles at 4.5:1 or more, with no large-text exemption (decision NDS-6).
- **A tab heading's line** sits under the title in body regular, `text-secondary`, 4 below, never bold or at title size; the tab's status goes in a `Chip` beside the title.

## Hierarchy

A screen has one `heading` (or one `display` on onboarding and empty hero states), then `title` per card or section, then `body` and `label`. `eyebrow` introduces a card without competing with its title. Never skip from `heading` to `caption` for content people must read.

## Density and the tiers

The tier follows the platform, not the window size: a narrow macOS window still uses `mac-` type, and a wide iPad still uses `ios-`. The dense pro-tool mode (`.nr-dense`) keeps the compact tier but tightens spacing; Unity's Editor sets body at 12px Inter and 18-20px rows, and the parent's `mac-label` 12/16 inside a 20px row is its equivalent.

## Localization

- Leave room: labels grow 30-40% in German and Finnish. Buttons hug their labels; never fix a button width to English.
- Scripts with tall glyphs (Thai, Vietnamese, Devanagari) need taller line heights; M3 publishes language-specific heights, and Apple's text styles handle it automatically.
- Mirror layout for right-to-left languages, but never mirror numbers, code, media controls or logo marks.
- Never build a sentence from fragments; counts inflect in the copy source.
