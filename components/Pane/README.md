# Pane

A pane is the outermost glass container of the navigation layer: windows are built from panes that float 10 apart with no chrome around them, and everything inside a pane is painted, never blurred again.

## When to use

- A window region: the main pane (navigation, tabs, toolbar), the inspector, the settings body, the menu-bar panel, the edge-rail peek. The first-run stage has no pane: its cards sit on the scene as `scene-card` (NDS-32).
- Web and Windows/Linux shells: the app's panels over the `.nr-scene`.
- Not to group content inside a pane (`Card`), and never a pane on a pane: a sheet's body is a padded column (`Sheet`), not another pane.
- Phones and tablets: the screen itself is one opaque pane; bars float over it as glass.

## Anatomy

1. **Surface** `.nr-pane`: `glass-veil` and `pane-fill` over `blur-pane`, `shadow-float`, radius `radius-pane` 20, padding `pane-padding` 12.
2. **Insets**: `--inspector` 16 by 18 (`inspector-padding-x`, `inspector-padding-y`); `--flush` 0 for edge-to-edge lists, clipping its content.
3. **Content layer** `--content`: `pane-base` with no blur, for maps, graphs and charts. Glass controls floating on it are then never glass on glass.
4. **Three-pane window** `.nr-pane-layout`, panes `pane-gap` 10 apart with no window padding:
   - **Main** `__main`: 440 by default (`size-pane-main`), always shown. It holds the toolbar, the tabs and the traffic lights in a 78 by 30 clearance (`Toolbar`).
   - **Divider**: between the main and content panes, a resize target in the 10 gap with nothing drawn. Dragging it moves width between the two; both widths are remembered (NDS-35).
   - **Content** `__content`: at least 360 (`size-pane-content-min`), opens at 440; takes window resizes. Usually `--content`.
   - **Inspector** `__inspector`: 293 (`size-pane-inspector`, two thirds of the main pane), fixed, with `--inspector` insets.
   - Default window 1193 by 614 (440 + 10 + 440 + 10 + 293); minimum height 560; the main pane alone is the narrowest window. A window opens sized to the panes it shows (890 with the inspector hidden).

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Padding | 12; inspector 16 × 18 | 12; inspector 16 × 18 | screen margins 16, 24 from 600 | 16, 24 from 600 | 18 left, 4 right, 8 top and bottom (`dense-padding-left`) |
| Radius | 20 | 20 (window 22) | full screen; sheets `radius-sheet` | full screen; sheets `radius-sheet` | 20 |
| Gap | 10 | 10 | none (one pane) | none | 10 |
| Material | native glass (NDS-7) | `blur-pane` | opaque `pane-opaque` | `pane-base`, `blur-bar` on bars | as compact |

## Variants

- **Glass** (default), **content** (`--content`), **opaque** (`--opaque`, for Reduce Transparency on shells that paint their own glass, forced colors and the settings window body).
- **Inspector** (`--inspector`) and **flush** (`--flush`) insets.
- **Miniature** (`.nr-pane-layout--miniature`): documentation only; draws a window at 0.6 scale.

## States

| State | Treatment |
|---|---|
| Active window | as drawn |
| Inactive window (`--inactive`) | `inactive-dim` over the pane, so background windows read darker |
| Reduce Transparency | Apple platforms: the system's to apply; the native material frosts itself and the painted veil and fill stay (NDS-23). Web, Windows, Linux and Android: `pane-opaque`, no blur |
| No backdrop support | `pane-base` |
| Increased contrast | a 1px `edge-hc` inset edge |
| Forced colors | system Canvas with a CanvasText border |
| Hidden | removed; it reserves no space |

## Behavior

- **Opening and closing**: opening a pane grows the window to its right by the pane and its gap; closing shrinks it from the right by the same. No other pane moves or changes width, and each pane keeps a width the person dragged it to. A window that would run off the screen slides left only as far as it must, with its right edge on the screen edge and the main pane's width kept; closing a pane leaves the left edge where it is, with no snap back. The window stays on its display, and AppKit keeps it on screen at launch (NDS-35).
- **Resizing**: the content pane takes window resizes. While the window edge is dragged, panes follow the frame directly; their widths never animate frame by frame. With the content pane hidden, the main pane takes the width.
- **First launch**: show the content pane when the screen is at least 1100 wide (`bp-map`) and the inspector from 900 (`bp-inspector`). After that, restore each window's own choice.
- **Motion**: the window edge and the pane's fade run together on `duration-standard` with `ease-standard`. Under Reduce Motion, and in full screen, the panes change at once.
- **Toggles**: every pane has a toolbar toggle, a View menu item and a shortcut. Events may open the inspector; nothing closes it on its own. On a tab with no detail the inspector's toggle is disabled with a reason.
- **Web**: under 1200 (`bp-large`) the inspector becomes a side sheet over the content pane; under 840 (`bp-expanded`) one pane shows at a time, with back navigation between them.

## Accessibility

- Each pane is a named landmark (`nav`, `main`, `aside` or a labelled `section`); focus order follows the panes left to right, and a shortcut (F6 on web) moves focus between panes.
- Text on a pane is measured over the worst-case ground: a white desktop under dark glass and #333333 under light glass. `glass-veil` exists to hold 4.5:1 there.
- Charts never plot on glass: use `--content` or a `surface-chart` card.
- **The product supplies**: each pane's content and landmark name, and which panes a window shows.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| `GlassPane` over `NSGlassEffectView` `.regular` tinted with the veil (vibrancy on 14 to 25); `GlassThreePane` in a `glassWindow()` with a hidden title bar | `NavigationSplitView` columns with system glass on the sidebar; app-drawn panes painted per NDS-7; phones show one column | `ListDetailPaneScaffold` and `SupportingPaneScaffold` on `pane-base`; `blur-bar` (RenderEffect) on API 31+ | `.nr-pane` with `backdrop-filter`; `.nr-pane-layout` |

## Do and don't

- Do let the content pane absorb window resizes, and let the person move the divider between the main and content panes.
- Do put graphs and maps on a content-layer pane.
- Don't nest panes or blur anything inside a pane.
- Don't reflow the other panes when one opens.
- Don't put text on the scene outside a pane.

## Source

`GlassPane`, `GlassPaneInsets.inspector` and `GlassSheet` in `macos/Sources/TCDesign/Components/Surfaces.swift`; `GlassPaneLayout` and `GlassThreePane` in `ThreePane.swift` (main 440 by default, inspector 293, map opening at 440 with a 360 minimum, 10 gaps, no window padding, the window grows to the right, first launch at 1100 and 900, a 78 by 30 window-controls inset); the main and content divider with remembered widths (2026-10-19/20); `GlassPaneLayout.windowFrame(onScreen:width:visible:)`, the slide-left placement (owner, 2026-10-30, #1775); `glassWindow()` in `GlassBackdrop.swift`, where Reduce Transparency is left to the system (R14).
