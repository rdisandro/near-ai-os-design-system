# Implementation

This section is for engineers wiring the system into a product. It covers how tokens flow from this artifact into each platform, how each platform draws glass, how the springs translate, how the web components are built, what the tests check, and which fonts ship where. Platform names for every component are in Platform crosswalk; the rules behind the glass are in Glass and materials.

## The repository

The system's source lives in the Near AI OS Design System repository. The published page is assembled from it.

| In the repository | What it is | On the published page |
|---|---|---|
| `tokens/near-ai.tokens.json` | The hand-edited source: every role in six themes, scales, type, springs | (source only) |
| `dist/artifact/tokens.json` | Generated, in the page's list format | `tokens.json` |
| `dist/css/tokens.css` | Generated custom properties; follows `prefers-color-scheme` and `prefers-contrast` when no `data-theme` is set | compiled by the page from `tokens.json` |
| `css/*.css` → `dist/css/near-ai.css` | The component stylesheet, one source file per component group | `components/bundle.css` |
| `dist/tailwind/theme.css` | Tailwind CSS v4 `@theme` mapping onto `tokens.css` | (repository only) |
| `dist/swift/NearAITokens.swift` | SwiftUI colors per theme, measures, motion, type steps | (repository only) |
| `dist/compose/NearAITokens.kt` | Compose colors per theme, measures, springs, the Android type tier | (repository only) |
| `dist/dtcg/<theme>.tokens.json` | W3C design-token files for design tools | (repository only) |
| `components/<Name>/` | Each component's guidelines and preview | the component cards |
| `docs/` | The brand book and these sections | the brand book and sections |

`make build` regenerates `dist/`; `make check` holds the contrast floors, checks every token reference and fails if `dist/` is stale; `make previews` renders every component card in each theme; `make artifact` assembles the page's files for publishing.

## Token pipeline

`tokens.json` in this artifact is the parent source. Every product reads it; no product hand-keeps a copy of a value.

```
tokens.json                 parent roles x six themes, scales, type, motion
  + <product>.theme.json    sparse overrides: accent family, product series, product-only roles
      |
      +-- Swift     NRTokens.swift       macOS, iOS, iPadOS, visionOS   (+ drift test)
      +-- Kotlin    NearTokens.kt        ColorScheme, NearGlass, MotionScheme, Typography
      +-- CSS       tokens.css           [data-theme] blocks, :root scales, type classes
      +-- Tailwind  theme.css            @theme mapping onto tokens.css
      +-- WinUI     BrandTokens.xaml     roles, HighContrast aliases
      +-- GTK       brand_tokens.rs      @define-color sheets, flattened opaque
```

**Shape of the source.** Colors carry one value per theme (`light`, `dark`, `light-hc`, `dark-hc`, `gateway-light`, `gateway-dark`) as `#rrggbb` or `#rrggbbaa`, plus a `usage` note. Shadows are per theme too. Spacing, radius, size, opacity, blur, zIndex, breakpoint, duration and easing are theme-independent. Type is a set of tiers (`mac`, `web`, `ios`, `android`, `hero`) over one step scale. Names are kebab-case; CSS uses `--<name>`, Swift and Kotlin use lowerCamel (`glass-veil` becomes `glassVeil`).

**Product themes are overrides.** A product authors only what differs from the parent's light and dark columns (NDS-1), and the build resolves them into full theme columns, which is what `gateway-light` and `gateway-dark` are. Gateway overrides two roles today: `toolbar-expanded` and the light `well` (it took the parent's accent family and data colors, NDS-22, and hidden-toolbar greys, NDS-50). Product-only roles (Gateway's menu-bar strip, edge rail, map, tool tints, promo treatments, the Classic gradients) stay in the product file and never enter the parent. A product theme without its own increased-contrast pair falls back to the parent `light-hc` and `dark-hc`, whose accent is Near AI blue; a product that needs its accent there adds `<product>-light-hc` and `<product>-dark-hc` solved to the 7:1 text floor.

**Every generator validates before it writes.** Port the checks from trace-commons' `scripts/design-tokens/generate.py` and add the parent's:

- identifiers are kebab-case in the source and valid lowerCamel after conversion;
- colors are `#rrggbb` or `#rrggbbaa`, nothing else;
- a product theme overrides color roles only (and shadows that carry the accent, such as `edge-classic-cta`);
- every `mac-*` and `ios-*` size equals its Apple text style's default size;
- `text-on-accent` on `accent` reaches 4.5:1 (7:1 in `-hc`), or generation fails;
- the full contrast matrix in Testing passes, except the failures recorded in `contrast-report.json`;
- `--check` writes nothing and exits non-zero when any output is stale. Make it a required CI check (trace-commons runs it, but no client lane is required today).

### Swift

Follow trace-commons' pattern: one generator, one generated file, one drift test. Today `generate.py` reads `design-tokens/glass.tokens.json` and writes `macos/Sources/TCDesign/Generated/GlassTokens.swift`; `TokenDriftTests` decodes the JSON and compares every constant. The parent generator emits the same kind of file, with four appearance slots per color resolved by the system, so no view reads an environment value to pick a color.

```swift
// Generated from tokens.json + trace.theme.json. Do not edit.
public enum NRColor {
    public static let glassVeil = NRDynamicColor(
        light: 0xE3E6EC_A8, dark: 0x070A1A_AD, lightHC: 0xE3E6EC_E6, darkHC: 0x070A1A_E6)
    public static let accent = NRDynamicColor(            // Gateway build: gateway-light / gateway-dark columns
        light: 0x15608A_FF, dark: 0x6D14F3_FF, lightHC: 0x01599F_FF, darkHC: 0x7EBCFF_FF)
}

public struct NRDynamicColor: Sendable {
    let light, dark, lightHC, darkHC: UInt32              // 0xRRGGBBAA

    public var nsColor: NSColor {
        NSColor(name: nil) { appearance in
            switch appearance.bestMatch(from: [.aqua, .darkAqua,
                .accessibilityHighContrastAqua, .accessibilityHighContrastDarkAqua]) {
            case .darkAqua?: NSColor(rgba: dark)
            case .accessibilityHighContrastAqua?: NSColor(rgba: lightHC)
            case .accessibilityHighContrastDarkAqua?: NSColor(rgba: darkHC)
            default: NSColor(rgba: light)
            }
        }
    }
    public var color: Color { Color(nsColor: nsColor) }
}
```

On iOS the same struct resolves through `UIColor { traits in … }` on `traits.userInterfaceStyle` and `traits.accessibilityContrast == .high`. Type steps are generated as text styles (`.body`, `.title3`, `.caption2`) with a weight, never as point sizes. Springs are generated as `Animation` values (see Springs). The drift test decodes `tokens.json` and the product file, resolves the product's columns, and compares every constant, themes included (trace-commons' current drift test skips the `themes` block).

