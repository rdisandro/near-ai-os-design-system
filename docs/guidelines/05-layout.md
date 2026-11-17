# Layout, density and targets

Lay out by the width you actually have, size controls by the input in use, and never let a touch target shrink. Units are points on Apple, dp on Android and CSS px on the web; all three are about 160 per inch, so one number serves all three.

## Layout classes

Classify every window, pane or container by its own width, using Material 3's breakpoints on every platform (decision NDS-12).

| Class | Width | Typical | Panes | Primary navigation | Margin |
|---|---|---|---|---|---|
| Compact | under 600 | Phones in portrait, narrow split views | 1 | Bottom tab bar or navigation bar | `margin-compact` 16 |
| Medium | 600 to 839 | iPad portrait, foldables open, narrow web | 1, or 2 at 50/50 for low-density content | Collapsed rail (Android, web); iPad tab bar that can become a sidebar | `margin-medium` 24 |
| Expanded | 840 to 1199 | iPad landscape, small desktop windows | 2 (list-detail) | Rail or sidebar | 24 |
| Large | 1200 to 1599 | Laptop windows, iPad 13" landscape, visionOS default window | 2 to 3 | Expanded rail or sidebar | 24 |
| Extra-large | 1600 and up | Desktop displays | 3 (third is an inspector, at most 400) | Sidebar | 24, with a maximum content width |

Height classes: compact under 480 (phones in landscape: hide or minimize bars, keep one pane), medium 480 to 899, expanded 900 and up.

Apple's binary size classes only choose idiom-specific components: a tab bar or a sidebar, a sheet or a popover. An iPhone Pro Max in landscape is regular width but compact height for Apple and expanded width for Material; give it one pane and minimized bars. Use container queries on the web, `GeometryReader` or `containerRelativeFrame` on iOS, and `WindowSizeClass` with large and extra-large widths enabled on Android.

## The desktop window

The lead desktop layout is trace-commons' floating three-pane window (`Pane`):

| Pane | Width | Behavior |
|---|---|---|
| Main (navigation) | `size-pane-main` 440 by default | Always shown; holds the tabs and the list or tree. A divider moves width between it and the content pane; with the content pane hidden it takes the width |
| Content (map, document, canvas) | flexible, minimum `size-pane-content-min` 360 | Takes window resizes; content layer |
| Inspector | `size-pane-inspector` 293 (two thirds of main) | Opens on demand (a selection, a review); nothing closes it automatically |

Panes float `pane-gap` 10 apart with no window padding; opening a pane grows the window to the right by the pane plus its gap and closing one shrinks it from the right, so nothing else moves. Near the screen edge the window slides left just enough to show the new pane, and closing never snaps it back (NDS-35). Pane widths are remembered per window. On first launch the window shows the inspector at a screen width of `bp-inspector` 900 and the content pane at `bp-map` 1100. The default window is 1193 by 614; the traffic lights sit inside the main pane, which reserves 78 by 30 for them.

Lay tab content out for the main pane's default first: at 440 with 16 insets the content is 408 wide, one column, two columns above about 690. The first element of every tab sits 16 below the tab bar; the pane owns that gap.

Other desktop measures: modals 780 wide (regular) or 450 (narrow); a settings section list 180; popovers and node cards 260; menus at least 220; the menu-bar panel 285 (NDS-33); edge-rail peeks and tray flyouts 380 (`size-panel-width`); the first-run stage 860 by 760, scaled to fit (NDS-32).

## Margins, gutters and spacing

- Page margins: 16 below 600, 24 from 600. On Apple, respect the readable content guide and safe areas; on Android, the window insets; on the web, `env(safe-area-inset-*)`.
- Inside panes: `pane-padding` 12, cards `card-padding-y` 12 and `card-padding-x` 14, `card-gap` 10 between cards, `inline-gap` 6 between a dot or icon and its words.
- Inside a section card, body text sits `space-10` further in than the card's title and its bottom actions. Nested containers (chart wells, quiet cards, row cards, dashed boxes) give that inset back and line up with the title. Text inside a container gets `space-8` more on each side; quote and warning boxes keep the container's edge.
- The spacing scale is `space-2` to `space-16` in steps of 2, then `space-20` and `space-24` inside components; `space-32`, `space-40`, `space-48` and `space-64` separate page sections on the web and tablets.
- Space sibling groups with gap, not margins on each element.
- Keep running text within `size-readable-width` 680; on wide screens widen the margins or add panes, never the measure.

## Density

Density follows the input, not the screen size.

| Density | Where | Inline control | Bar button | Row | Gap between fields | Type tier |
|---|---|---|---|---|---|---|
| Compact | macOS and pointer-first desktop | `size-control-large` 28 (26 for round and segment) | `size-cta` 34 (modals `size-cta-small` 30) | `size-list-row` 40 | 8 | `mac-` |
| Regular | Web and the Windows and Linux shells | 28 | 34 | 40 | 8 | `web-` |
| Touch | Phones, tablets, touch web | `size-control-touch` 44 (iOS); 40 visible in a 48 target (Android) | 44 / 48 | 44 iOS, 56 Android | 12 | `ios-`, `android-` |
| Dense | Pro-tool panels: inspectors, property grids, consoles | `size-control-dense` 20 | 28 | 20 | 2 | `mac-` |

Apply density to a container (`.nr-compact`, `.nr-regular`, `.nr-touch`, `.nr-dense`); every control inside reads its height from the container. Mixed input devices (an iPad with a trackpad, a touch laptop) use touch density unless the person chooses otherwise.

The macOS ladder keeps trace-commons' sizes (decision NDS-7): 26 for round buttons and segments, 28 inline, 30 in modal action bars, 34 for the primary action and every button in a window or sheet action bar. The system's own controls on macOS 26 and 27 measure 24, 28 and 36; native controls keep their own sizes where the parent uses them unstyled.

## Targets

| Input | Recommended | Minimum | Spacing |
|---|---|---|---|
| Touch on iOS and iPadOS | `target-touch-apple` 44 | 28 | About 12 around bordered controls, 24 around borderless ones |
| Touch on Android and touch web | `target-touch-android` 48 | 48 | 8 between targets |
| Pointer on macOS and desktop web | `target-pointer` 28 | 20 | Hit areas never overlap |
| Gaze and pinch on visionOS | `target-spatial` 60 | 60 | Centers 60 apart, or 16 margins |

A control smaller than the target gets an invisible hit area extended to it (an `::after` inset on the web, `contentShape` on Apple, `minimumInteractiveComponentSize` on Android). Never extend a hit area over a neighbor's. trace-commons' smallest pointer targets (the kebab at 22 by 24, toolbar buttons at 28 by 24) meet the pointer minimum; on touch they grow to the touch target.

## Hover is never the only way

Every hover behavior needs a keyboard, tap or long-press equivalent: info popovers pin on click and on Return; map node cards show on focus; chart values show on focus and in the table view; the edge rail opens from its handle's accessibility action. Touch platforms show no hover-only content.

## Reflowing panes

| From | To compact | To medium | To expanded and up |
|---|---|---|---|
| Three-pane window | One pane; content and inspector push as pages | Main plus content; inspector as a side sheet | All three |
| Inspector | Sheet at the large detent | Side sheet, modal | Docked pane |
| Map or canvas | Full screen with a floating toolbar | Second pane | Content pane |
| Settings with section list | List, then page | List-detail | List-detail |

Move between layouts by the class, never by device name, and keep the selection and scroll position across the change.
