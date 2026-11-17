# Architecture and theming

The system has three layers. The parent defines every role and rule. A product theme overrides the accent family and nothing else. A platform adapter renders the same roles with that platform's materials, controls and type. Change a value at the lowest layer that owns it.

| Layer | Owns | Example |
|---|---|---|
| Parent (this system) | Color roles, type steps, spacing, radii, materials, motion, density, components, patterns, contrast floors | `card` is the painted fill of a card; `size-cta` is 34 |
| Product theme | The accent family and, optionally, the first data colors | Gateway: the parent's Near AI blue since 2026-10-19 (NDS-22), with an accent-filled open toolbar menu and a lighter light well |
| Platform adapter | How a role renders: native material, control, font face, motion engine | `glass-veil` over `NSGlassEffectView` on macOS; over `backdrop-filter` on web |

## Token tiers

1. **Brand constants.** Colors that belong to a brand and never change with the theme: `brand-blue`, `brand-sky`, `brand-deep-blue` (the near.ai/brand blues), `brand-tile`, `brand-tile-dark` (the dark app-icon ground), `brand-paper`, `brand-ink`, and the Gateway product purple `gateway-purple`. Use them in logos, illustration and, where a role says so, as a role's value. Never style a control with a brand constant directly.
2. **Roles.** Every other color token names a job, not a hue: `pane-fill`, `text-secondary`, `accent`, `caution-text`, `data-3`. Components and screens use roles only. A role has a value in each of the six themes.
3. **Measures.** Spacing, radius, size, opacity, blur, z-index, breakpoint, duration and easing tokens. They do not change with the theme.
4. **Type styles.** One step scale (`micro` to `mono`) rendered per platform tier (`mac-`, `web-`, `ios-`, `android-`), plus two hero styles.
5. **Component specs.** Each component's README fixes its anatomy in measures and roles (for example `Button` bar size = `size-cta`, `radius-pill`, `web-body-strong`). A component never introduces a color of its own.

The CSS custom property for any token is `--` plus its name (`--accent`, `--space-12`, `--blur-pane`, `--spring-spatial`). Type styles are classes (`.web-body`, `.mac-label`). Font stacks are `--font-apple`, `--font-web`, `--font-android`, `--font-mono`.

## Themes

| Theme | When | Notes |
|---|---|---|
| `light` | Light appearance, any Near AI surface without a product theme | Cool grey glass, Near AI blue accent #035ca3 |
| `dark` | Dark appearance | Navy glass, Near AI blue accent #7ebcff with dark text |
| `light-hc` | Light appearance with Increase Contrast, `prefers-contrast: more` or high-contrast text | Veil 90%, every text pair 7:1, 1px `edge-hc` on every painted surface |
| `dark-hc` | Dark appearance with increased contrast | As above |
| `gateway-light` | Gateway, light | The trace-commons flat light theme: the parent accent #035ca3, an accent-filled open toolbar menu, a 28% well |
| `gateway-dark` | Gateway, dark | The trace-commons flat dark theme: the parent accent #7ebcff with dark text, an accent-filled open toolbar menu |

Pick the theme in this order: the product (parent or Gateway), then the appearance (the person's in-app choice if they made one, else the system's), then contrast (the `-hc` variant when the system asks for more contrast). A product without its own increased-contrast pair uses the parent `-hc` themes, accent included; legibility wins over brand there.

Appearance follows the system by default. An in-app Light / Dark / System choice is allowed and lives in Settings > General > Appearance. It applies at once to every window and never needs a restart.

## Adding a product theme

A product theme is a file of overrides for these roles and no others:

| Role | Rule |
|---|---|
| `accent` | Fills the primary action and every selected state. At least 3:1 against every ground (pane, card, quiet card, field, control, popover, menu, opaque pane) over the worst desktop, in both appearances. |
| `accent-pressed` | `accent` 8% darker in each channel. |
| `text-on-accent` | 4.5:1 on `accent` and `accent-pressed` (7:1 in the `-hc` themes). Light text on a dark accent, dark text on a light accent. |
| `accent-text` | 4.5:1 on every ground text-primary uses, over the worst desktop. |
| `accent-soft` | 3:1 on `pane-opaque`. Non-text accent marks and a single data series. |
| `accent-tint` | `accent-soft` at 14% (light) or 22% (dark). |
| `tab-ember`, `tab-ember-halo` | `accent-soft`, and `accent-soft` at 22% (light) or 31% (dark). |
| `focus-ring`, `selection`, `menu-hover` | `accent`; `menu-hover` at 90%. |
| `data-1` to `data-3` (optional) | Product-specific series, revalidated as a set with the remaining parent series. |

Derive the family from one seed color: hold its OKLCH hue and chroma, and step its lightness until each rule above passes. The parent accent was derived this way from `brand-blue` #0091fd (OKLCH 0.65, 0.19, 251): the light fill landed at L 0.47 (#035ca3), the dark fill at L 0.78 (#7ebcff), the accent text at L 0.37 and 0.90. Material Color Utilities (HCT tonal palettes) is an acceptable generator if every result is checked against the same floors. A product theme ships only when its contrast suite passes; the floors have no exceptions (decision NDS-6).

## How contrast is measured