**Migrating trace-commons to inherit from the parent.** Do it in steps. The first three ship with no visual change; each later step changes one thing and its tests:

1. Vendor the parent `tokens.json` into `design-tokens/near-ai/` at a pinned version, recording its `meta.synced` date and a content hash that `--check` verifies.
2. Write `design-tokens/trace.theme.json` with Gateway's 16 overrides and its product-only roles, seeded from the flat theme's values as they ship, including the three that `contrast-report.json` flags.
3. Teach `generate.py` to read both files and map kebab names onto the existing keys through an alias table (`glass-veil` to `glassVeil`, `accent-soft` to `purpleSoft`, `critical-text` to `statusOutsideText`), so `GlassTokens.swift` keeps its API and, for the flat theme, its values. No screen changes.
4. Replace the `*HighContrast` partner tokens with the `-hc` columns, and extend `TokenDriftTests` and `FlatThemeContrastTests` to every theme.
5. Keep Classic as the optional expressive treatment in the product file (`edge-classic-*` from the parent, the gradients from Gateway).
6. Retire `glass.tokens.json`, then rename the deprecated keys over one release (`purpleSoft` to `accentSoft`).
7. Widen the GTK and WinUI outputs from the 11 shell roles to the full parent role set.

### Compose

Compose takes from the generator a Material `ColorScheme` for the slots M3 components read, a `CompositionLocal` for the roles M3 lacks, and a `MotionScheme` and `Typography` built from the tokens.

```kotlin
// Generated. M3 slots read by stock components.
fun nearColorScheme(t: NearRoles, dark: Boolean): ColorScheme {
    val base = if (dark) darkColorScheme() else lightColorScheme()
    return base.copy(
        primary = t.accent, onPrimary = t.textOnAccent,
        primaryContainer = t.accentTint, secondaryContainer = t.selection,
        onSecondaryContainer = t.textOnAccent,
        surface = t.paneOpaque, surfaceContainer = t.paneBase,
        surfaceContainerLow = t.cardQuiet, surfaceContainerHigh = t.card,
        surfaceContainerHighest = t.field,
        onSurface = t.textPrimary, onSurfaceVariant = t.textSecondary,
        outline = t.neutral, outlineVariant = t.hairline,
        error = t.critical, onError = t.textOnStatus, errorContainer = t.criticalTint,
        scrim = t.scrimModal,
    )
}

// Roles M3 has no slot for: glass and status.
@Immutable data class NearGlass(
    val veil: Color, val paneFill: Color, val paneBase: Color, val paneOpaque: Color,
    val popover: Color, val menu: Color, val inactiveDim: Color, val edgeHc: Color,
)
val LocalNearGlass = staticCompositionLocalOf<NearGlass> { error("Wrap content in NearTheme") }

object NearMotion : MotionScheme {
    override fun <T> fastSpatialSpec(): FiniteAnimationSpec<T> = spring(dampingRatio = 0.9f, stiffness = 1400f)
    override fun <T> defaultSpatialSpec(): FiniteAnimationSpec<T> = spring(dampingRatio = 0.9f, stiffness = 700f)
    override fun <T> slowSpatialSpec(): FiniteAnimationSpec<T> = spring(dampingRatio = 0.9f, stiffness = 300f)
    // One effects token (spring-effects) serves all three speeds.
    override fun <T> fastEffectsSpec(): FiniteAnimationSpec<T> = spring(dampingRatio = 1f, stiffness = 1600f)
    override fun <T> defaultEffectsSpec(): FiniteAnimationSpec<T> = spring(dampingRatio = 1f, stiffness = 1600f)
    override fun <T> slowEffectsSpec(): FiniteAnimationSpec<T> = spring(dampingRatio = 1f, stiffness = 1600f)
}

@Composable
fun NearTheme(roles: NearRoles, dark: Boolean, content: @Composable () -> Unit) {
    CompositionLocalProvider(LocalNearGlass provides roles.glass, LocalNearStatus provides roles.status) {
        MaterialTheme(
            colorScheme = nearColorScheme(roles, dark),
            typography = NearTypography,          // android-* steps on M3 roles, Roboto Flex
            motionScheme = NearMotion,
            content = content,
        )
    }
}
```

