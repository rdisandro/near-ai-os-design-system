# Breadcrumb

A breadcrumb shows where a sub-page sits inside its pane and takes the person back up: a bare back chevron, then the trail of parent pages, ending in the current page's title.

## When to use

- Sub-pages inside a pane: Traces › History, Missions, Mission drafts. A sub-page lives under the tab whose content it extends (Gateway moved History into Traces).
- Web pages two or more levels deep (Agents › Research agent › Run 14).
- Not for top-level destinations (`Tabs`, `Sidebar`), not for a sequence (`StepProgress`), and not as the only way back on a phone, where the platform's back control leads.

## Anatomy

1. **Back button** `.nr-breadcrumb__back`: a chevron glyph, 12 (`space-12`) on desktop and 20 on touch, semibold weight, no container. The target is 26 (`size-control`) on macOS, `--nr-target` elsewhere. It pulls the trail 4 closer so the first crumb keeps its place.
2. **Trail** `.nr-breadcrumb__list`, an ordered list. Crumbs `.nr-breadcrumb__crumb` are links in `text-secondary`, each with a hit area 6 above and below the text (28 tall at the label step).
3. **Separator**: a `›` in `text-tertiary`, drawn by CSS and silent to screen readers. Gateway's macOS shell draws a `/` (`--slash`); a product picks one separator and keeps it everywhere.
4. **Current page** `.nr-breadcrumb__current` in `text-primary`, a heading, truncating with an ellipsis when space runs out.

Every part uses the label step at semibold, 4 apart.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Back target | 26 | 28 | 44 (system back) | 48 (system back) | 20 |
| Chevron | 12 | 12 | 20 | 20 | 12 |
| Type | `mac-label` | `web-label` | `ios-label` | `android-label` | `mac-label` |
| Crumb hit height | 28 | 28 | 44 | 48 | 20 |

## Variants

- **With back** (desktop panes): the chevron goes to the parent page.
- **Trail only** (web pages): the browser has back, so the trail starts at the section.
- **Collapsed** (`--collapsed`, compact width): the back button and the current title only. The back button's name carries the parent ("Back to Agents").

## States

| State | Treatment |
|---|---|
| Crumb and back, default | `text-secondary` |
| Hover | `text-primary`, no fill |
| Pressed | the text darkens (`filter: brightness(0.92)`); there is no fill to press |
| Current | `text-primary`, not interactive |
| Focus | 2px `focus-ring`, 2px outside (NDS-5) |
| Long trail | the current title truncates first; parents never shrink below their words |

## Behavior

- **Keyboard**: each crumb and the back button are in tab order; Return activates. In a pane sub-page, Escape goes back (macOS) as the back button does.
- **Pointer**: a crumb jumps straight to that page. The back button goes to the parent, never to browser history.
- **Motion**: the breadcrumb itself never animates. Page changes use the platform's navigation transition, and nothing moves under Reduce Motion.

## Accessibility

- A `nav` with an `aria-label` from the product ("Breadcrumb"), an `ol` inside, and `aria-current="page"` on the current title, which is also the page heading.
- The back button is icon-only, so it needs a name and a tooltip from the product's copy ("Back to Home"). The chevron and the separator are hidden.
- `text-secondary`, `text-tertiary` and `text-primary` all hold 4.5:1 over the worst-case ground.
- **The product supplies**: the trail's titles and destinations, the back button's name, and the navigation label.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| Custom `GlassBreadcrumb` inside a pane; standard windows use the toolbar's back button | System back in the navigation bar (`NavigationStack`); the parent titles live in the back button's long-press menu. No trail | Top app bar navigation icon and predictive back. No trail | Custom: `nav > ol`, this CSS (WAI-ARIA breadcrumb pattern) |

## Do and don't

- Do use the page titles the person already saw, word for word.
- Do keep the back chevron bare: a symbol with no "Back" word and no round container (HIG toolbars).
- Don't show a trail of one; a top-level page needs no breadcrumb.
- Don't put actions, filters or status into the trail.
- Don't repeat the current title as a second heading under the breadcrumb.

## Source

`GlassBreadcrumb` and `GlassCrumb` in `macos/Sources/TCDesign/Components/Navigation.swift`: a bare back chevron (owner, 2026-10-08) on a `size.control` 26 target with a 12pt semibold glyph; crumbs secondary, separator tertiary ("/" since 2026-10-12), current primary with the header trait; crumbs turn primary under the pointer (#1146 `.tc-breadcrumb__crumb:hover`). Used for sub-pages in `Views/MonitorWindowView.swift` ("Traces / History" since 2026-10-12), where Escape goes back.