Glass shows whatever is behind it, so text is measured over the worst case. Under dark glass the worst desktop is pure white; under light glass it is #333333 (light glass frosts a black desktop no darker than that). A ground is built bottom-up: desktop, then `glass-veil`, then `pane-fill`, then the tier's fill (`card`, `card-quiet`, `field`, `control`). Floating surfaces start from the desktop and add `popover` or `menu`. Every text role must hold 4.5:1 (7:1 in `-hc`) on every ground; every mark that carries a state on its own must hold 3:1. Charts are measured against `surface-chart`, status marks against `pane-opaque`. This is trace-commons' `FlatThemeContrastTests` model, applied to every theme.

## The relationship to trace-commons

trace-commons keeps `design-tokens/glass.tokens.json` as the Gateway product's own source, generating `GlassTokens.swift` and its GTK and WinUI roles. The parent took its flat-theme values as the baseline and its accent family as the Gateway theme; since 2026-10-20 trace-commons has taken the parent's accent, chart and `surface-chart` values back (NDS-22). The main names map like this:

| trace-commons key | Parent role |
|---|---|
| `glassVeil` | `glass-veil` |
| `paneFill` (gradient, flat: one stop) | `pane-fill` |
| `paneBase`, `paneOpaque` | `pane-base`, `pane-opaque` |
| `cardFill`, `cardFillQuiet` | `card`, `card-quiet` |
| `controlFill`, `controlHover`, `cardHover`, `rowHover` | `control`, `control-hover`, `card-hover`, `row-hover` |
| `wellFill`, `fieldFill`, `consentFill` | `well`, `field`, `consent` |
| `popoverFill`, `menuFill` | `popover`, `menu` |
| `textPrimary`, `textSecondary`, `textTertiary`, `placeholder` | `text-primary`, `text-secondary`, `text-tertiary`, `text-placeholder` |
| `purple` / flat `controlSelected`, `ctaFill`, `toggleOn` | `accent` |
| `purpleText`, `linkText` | `accent-text` |
| `purpleSoft` | `accent-soft` |
| `statusOn`, `statusAsk`, `statusOutside`, `statusOff` | `positive`, `caution`, `critical`, `neutral` |
| `statusOnText`, `statusAskText`, `statusOutsideText` | `positive-text`, `caution-text`, `critical-text` |
| `tintOn`, `tintAsk`, `tintOutside`, `tintAccent`, `tintNeutral` | `positive-tint`, `caution-tint`, `critical-tint`, `accent-tint`, `neutral-tint` |
| `selection`, `menuHover`, `menuHoverText` | `selection`, `menu-hover`, `text-on-accent` |
| `hairline`, `rule`, `edgeHighContrast` | `hairline`, `rule`, `edge-hc` |
| `chartSeries1` to `chartSeries4`, `chartSurface`, `chartGrid` | `data-1` to `data-4`, `surface-chart`, `chart-grid` |
| `dataShared`, `dataKept` | Gateway's Shared and Kept graph pair (product vocabulary) |
| `cardNested`, `controlOnMenu`, `controlOnSelection`, `toggleKnobOff` | `card-nested`, `control-on-menu`, `control-on-selection`, `toggle-knob-off` |
| `firstRunCard`, `firstRunControl`, `firstRunRule`, `firstRunGlow` | `scene-card`, `scene-control`, `scene-rule`, `scene-glow-brand` |
| `radius.pane/card/cardQuiet/control` (flat) | `radius-pane`, `radius-card`, `radius-card-quiet`, `radius-control` |
| `size.cta`, `size.controlLarge`, `size.control` | `size-cta`, `size-control-large`, `size-control` |
| `motion.fast`, `motion.standard`, curve 0.2, 0.8, 0.2, 1 | `duration-fast`, `duration-standard`, `ease-standard` |

Gateway-only tokens (menu-bar mode colors, the status item's `menuStrip*` colors, map fields, tool tints, the edge-rail handle, the first run's beam and approve greens, the hero promotion gradients) stay in the Gateway file; they are product vocabulary, not parent roles. The window-tier values trace-commons dropped for macOS (pane and popover blur, scrim blur, window radius 22, scene glows) come back here as `blur-pane`, `blur-floating`, `blur-scrim`, `radius-window` and `scene-glow-1` to `-3`, because the web, Windows, Linux and Android need them.

Migration path for Gateway, when its team chooses: keep the generator and the drift test, read the parent `tokens.json` first, then apply `glass.tokens.json` as the Gateway overrides. Nothing in the parent requires that change today.

## Governance

- **One register.** Decisions are numbered NDS-1, NDS-2 and so on in Decisions and open questions. Product decision IDs (trace-commons' D-, R- and Insights IDs) are never reused here.
- **Versioning.** `tokens.json` carries a `version`. Renaming or removing a token is a major change; adding one or changing a value is minor. Product themes declare the parent version they target.
- **Merge gate.** A token change ships with its contrast suite green in all six themes and with every component preview re-rendered in each theme.
- **Who decides.** Visual and component choices belong to the design owner; consent copy, notices and accessibility duties are fixed by the product spec and the floors. When the two disagree on a visual value, the shipped code is the record and the spec follows it, as trace-commons does.