Rules for Android:

- Use `NearMotion`, never `MotionScheme.expressive()`, as the app default. The expressive spring (800, 0.6) is a separate value for one or two hero moments (NDS-11). Where the Compose Material3 version still marks `motionScheme` experimental, opt in or pass it through `MaterialExpressiveTheme`.
- Status roles (`positive`, `caution`, `critical` and their `-text` and `-tint`) live in `LocalNearStatus`. Never map them onto `tertiary`.
- Pick the theme from `isSystemInDarkTheme()` and, on API 34+, `UiModeManager.contrast`: at 0.5 or above, load the `-hc` roles. Dynamic (wallpaper) color stays off; a personal surface may opt in.
- `NearTypography` maps the steps onto M3 roles exactly as Platform crosswalk lists (`micro` to `labelSmall`, `body` to `bodyLarge`, `number` to `headlineLarge` with `fontFeatureSettings = "tnum"`).

### CSS custom properties

The artifact compiles `tokens.json` into `tokens.css`: a `:root, [data-theme="light"]` block, one block per other theme (`[data-theme="dark"]`, `light-hc`, `dark-hc`, `gateway-light`, `gateway-dark`), one `:root` block of theme-independent scales, then the type classes (`.mac-*`, `.web-*`, `.ios-*`, `.android-*`, `.hero-*`). Products import the same file.

Set `data-theme` on `<html>` from a small resolver that runs inline in `<head>` before first paint, and again when the system setting or the user's Light / Dark / System choice changes (NDS-17):

```ts
type Appearance = 'system' | 'light' | 'dark';
type Product = '' | 'trace-';
const mq = (q: string) => window.matchMedia(q);

export function resolveTheme(product: Product, appearance: Appearance): string {
  const dark = appearance === 'dark' ||
    (appearance === 'system' && mq('(prefers-color-scheme: dark)').matches);
  const base = dark ? 'dark' : 'light';
  if (mq('(prefers-contrast: more)').matches) return `${base}-hc`;   // parent -hc unless the product ships its own
  return `${product}${base}`;
}

export function watchTheme(product: Product, appearance: () => Appearance) {
  const apply = () => { document.documentElement.dataset.theme = resolveTheme(product, appearance()); };
  apply();
  ['(prefers-color-scheme: dark)', '(prefers-contrast: more)']
    .forEach((q) => mq(q).addEventListener('change', apply));
  return apply;   // call again after Settings > General > Appearance changes
}
```

The other user settings are pure CSS and never switch the theme:

- **`prefers-reduced-transparency: reduce`** turns every pane and floating surface to `pane-opaque` with no `backdrop-filter`. Support is partial, so mirror it with an in-app switch that sets `data-transparency="reduce"` on `<html>`.
- **`forced-colors: active`** drops the fills the browser removes anyway: panes and cards get a 1px `CanvasText` border, selection uses `Highlight` and `HighlightText`, the focus ring uses `Highlight`. Never set `forced-color-adjust: none` on text.
- **`prefers-reduced-motion: reduce`** removes transitions and animations; a change jumps to its end state.
- **`color-scheme`** is set per theme (`dark` for the dark themes) so form controls and scrollbars match.

CSS custom properties cannot appear in media queries. The generator writes breakpoints as literals wherever a query needs them: in the Tailwind theme below, or as `@custom-media --nr-medium (width >= 600px);` for a build that supports custom media.

### Tailwind 4

The Tauri frontend (React 19, Tailwind 4) maps Tailwind's theme onto `tokens.css`. Use `@theme inline` for themed values, so utilities emit `var(--accent)` directly and follow `data-theme` on any subtree; a plain `@theme` variable would resolve once at `:root`.

```css
@import "tailwindcss";
@import "./tokens.css";

@theme inline {
  --color-*: initial;                         /* no stock palette: every color is a role */
  --color-primary: var(--text-primary);       /* text-primary */
  --color-secondary: var(--text-secondary);   /* text-secondary */
  --color-tertiary: var(--text-tertiary);
  --color-accent: var(--accent);              /* bg-accent */
  --color-on-accent: var(--text-on-accent);   /* text-on-accent */
  --color-accent-text: var(--accent-text);
  --color-card: var(--card);
  --color-control: var(--control);
  --color-control-hover: var(--control-hover);
  --color-field: var(--field);
  --color-hairline: var(--hairline);
  --color-critical-text: var(--critical-text);
  --font-sans: var(--font-web);
}

@theme {                                      /* generated literals, equal to tokens.css */
  --breakpoint-*: initial;
  --breakpoint-medium: 37.5rem;               /* bp-medium 600 */
  --breakpoint-expanded: 52.5rem;             /* bp-expanded 840 */
  --breakpoint-large: 75rem;                  /* bp-large 1200 */
  --breakpoint-xlarge: 100rem;                /* bp-xlarge 1600 */
  --radius-*: initial;
  --radius-pane: 20px;
  --radius-card: 16px;
  --radius-control: 11px;
  --radius-pill: 999px;
  --ease-standard: cubic-bezier(0.2, 0.8, 0.2, 1);
}

@custom-variant dark (&:where([data-theme*="dark"], [data-theme*="dark"] *));
@custom-variant hc (&:where([data-theme$="-hc"], [data-theme$="-hc"] *));
```

Rules for Tailwind:

