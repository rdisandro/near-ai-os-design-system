# Near AI OS Design System

The parent design system for Near AI products on desktop, web, tablet and phone. It carries the flat glass look of the Gateway macOS app (frosted panes, flat painted fills, one accent for the one action) into shared tokens, components and pattern libraries, and lets each product bring its own accent.

This repository is the source. The browsable reference is published as a Design System page: <https://claude.ai/artifact/NTUqkQNo8D8MQ6kSey959M> (private; share it from the page's Share menu).

## What is here

```
tokens/near-ai.tokens.json   the token source: 87 color roles x 6 themes, brand colors, scales, type, springs
css/*.css                    component styles, one file per component group (nr- classes)
components/<Name>/           59 components: README.md (spec) and preview.html (live card), plus the Cover
docs/brand-book.md           the brand book: principles, token usage, voice, visual foundations
docs/guidelines/             color, glass, type, layout and density, shape, motion, icons, accessibility, writing
docs/patterns/               navigation, desktop, web, tablet, phone, spatial, dense tools, AI, feedback, forms
docs/reference/              platform crosswalk, implementation, decisions and open questions
assets/logos/                Near AI lockups from the logo kit (unchanged)
dist/                        generated outputs (committed; regenerate with make build)
scripts/                     build, check, previews, accent derivation, page assembly
research/                    the research the system was built from
artifact.json                the published page's URL and its uploaded asset ids
```

Generated outputs in `dist/`:

| File | Use |
|---|---|
| `css/tokens.css` | CSS custom properties for all six themes. With no `data-theme`, follows `prefers-color-scheme` and `prefers-contrast`. |
| `css/near-ai.css` | The component stylesheet (load after `tokens.css`). |
| `tailwind/theme.css` | A Tailwind CSS v4 `@theme` mapping onto `tokens.css`. |
| `swift/NearAITokens.swift` | SwiftUI: `NearAITheme`, `NearAIColors`, measures, motion, type steps. Type-checks in Swift 6 for macOS 14 and iOS 17. |
| `compose/NearAITokens.kt` | Jetpack Compose: `NearAIThemes`, measures, springs, the Android type tier. |
| `dtcg/<theme>.tokens.json` | W3C design-token files for design tools. |
| `artifact/tokens.json` | Tokens in the published page's format. |
| `contrast-report.json` | Every contrast check and its ratio. |

## Use it

**Web.** Load the two stylesheets and set the theme on `<html>`:

```html
<link rel="stylesheet" href="dist/css/tokens.css">
<link rel="stylesheet" href="dist/css/near-ai.css">
<html data-theme="dark">   <!-- light, dark, light-hc, dark-hc, gateway-light, gateway-dark; omit to follow the system -->
```

```html
<section class="nr-pane nr-regular">
  <div class="nr-card">
    <span class="web-body-strong">near-agents</span>
    <span class="web-caption nr-text-secondary">Ask me · 3 sessions waiting</span>
  </div>
</section>
```

Each component's classes and states are in its `components/<Name>/README.md`. With Tailwind 4, import `tokens.css`, then `dist/tailwind/theme.css`; colors become utilities such as `bg-card` and `text-text-secondary`.

**SwiftUI.** Add `dist/swift/NearAITokens.swift` to a target:

```swift
let c = NearAITheme.dark.colors
Text("Contribute")
    .font(NearAIType.Mac.bodyStrong.font)
    .foregroundStyle(c.textOnAccent)
    .frame(minHeight: NearAISize.sizeCta)
    .background(c.accent, in: Capsule())
    .animation(NearAIMotion.springSpatialFast, value: isOn)
```

**Compose.** Add `dist/compose/NearAITokens.kt` (package `ai.near.design`):

```kotlin
val c = NearAIThemes.Dark
Text("Contribute", style = NearAIType.bodyStrong, color = c.textOnAccent)
val knob by animateDpAsState(target, animationSpec = NearAIMotion.springSpatialFast())
```

Glass is drawn per platform (native material, `backdrop-filter`, `RenderEffect`); the recipes are in `docs/guidelines/03-materials.md` and `docs/reference/22-implementation.md`.

## Change it

```bash
make build      # regenerate dist/ from the token source and css/
make check      # contrast floors, token references, component cards, stale dist/
make previews   # render every component card in light and dark to build/render/
make artifact   # assemble the published page's files in build/artifact/
```

- **A token.** Edit `tokens/near-ai.tokens.json`, then `make build` and `make check`. Every color role needs a value in all six themes.
- **A component.** Add `components/<Name>/README.md` and `preview.html` (first line `<!-- @dsCard group="…" height=N subtitle="…" -->`), and its styles to a `css/NN-<area>.css` file with `nr-<name>` classes. Use tokens only; the check rejects a `var(--…)` that is not a token.
- **A product theme.** Run `make accent SEED=#rrggbb` for a passing accent family, add the two themes to `themes`, and give every color role a value for them (copy the parent's and change the accent family). `make check` reports a product theme that misses a floor; it may not ship until it passes.
- **The published page.** Run `make artifact`, then publish `build/artifact/` to the URL in `artifact.json` with Claude Code's Artifact tool (`root` = `build/artifact`, `file_path` = its `project/design-system.json`, `files` = the printed map). New or changed SVGs are uploaded as assets first and recorded in `artifact.json`.

## The rules the checks hold

- Text is at least 4.5:1, and 7:1 in the increased-contrast themes, on every ground it is drawn on, measured over the worst desktop the glass can show (white under dark glass, #333333 under light glass).
- A mark that shows a state on its own (a selected fill, the focus ring, a chart series) is at least 3:1.
- No designer overrides. A product value that misses a floor is reported as flagged and blocks that theme. None is flagged today: Gateway took the parent accent (NDS-22) and the parent's hidden-toolbar greys (NDS-50).

## Decisions

The register is `docs/reference/23-decisions.md`: NDS-1 to NDS-8 are the owner's decisions of 2026-10-13, NDS-9 to NDS-21 are defaults set when the system was written, NDS-22 to NDS-50 are the owner's decisions from designing Gateway, the private chat and the Near AI Gateway site (2026-09-30 to 2026-11-04), and eleven questions are open. `research/sessions-2026-11.md` records where each of the later decisions came from.

## Relationship to trace-commons

trace-commons keeps its own token source (`design-tokens/glass.tokens.json`) and generator for the Gateway macOS app. This system took that file's flat theme as its baseline and its accent family as the Gateway theme; since 2026-10-20 Gateway has used the parent's accent and chart values in turn (NDS-22). `docs/guidelines/01-architecture.md` maps every name. Nothing here changes trace-commons.

The private chat (nearai/LibreChat) maps the parent's light and dark roles into its theme config, and the Near AI Gateway marketing site (nearai-gateway-website) follows the marketing rules in `docs/patterns/13-web.md` (NDS-45).

## Requirements

Python 3.9 or later (standard library only). Google Chrome for `make previews` (set `CHROME` to its path elsewhere than macOS). Xcode command-line tools to type-check the Swift output. No Node packages are needed to build.

## License

Not chosen yet.