- Spacing keeps Tailwind's 4px step; the parent's 2px steps are the halves (`p-0.5` is `space-2`, `p-1.5` is `space-6`, `p-2.5` is `space-10`, `p-3.5` is `space-14`).
- Glass, shadows and blur belong to components (`.nr-pane`, `.nr-floating`, the bars), so the Tailwind theme does not map them. Never write `backdrop-blur-*` utilities in product code.
- Type, mono included, comes from the generated `web-*` styles. The generator also emits them as `@utility web-body { … }` so variants work (`md:web-heading`).
- Never put an opacity modifier on a role (`bg-card/50`). Translucent roles already carry their alpha, and a second dimming breaks the contrast tests.

[trace-commons: generate.py, GlassTokens.swift, TokenDriftTests] [material-web: token pipeline] [M3: color roles]

## Glass by platform

Glass lives on the navigation and floating layers only (NDS-9). Each platform below draws the same three tiers: the native or CSS blur with the veil and fill, an opaque `pane-base` where blur is missing, and `pane-opaque` under Reduce Transparency and its equivalents on the shells that paint their own glass. On Apple platforms Reduce Transparency is the system's to apply (NDS-23).

### macOS: SwiftUI and AppKit

A pane is the native material with the parent's veil and flat fill painted over it (NDS-7): `NSGlassEffectView` style `.regular`, tinted with a quarter of the veil, on macOS 26 and later; `NSVisualEffectView` `.hudWindow` behind the window on macOS 14-25. Floating surfaces (menus, popovers, node cards) paint `popover` or `menu` over an `NSVisualEffectView` blending within the window. Only TCDesign-style tier code branches on the OS; screens never do.

```swift
/// Tier code. The only place that knows which material this Mac draws.
struct NRPaneBackground: View {
    var radius: CGFloat = NRRadius.pane                          // radius-pane 20
    @Environment(\.controlActiveState) private var activeState
    @Environment(\.colorSchemeContrast) private var contrast

    var body: some View {
        let shape = RoundedRectangle(cornerRadius: radius, style: .continuous)
        // Reduce Transparency is the system's to apply (NDS-23): the material
        // frosts itself; the veil and fill stay as they are.
        ZStack {
            NRNativeMaterial(cornerRadius: radius)
            shape.fill(NRColor.glassVeil.color)
            shape.fill(NRColor.paneFill.color)
            if activeState != .key { shape.fill(NRColor.inactiveDim.color) }
        }
        .overlay {
            if contrast == .increased { shape.strokeBorder(NRColor.edgeHc.color, lineWidth: 1) }
        }
    }
}

struct NRNativeMaterial: NSViewRepresentable {
    let cornerRadius: CGFloat

    func makeNSView(context: Context) -> NSView {
        if #available(macOS 26, *) {
            let glass = NSGlassEffectView()
            glass.style = .regular                                  // never .clear: it shows the desktop unblurred
            glass.tintColor = NRColor.glassVeil.scaledAlpha(0.25).nsColor
            glass.cornerRadius = cornerRadius
            return glass
        }
        let effect = NSVisualEffectView()                           // macOS 14-25
        effect.material = .hudWindow
        effect.blendingMode = .behindWindow
        effect.state = .active
        effect.wantsLayer = true
        effect.layer?.cornerRadius = cornerRadius
        effect.layer?.cornerCurve = .continuous
        effect.layer?.masksToBounds = true
        return effect
    }

    func updateNSView(_ view: NSView, context: Context) {}
}
```

Rules for the Mac:

- Leave Reduce Transparency to the system (NDS-23). The owner ruled on 2026-10-02 not to regress Apple's guidance: the native material frosts itself, and the painted veil and fill stay. trace-commons does the same (its R14). Only the shells that paint their own glass (web, Windows, Linux, Android) switch to `pane-opaque`.
- Under Increase Contrast, the `-hc` columns resolve by themselves; add the 1pt `edge-hc` stroke to painted surfaces and never a border of our own on system glass. On macOS 27, also stroke interactive controls when `accessibilityShowBorders` is true.
- `.glassEffect`, `GlassEffectContainer`, `.glassProminent` and `NSGlassEffectView` appear only in tier code behind `#available`. Keep trace-commons' source-scan test that fails when a screen calls them.
- The window is transparent with a full-size content view and no title-bar separator, so the material shows through.
- Two trade-offs are known and accepted (NDS-7): painted surfaces do not follow the user's Liquid Glass slider, and macOS 27 draws its own glass edges.
- `.hudWindow` is a dark material. The light-appearance fallback on macOS 14-25 is still open in trace-commons; test it before shipping a light pre-26 build.

```swift
extension View {
    /// Merges neighboring glass controls. Tier code only.
    @ViewBuilder func nrGlassGroup(spacing: CGFloat = NRSpace.s8) -> some View {
        if #available(macOS 26, iOS 26, *) {
            GlassEffectContainer(spacing: spacing) { self }
        } else {
            self
        }
    }
}
```

### iOS and iPadOS: SwiftUI and UIKit

The screen is an opaque pane, `pane-base`; Reduce Transparency is the system's to apply to its own glass (NDS-23). System bars, tab bars, toolbars and sheets keep their own Liquid Glass; set `.tint(accent)` at the root and never paint them. A floating toolbar the app draws follows the Mac recipe.

```swift
/// Design-system tier code: the only iOS view that calls .glassEffect.
struct NRFloatingToolbar<Content: View>: View {
    @ViewBuilder var content: Content

    var body: some View {
        let bar = HStack(spacing: NRSpace.s8) { content }.padding(NRSpace.s8)
        // Reduce Transparency: the system frosts its own glass (NDS-23).
        if #available(iOS 26, *) {
            bar.background(NRColor.glassVeil.color, in: .capsule)
               .glassEffect(.regular.tint(NRColor.glassVeil.scaledAlpha(0.25).color), in: .capsule)
        } else {
            bar.background(NRColor.glassVeil.color, in: .capsule)
               .background(.regularMaterial, in: .capsule)
        }
    }
}
```

In UIKit the same tiers are `UIVisualEffectView(effect: UIGlassEffect(style: .regular))` with `tintColor` on iOS 26, `UIBlurEffect(style: .systemMaterial)` before it, with Reduce Transparency left to the system (NDS-23). Partial sheets stay inset and go opaque at full height, as the system draws them. Never stack glass: controls on a glass toolbar are plain fills.

### Android: Compose

Bars that float over content (the top bar once content scrolls under it, the navigation bar, the rail, a floating toolbar) blur what is behind them with `blur-bar` and paint `glass-veil`; menus and popovers use `blur-floating` with `popover`. The screen itself is `pane-base`.

`RenderEffect` blurs a layer's own pixels, not what lies behind it. A backdrop blur records the content into a `GraphicsLayer` and draws a blurred, clipped copy behind the bar, or uses a backdrop library such as Haze (`hazeSource` on the content, `hazeEffect` on the bar).

```kotlin
/** blur-bar = blur(20px) saturate(160%) as an Android RenderEffect (API 31+). */
@RequiresApi(31)
fun blurBarEffect(density: Density): RenderEffect {
    val r = with(density) { 20.dp.toPx() }
    val saturate = android.graphics.ColorMatrix().apply { setSaturation(1.6f) }
    return android.graphics.RenderEffect.createChainEffect(
        android.graphics.RenderEffect.createColorFilterEffect(ColorMatrixColorFilter(saturate)), // outer
        android.graphics.RenderEffect.createBlurEffect(r, r, Shader.TileMode.CLAMP),            // inner
    ).asComposeRenderEffect()
}

@Composable
fun rememberGlassTier(): GlassTier {
    val context = LocalContext.current
    val blur = Build.VERSION.SDK_INT >= 31 &&
        context.getSystemService(WindowManager::class.java).isCrossWindowBlurEnabled &&
        !LocalNearSettings.current.reduceTransparency
    return if (blur) GlassTier.Blur else GlassTier.Opaque     // Opaque: pane-base, no blur
}
```

Draw opaque `pane-base` below API 31, when the system has turned blur off (`isCrossWindowBlurEnabled` is false on low-end devices and in power saving; listen for changes), and when the user turns on the app's Reduce transparency switch. Android has no system-wide equivalent on every device, so the app offers one. Reserve AGSL lensing for at most one or two fixed-size hero controls behind a capability flag, or skip it.

### Web

```css
.nr-pane {
  background-color: var(--glass-veil);
  background-image: linear-gradient(var(--pane-fill), var(--pane-fill));
  -webkit-backdrop-filter: var(--blur-pane);
  backdrop-filter: var(--blur-pane);
}
@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
  .nr-pane { background: var(--pane-base); }
}
@media (prefers-reduced-transparency: reduce) {
  .nr-pane { background: var(--pane-opaque); -webkit-backdrop-filter: none; backdrop-filter: none; }
}
:root[data-transparency="reduce"] .nr-pane {
  background: var(--pane-opaque); -webkit-backdrop-filter: none; backdrop-filter: none;
}
@media (forced-colors: active) {
  .nr-pane { background: Canvas; border: 1px solid CanvasText; backdrop-filter: none; }
}
```

Rules for the web:

- Always write the `-webkit-` prefix beside `backdrop-filter`; Safari still needs it.
- Budget about four backdrop-filtered surfaces visible at once, and one large one (a sidebar). Never put `backdrop-filter` on items in a scrolling list; they are content and each one is a compositing pass.
- Animate opacity and transform only. Never animate a blur radius.
- Keep compositor cost under 2ms a frame on mid-range hardware. Set `data-transparency="reduce"` on devices with four cores or fewer, with Save-Data or `prefers-reduced-data`, or when frame time degrades.
- Never rely on SVG displacement lensing (`backdrop-filter: url(#…)`). Only Chromium renders it; Safari ignores it, and Firefox passes `@supports` and then draws nothing, so the glass disappears.
- Put menus, popovers and modals in the top layer (`popover`, `<dialog>` with `showModal()`), so their blur samples the page beneath.

**Tauri shells.** On macOS, the native `NSGlassEffectView` sits under a transparent webview; the page drops its CSS blur on panes and paints the veil and fill only, as trace-commons' glass branch does with `html.tc-native-glass`. On Windows, use Mica (below). On Linux, use the opaque tier.

### Windows

Windows 11 maps onto the same split. Mica, opaque and dynamic, is the large glass for long-lived window backgrounds, title bars and sidebars; Acrylic, translucent and live, is for transient surfaces such as menus, flyouts and tooltips. Use the system backdrop, never a painted imitation.

```csharp
public MainWindow()
{
    InitializeComponent();
    ExtendsContentIntoTitleBar = true;
    SystemBackdrop = new MicaBackdrop();     // the pane material; veil and fill are painted in XAML over it
}
```

In a Tauri window, request the `mica` window effect on a transparent window and keep CSS `backdrop-filter` for the floating layer inside the page. Under High Contrast, drop Mica and Acrylic and alias every role to the system brushes, as trace-commons' generated `BrandTokens.xaml` already does. The current WinUI shell draws opaque brushes and its own warm palette; moving it to the parent roles and Mica is part of the migration.

### Linux: GTK

GTK and libadwaita have no backdrop blur, so the Linux shell is opaque throughout. Panes paint `pane-base`, cards and controls paint their roles flattened over it at generation time (the generator composites each translucent role over `pane-base` so GTK gets exact opaque colors that the contrast tests measure). Follow `adw::StyleManager` for dark and high contrast, loading the `-hc` roles when high contrast is on; never override the high-contrast theme at application priority, which the current GTK shell does. Blur appears only where a compositor offers it (KDE), and the opaque tier stays the default.

[Liquid Glass: API mapping, non-Apple platforms] [trace-commons: GlassBackdrop.swift, Tauri glass CSS, WinUI, GTK] [HIG: materials]

## Springs

Every spring token is a (stiffness, damping ratio) pair at mass 1. Each platform takes the pair directly or a value derived from it.

| Token | Stiffness k | Damping ratio ζ | SwiftUI | Compose | CSS (curve over duration) |
|---|---|---|---|---|---|
| `spring-spatial-fast` | 1400 | 0.90 | `.spring(response: 0.168, dampingFraction: 0.9)` | `spring(0.9f, 1400f)` | `var(--spring-spatial-fast)` over `duration-spring-spatial-fast` 224ms |
| `spring-spatial` | 700 | 0.90 | `.spring(response: 0.237, dampingFraction: 0.9)` | `spring(0.9f, 700f)` | `var(--spring-spatial)` over 317ms |
| `spring-spatial-slow` | 300 | 0.90 | `.spring(response: 0.363, dampingFraction: 0.9)` | `spring(0.9f, 300f)` | `var(--spring-spatial-slow)` over 484ms |
| `spring-effects` | 1600 | 1.00 | `.spring(response: 0.157, dampingFraction: 1)` | `spring(1f, 1600f)` | `var(--spring-effects)` over 231ms |
| `spring-expressive` | 800 | 0.60 | `.spring(response: 0.222, dampingFraction: 0.6)` | `spring(0.6f, 800f)` | `var(--spring-expressive)` over 360ms |
| `spring-ember` | 322 | 0.85 | `.spring(response: 0.35, dampingFraction: 0.85)` | `spring(0.85f, 322f)` | `var(--spring-ember)` over 488ms |

The conversions:

- **SwiftUI.** response = 2π / √k and dampingFraction = ζ. The exact equivalent is `.interpolatingSpring(mass: 1, stiffness: k, damping: 2ζ√k)`; `Spring(duration: response, bounce: 1 − ζ)` is the same curve. `spring-ember` is Gateway's tab ember, `.spring(response: 0.35, dampingFraction: 0.85)`, as shipped.
- **Compose.** `spring(dampingRatio = ζ, stiffness = k)`, used directly or through `NearMotion`.
- **CSS.** The `linear()` token samples the spring's step response; its `duration-spring-*` partner is the settle time. Always use the pair together. Where `linear()` is unsupported, fall back to `ease-standard` at the same duration.

```css
.nr-switch__track::before {
  transition: transform var(--duration-spring-spatial-fast) var(--spring-spatial-fast);
}
@supports not (transition-timing-function: linear(0, 1)) {
  .nr-switch__track::before { transition-timing-function: var(--ease-standard); }
}
@media (prefers-reduced-motion: reduce) {
  .nr-switch__track::before { transition: none; }
}
```

For JavaScript-driven motion, pass the same strings to the Web Animations API: `el.animate(frames, { duration: 317, easing: getComputedStyle(document.documentElement).getPropertyValue('--spring-spatial') })`.

Reduce Motion is one rule everywhere: nothing moves (NDS-11). SwiftUI returns a `nil` animation when `accessibilityReduceMotion` is true; Compose uses `snap()` when the system animator duration scale is 0; CSS sets `transition: none`. Navigation transitions use each platform's defaults and never take a token.

[M3: motion springs] [trace-commons: GlassMotion.swift, Navigation.swift] [material-web: linear() springs]

## Web components

The web builds its own components on the parent tokens (NDS-18): React with headless accessible primitives for behavior, and the classes in `components/bundle.css` for the look. Each component card in this artifact is the reference rendering; the React component's job is to put those classes on the primitive's DOM.

```tsx
import { Button as AriaButton, type ButtonProps as AriaButtonProps } from 'react-aria-components';

type Kind = 'primary' | 'secondary' | 'glass' | 'destructive' | 'link' | 'submit';

export interface ButtonProps extends AriaButtonProps {
  kind?: Kind;
  bar?: boolean;            // action-bar size: size-cta
}

/** Words come from the product's copy source as children; the component authors none. */
export function Button({ kind = 'glass', bar = false, className, ...rest }: ButtonProps) {
  const classes = ['nr-button', `nr-button--${kind}`, bar && 'nr-button--bar', className]
    .filter(Boolean).join(' ');
  return <AriaButton {...rest} className={classes} />;
}
```

**Choose one primitive library per app.** React Aria Components covers the whole inventory, including number fields, tables and internationalized behavior. Radix covers the overlays and form controls. The Tauri shell on trace-commons `main` still uses Base UI through shadcn. The owner ordered every shadcn reference removed from it on 2026-09-30, including the colored left bar on alerts; that work is in #1146, which has not merged. Don't build new surfaces on shadcn. Render native elements wherever the primitive allows, so the bundle's `:hover`, `:active`, `:focus-visible` and `:disabled` rules apply; where a primitive manages a state itself, style its attribute beside the pseudo-class (`[data-pressed]` with `:active`).

| Component | React Aria Components | Radix |
|---|---|---|
| `Button`, `IconButton` | `Button` | native `<button>` |
| `Menu`, `SplitButton` | `MenuTrigger`, `Menu`, `MenuItem`, `SubmenuTrigger` | `DropdownMenu`, `ContextMenu` |
| `CommandPalette` | `Modal`, `Autocomplete`, `Menu` | `Dialog` with a combobox |
| `Modal`, `Sheet` | `ModalOverlay`, `Modal`, `Dialog` | `Dialog`, `AlertDialog` |
| `Popover`, `Tooltip` | `DialogTrigger` + `Popover`; `TooltipTrigger` + `Tooltip` | `Popover`, `Tooltip` |
| `TextField`, `TextArea`, `SearchField` | `TextField`, `TextArea`, `SearchField` | native inputs + `Label` |
| `Select` | `Select`, `ListBox` | `Select` |
| `Checkbox`, `RadioGroup`, `Switch` | `Checkbox`, `RadioGroup`, `Switch` | `Checkbox`, `RadioGroup`, `Switch` |
| `SegmentedControl` | `ToggleButtonGroup` (single selection) | `ToggleGroup` |
| `Slider`, `NumberField` | `Slider`, `NumberField` | `Slider`; none |
| `Tabs`, `Breadcrumb`, `Toolbar` | `Tabs`, `Breadcrumbs`, `Toolbar` | `Tabs`; none; `Toolbar` |
| `ListRow`, `DataTable` | `GridList`, `Table` | none |
| `Expander` | `Disclosure` | `Collapsible` |
| `Toast` | `Toast` (unstable API) | `Toast` |
| `ProgressBar` | `ProgressBar` | `Progress` |

**Why not material-web.** It is in maintenance mode, with no new features or components planned, and the maintainers have said Expressive is not planned for it. The stable `md-*` elements run on the 2023 token set, render inside shadow DOM where our glass container cannot reach, ship no density, motion or spacing tokens, default to Roboto and leave dark mode to the app. Several components we need were never built: navigation rail, sheets, snackbar, search, tooltip, data table. The labs suite (`md-gb-*`) is Expressive but explicitly experimental and may break in minor releases.

**What to borrow from it.** Treat the labs suite as a reference implementation and copy patterns, never the package: the class-contract "baseline DOM" on native elements, `@layer` ordering so overrides are predictable, `light-dark()` colors, springs converted to `linear()`, `focusgroup` with a roving-tabindex fallback, `:state()` for custom states, `soft-disabled` (disabled but focusable inside toolbars and menus), the `ElementInternals` form-association mixins for any custom element, and its `forced-colors` handling. Vendor any code at a pinned commit and keep the Apache-2.0 notices.

**Accent families from Material Color Utilities.** A new product theme starts from a seed color. MCU proposes the family; the parent's contrast solver decides it.

```ts
import { Hct, TonalPalette, argbFromHex, hexFromArgb } from '@material/material-color-utilities';

/** Candidate accent family for a product seed. Candidates only: the contrast build
 *  moves each one until it holds its floor over the worst ground, then writes the theme. */
export function accentCandidates(seed: string) {
  const p = TonalPalette.fromHct(Hct.fromInt(argbFromHex(seed)));
  const t = (tone: number) => hexFromArgb(p.tone(tone));
  return {
    light: { accent: t(40), 'accent-text': t(30), 'accent-soft': t(50) },
    dark: { accent: t(80), 'accent-text': t(90), 'accent-soft': t(70), 'text-on-accent': t(10) },
  };
}
```

HCT tone differences predict contrast, which makes MCU a good first guess; the solver in the token build then nudges lightness in OKLCH against the worst-case grounds, as it did for the parent's Near AI blue (`brand-blue` #0091fd stepped to `accent` #035ca3 light and #7ebcff dark). Run MCU at build time only. A runtime seeded theme is out of scope until a product asks for one.

[material-web: status, recommendations] [trace-commons: Tauri on main]

## Testing

Four kinds of tests keep every platform honest. Each runs in CI as a required check.

**Contrast, per theme, over the worst ground.** Port trace-commons' `FlatThemeContrastTests` model to every theme and every platform. Glass is see-through, so the ground behind text is whatever desktop is behind the window; the test assumes the worst one the glass passes nearly unchanged: pure white under the dark themes, #333333 under the light ones (light glass frosts a dark desktop no darker than that). Composite in sRGB, alpha over, in layer order.

```python
def grounds(t, theme):
    desk = WHITE if is_dark(theme) else hex_rgb('#333333')
    pane = over(over(desk, t['glass-veil']), t['pane-fill'])
    return {
        'pane': pane,
        'card': over(pane, t['card']), 'card-quiet': over(pane, t['card-quiet']),
        'field': over(pane, t['field']), 'control': over(pane, t['control']),
        'popover': over(desk, t['popover']), 'menu': over(desk, t['menu']),
        'pane-opaque': t['pane-opaque'],
    }

for theme in THEMES:
    t, floor = tokens[theme], (7.0 if theme.endswith('-hc') else 4.5)
    for name, ground in grounds(t, theme).items():
        for role in TEXT_ROLES:                     # text-primary … destructive-text
            check(theme, role, name, contrast(over(ground, t[role]), ground), floor)
        check(theme, 'accent', name, contrast(t['accent'], ground), 3.0)
        check(theme, 'focus-ring', name, contrast(t['focus-ring'], ground), 3.0)
```

The full matrix:

| Check | Floor |
|---|---|
| Every text role (`text-primary`, `-secondary`, `-tertiary`, `-placeholder`, `accent-text`, the three status `-text` roles, `destructive-text`) on pane, card, quiet card, field, control, popover, menu and `pane-opaque` | 4.5:1; 7:1 in `-hc` |
| `text-on-accent` on `accent`, on `accent-pressed`, and on `menu-hover` over `menu` | 4.5:1; 7:1 in `-hc` |
| `text-on-status` on `badge-fill` | 4.5:1; 7:1 in `-hc` |
| `accent` as a selected fill, and `focus-ring`, on every ground | 3:1 |
| `positive`, `caution`, `critical`, `neutral`, `accent-soft`, `tab-ember` on `pane-opaque` | 3:1 |
| `data-1` to `data-8` on `surface-chart` | 3:1 |
| `toolbar-glyph-off` on `control` over the pane | 3:1 |
| `edge-hc` on every ground, `-hc` themes | 3:1 |

Write one shared checker (one linearization threshold, 0.04045) and call it from every platform's suite; trace-commons has six Swift copies plus Python, C# and Rust with two thresholds between them. Known failures would be listed in `contrast-report.json` and kept visible as expected failures; there are none today. A new failure fails the build. The tests model glass composites; they never measure a device, so the release that ships a new shell also records an on-device check over a pure white and a pure black wallpaper.

**Token drift.** Every generator runs with `--check` in CI. Each platform also decodes `tokens.json` in a unit test and compares every generated constant, every theme included: XCTest for Swift, a JUnit test for Kotlin, a Vitest test that parses `tokens.css`. A CSS lint fails any color, size, radius, shadow, blur, duration or easing literal in a part file that is not one of the allowed literals, and any `nr-` class outside its component's prefix.

**Visual previews.** Render every component in at least `light`, `dark`, `gateway-dark` and `light-hc`, over the scene and over a busy image:

- this artifact's component cards (`preview.html` in each folder);
- the TCDesign gallery (`swift run TCDesignGallery`) and a SwiftUI `#Preview` per theme;
- Compose `@Preview` per theme with screenshot tests (Paparazzi or Roborazzi);
- a Storybook-style web catalog with a theme switcher, and Playwright screenshots in CI.

**Accessibility audits.** Automate what can be automated and do one manual pass per release:

- **Web:** axe-core in Playwright; keyboard traversal tests (Tab order, Escape, Return, the visible focus ring); emulated `forced-colors`, `prefers-contrast: more`, `prefers-reduced-motion` and `prefers-reduced-transparency`; 200% text zoom.
- **Apple:** `performAccessibilityAudit()` in XCUITest; Dynamic Type to AX5 and the macOS text sizes; VoiceOver with Reduce Transparency, Increase Contrast and Reduce Motion on.
- **Android:** Espresso `AccessibilityChecks`, Compose semantics assertions, a 200% font scale run and a TalkBack pass.
- **All:** targets measured against `target-pointer` 28, `target-touch-apple` 44, `target-touch-android` 48 and `target-spatial` 60. A product that turns the focus ring off (`.nr-focus-off`, as Gateway does) fails WCAG 2.4.7, and its audit says so.

[trace-commons: FlatThemeContrastTests.swift, test inventory, CI] [HIG: accessibility]

## Fonts

Each platform draws its own system face on the one step scale (NDS-4).

| Platform | Face | How |
|---|---|---|
| macOS, iOS, iPadOS, visionOS | SF Pro, SF Mono | Text styles (`.body`, `NSFont.preferredFont(forTextStyle:)`) and `.monospaced()`; never a named font or point size |
| Android | Roboto Flex, Roboto Mono | Bundle the variable font in `res/font` (or the downloadable-fonts provider); weights through `FontVariation.Settings`; Roboto is the fallback |
| Windows (WinUI, Tauri) | Segoe UI Variable, Cascadia Mono | The system face; `--font-web` lists it before Segoe UI |
| Linux (GTK, Tauri) | the system UI face (Cantarell, Ubuntu, Noto) | `system-ui` through fontconfig |
| Web | the visitor's system face | `--font-web` and `--font-mono` stacks; no web font by default |

Rules:

- Never ship SF Pro or SF Mono as a web font or inside a non-Apple build. SF is licensed for Apple platforms only. The web stack names it through `-apple-system` so Apple devices use their installed copy.
- Roboto Flex and Roboto Mono are under the SIL Open Font License. A web product that needs one face across platforms may self-host Roboto Flex with `font-display: swap`; that is a product decision, and the parent ships no web font.
- Figures use tabular digits everywhere a number can change: `.monospacedDigit()` in SwiftUI, `fontFeatureSettings = "tnum"` in Compose, `font-variant-numeric: tabular-nums` on the web (`.nr-tabular`).
- Text scales with the person's setting on every platform: Dynamic Type and the macOS text size, Android font scale in sp, browser zoom and font size in rem. Controls grow with their labels; heights in the tokens are minimums.

[trace-commons: Tauri fonts] [M3: typography] [HIG: typography]
