# Platform crosswalk

This section maps every part of the system to what each platform calls it and ships. Use it to find the native control to build on, the trace-commons type a component comes from, and the M3, Apple and Unity names for the same idea. The rule behind every row is NDS-3: one token and semantics layer, native idioms where they exist. Where a column names a native control, use it and dress it with the tokens. Where it says "custom", draw our component from the tokens. Where the trace-commons column says "addition", TCDesign has no type and the component card says where the design came from.

How to read the columns:

- **trace-commons** is the TCDesign type in `macos/Sources/TCDesign` (file in the component card's Source section).
- **macOS** and **iOS, iPadOS** list SwiftUI first, then AppKit or UIKit.
- **Android** is Jetpack Compose Material 3, including the Expressive APIs in Compose Material3 1.4 and 1.5.
- **Web** is our component (the `nr-` class from `components/bundle.css` on a native element or a headless primitive), then the closest material-web element for reference only (NDS-18). `md-gb-*` elements are the unstable labs suite.
- **Unity** lists the App UI 3.0 type, then the UI Toolkit element (UITK) where the Editor has one.

## Components

Rows follow the catalogue groups: Actions, Presentation, Inputs, Navigation, Containers, Data, Feedback, AI, Brand.

| Component | trace-commons | macOS | iOS, iPadOS | Android (Compose M3) | Web (ours; material-web ref) | Unity (App UI; UITK) |
|---|---|---|---|---|---|---|
| `Button` | `GlassButtonStyle` (`.primary`, `.secondary`, `.glass`, `.submit`, `.link`, `.destructive`), `GlassButtonSize` | `Button` + custom `ButtonStyle`; `NSButton` | `Button` + `.glassProminent` / `.glass` in bars; `UIButton.Configuration` | `Button`, `FilledTonalButton`, `OutlinedButton`, `TextButton` (XS-XL) | `.nr-button` on `<button>`; `md-filled-button`, `md-gb-button` | `Button` (accent, quiet); UITK `Button` |
| `IconButton` | `GlassRoundButton` (with `isOn:` as a toggle), `GlassRoundMenu`, `GlassPillIconButton`, `GlassToolbarButton`, `GlassKebab`, `GlassInfoButton`; refresh is `GlassRefreshPill` (a labelled `Button`, NDS-36) | `Button { Image }` + `.help()`; image `NSButton` | `Button` + `.buttonBorderShape(.circle)`; `UIButton` | `IconButton`, `FilledTonalIconButton`, `IconToggleButton` | `.nr-icon-button` + `aria-label`; `md-icon-button` | `IconButton`, `ActionButton`; UITK `ToolbarButton` |
| `SplitButton` | `GlassSplitButton` | `Menu(primaryAction:)`; `NSComboButton` | `Menu(primaryAction:)`; `UIButton` with `menu` | `SplitButtonLayout` (Expressive) | `.nr-split-button`; `md-gb-split-button` | none (`Button` + `MenuTrigger`) |
| `ActionBar` | `GlassActionBar`, `GlassActionNote` | custom footer row in the window or sheet | sheet `.toolbar` with `.cancellationAction` / `.confirmationAction` | dialog button row; custom `Row` | `.nr-action-bar`; `md-dialog` `actions` slot | `Dialog` button group (App UI `ActionBar` is a selection bar) |
| `Menu` | `GlassMenu`, `GlassMenuItem`, `GlassMenuSeparator`, `GlassMenuRowStyle`, `GlassIconMenu` | `Menu`, `.contextMenu`; `NSMenu` | `Menu`, `.contextMenu`; `UIMenu` | `DropdownMenu`, `DropdownMenuItem` (Expressive groups) | `.nr-menu` on `[popover]`, `role="menu"`; `md-menu`, `md-gb-menu` | `Menu`, `MenuItem`, `MenuSection`; UITK `GenericDropdownMenu` |
| `CommandPalette` | addition | custom panel; menu bar Help search | custom; iPadOS menu bar and key commands | custom `Dialog` + `SearchBar` | `.nr-command-palette` (combobox in `<dialog>`) | none; Editor Search window |
| `Modal` | `GlassModal`, `GlassConfirmation`, `GlassModalAction`, `GlassModalBody` | painted modal host; `NSAlert` for system prompts only | `.sheet`, `.alert`, `.confirmationDialog`; `UIAlertController` | `AlertDialog`, `BasicAlertDialog`, full-screen `Dialog` | `.nr-modal` on `<dialog>`; `md-dialog` | `Modal`, `Dialog`, `AlertDialog` |
| `Sheet` | addition (`GlassSheet` is only the padded column inside a pane or modal) | `.sheet`, `.inspector` | `.sheet` + `.presentationDetents`; `UISheetPresentationController` | `ModalBottomSheet`, `BottomSheetScaffold` | `.nr-sheet` on `<dialog>` (tokens only in MWC) | `Tray`, `Drawer` |
| `Popover` | `GlassPopover`, `GlassNodeCard`, `GlassInfoButton` | `.popover`; `NSPopover` | `.popover` + `.presentationCompactAdaptation`; `UIPopoverPresentationController` | `Popup`, `RichTooltip` | `.nr-popover` on `[popover]` | `Popover`; UITK `PopupWindow` |
| `Tooltip` | none (system `.help()`) | `.help()`; `NSView.toolTip` | `.help()` (pointer only) | `TooltipBox` + `PlainTooltip` | `.nr-tooltip`, `role="tooltip"` | `Tooltip`; UITK `tooltip` property |
| `TextField` | `GlassTextField`, `glassFieldWell` | `TextField`, `SecureField` (`.plain` in the painted well); `NSTextField` | `TextField`; `UITextField` | `OutlinedTextField` | `.nr-text-field` on `<input>`; `md-outlined-text-field` | `TextField`; UITK `TextField` |
| `TextArea` | `GlassTextArea` | `TextEditor`; `NSTextView` | `TextField(axis: .vertical)`, `TextEditor`; `UITextView` | `OutlinedTextField(singleLine = false)` | `.nr-text-area` on `<textarea>` | `TextArea`; UITK multiline `TextField` |
| `SearchField` | addition (screens use `GlassTextField` focused by Cmd-F) | `.searchable`; `NSSearchField`, `NSSearchToolbarItem` | `.searchable`, `Tab(role: .search)`; `UISearchController` | `SearchBar`, `DockedSearchBar` | `.nr-search-field` in `role="search"` | `SearchBar`; UITK `ToolbarSearchField` |
| `Select` | `GlassSelect`, `GlassPicker`, `GlassPickerPill` | `Picker(.menu)` in the painted pill; `NSPopUpButton` | `Picker(.menu)`; `UIButton` menu | `ExposedDropdownMenuBox` | `.nr-select` on `<select>` or a listbox; `md-outlined-select` | `Dropdown`, `EnumField`; UITK `DropdownField` |
| `Checkbox` | `GlassCheckboxStyle`, `GlassCheckMark`, `GlassCheckRow` | `Toggle(.checkbox)`; `NSButton` checkbox | none: checkmark row or `Switch` | `Checkbox`, `TriStateCheckbox` | `.nr-checkbox` on `<input type="checkbox">`; `md-checkbox` | `Checkbox`; UITK `Toggle` |
| `RadioGroup` | `GlassRadioGroup`, `GlassRadio`, `GlassRadioRow` | `Picker(.radioGroup)`; `NSButton` radio | `Picker(.inline)` checkmark list | `RadioButton` in `selectableGroup()` | `.nr-radio-group`, `role="radiogroup"`; `md-radio` | `RadioGroup`; UITK `RadioButtonGroup` |
| `Switch` | `GlassToggleStyle`, `GlassSwitchKind` | `Toggle(.switch)`; `NSSwitch` | `Toggle`; `UISwitch` | `Switch` | `.nr-switch`, `role="switch"`; `md-switch` | `Toggle`; UITK none |
| `SegmentedControl` | `GlassSegmentedTabs`, `GlassSegment` | `Picker(.segmented)`; `NSSegmentedControl` | `Picker(.segmented)`; `UISegmentedControl` | connected `ButtonGroup` (Expressive) | `.nr-segmented-control`; `md-gb-button-group` connected | `ActionGroup` (compact); UITK `ToggleButtonGroup` |
| `Slider` | addition | `Slider`; `NSSlider` | `Slider`; `UISlider` | `Slider`, `RangeSlider` | `.nr-slider` on `<input type="range">`; `md-slider` | `SliderFloat`, `RangeSliderFloat`; UITK `Slider` |
| `NumberField` | addition | `TextField(value:format:)` + `Stepper`; `NSStepper` | `TextField(value:format:)` + `Stepper` | `OutlinedTextField` (number keyboard) | `.nr-number-field`, `role="spinbutton"` | `FloatField`, `IntField`, `Stepper`; UITK `FloatField` |
| `Chip` | `GlassChip` | custom capsule; `NSTokenField` for input | custom capsule | `AssistChip`, `FilterChip`, `InputChip` | `.nr-chip`; `md-filter-chip` | `Chip`; UITK none |
| `Tabs` | `GlassRuleTabs` (the Ember Rule) | custom | `Picker(.segmented)` at the top of content | `PrimaryTabRow`, `SecondaryTabRow` | `.nr-tabs`, `role="tablist"`; `md-tabs` | `Tabs`, `TabItem`; UITK `TabView` |
| `Breadcrumb` | `GlassBreadcrumb`, `GlassCrumb` | custom; `NSPathControl` | back button in `NavigationStack` | top app bar back action | `.nr-breadcrumb`, `aria-current="page"` | `Breadcrumbs`; UITK `ToolbarBreadcrumbs` |
| `Sidebar` | addition (the three-pane main pane; `GlassSectionNavRowStyle` in Settings) | `NavigationSplitView`, `List(.sidebar)`; `NSSplitViewController` | `NavigationSplitView`, `.sidebarAdaptable`; `UISplitViewController` | `WideNavigationRail` | `.nr-sidebar` in `<nav>`; `md-navigation-drawer` (superseded) | `Drawer` (permanent) |
| `NavigationRail` | addition | none (sidebar) | iPadOS `.sidebarAdaptable` tab view; visionOS tab ornament | `NavigationRail`, `WideNavigationRail`, `ModalWideNavigationRail` | `.nr-rail` | `NavigationRail` |
| `TabBar` | addition | none | `TabView` + `Tab`; `UITabBarController` | `ShortNavigationBar`, `NavigationBar` | `.nr-tabbar`; `md-navigation-bar`, `md-gb-nav-bar` | `BottomNavBar` |
| `Toolbar` | `GlassToolbarGroup`, `GlassToolbarButton`, `GlassFloatingGroup` | `.toolbar`, `ToolbarItemGroup`; `NSToolbar` | `.toolbar`, `ToolbarSpacer`; `UIToolbar` | `HorizontalFloatingToolbar`, `FlexibleBottomAppBar` | `.nr-toolbar`, `role="toolbar"`; `md-gb-toolbar` | `Toolbar`, `ActionGroup`; UITK `Toolbar` |
| `StepProgress` | `GlassStepProgress` | custom | custom | custom | `.nr-steps` on `<ol>` | `PageIndicator` (nearest) |
| `EdgeRail` | `EdgeRailGeometry`, `GlassRailTile`, `GlassRailHandle`, `GlassRailRule` | screen-edge `NSPanel` | none | none | `.nr-edge-rail` (desktop shells only) | none |
| `StatusItem` | `GlassMenuBarStrip` (`MenuBarPanel.swift`) | `NSStatusItem` with a non-template `NSImage` drawn per menu-bar appearance | none (Live Activities, widgets) | none (ongoing notification) | none; Windows and Linux shells use a template tray icon | none |
| `Pane` | `GlassPane`, `GlassThreePane`, `GlassPaneFill` | `NSGlassEffectView` / `NSVisualEffectView` + painted veil and fill | opaque screen pane; `.glassEffect` only in tier code | `Surface` + backdrop blur (API 31+) | `.nr-pane` | `SplitView`, `Pane`; Editor docked window |
| `Card` | `GlassCard`, `GlassIconCard`, `GlassEyebrowCard`, `GlassPromoCard` | custom; `GroupBox` nearest | inset grouped `Section`; custom | `Card`, `ElevatedCard`, `OutlinedCard` | `.nr-card`; `md-gb-card` | none |
| `GetStartedCard` | `GetStartedCard` (app target), `InsightsSampleBanner` | custom card | custom card | custom `Card` | `.nr-get-started` | none |
| `ListRow` | `GlassListRow`, `GlassOptionRow`, `GlassActivityRow` | `List` row; `NSTableView` row | `List` row; `UICollectionViewListCell` | `ListItem` (Expressive segmented) | `.nr-list-row`; `md-list-item` | `ListViewItem`; UITK `ListView` |
| `DataTable` | `GlassTableHead`, `GlassTableRow` (no sorting or scrolling) | `Table`; `NSTableView` | `Table` (one column on compact) | custom `LazyColumn` | `.nr-data-table` on `<table>` | `GridView`; UITK `MultiColumnListView` |
| `PropertyInspector` | addition (`GlassPaneInsets.inspector` + `GlassKeyValueList`) | `.inspector`, `Form`; `NSSplitViewItem` inspector | `.inspector` (sheet on compact), `Form` | `SupportingPaneScaffold` pane | `.nr-property-inspector` | `InputLabel` rows; Editor Inspector |
| `KeyValueList` | `GlassKeyValueList` | `LabeledContent`, `Grid` | `LabeledContent` | `ListItem` (headline + supporting) | `.nr-key-value-list` on `<dl>` | read-only `InputLabel` |
| `Expander` | `GlassExpander` | `DisclosureGroup` | `DisclosureGroup` | custom `ListItem` + `AnimatedVisibility` | `.nr-expander` on `<details>` | `Accordion`; UITK `Foldout` |
| `ConsentBlock` | `GlassConsentBlock` | custom | custom | custom | `.nr-consent-block` | none |
| `CodeBlock` | `GlassCode` | monospaced `Text` + `.textSelection(.enabled)` | same | `SelectionContainer` + mono `Text` | `.nr-code-block` on `<pre>` | `CodeBlock` |
| `StatCard` | `GlassStatCard`, `GlassLegendCell` | custom | custom | custom `Card` | `.nr-stat-card` | none |
| `BarGraph` | `GlassBarGraph`, `GlassBarBucket`, `GlassDayGraph` | Swift Charts `BarMark` | Swift Charts `BarMark` | custom `Canvas` | `.nr-bar-graph` (SVG + table) | none |
| `StatusLabel` | `GlassStatusLabel`, `GlassStatusDot` | custom `Label` | custom `Label` | custom `Row` | `.nr-status-label` | none |
| `Tag` | `GlassTag` | custom capsule | custom capsule | custom `Surface` | `.nr-tag` | non-clickable `Chip` |
| `Badge` | `GlassBadge` | `.badge()` on rows; custom | `.badge()` on `Tab` and rows; `badgeValue` | `Badge`, `BadgedBox` | `.nr-badge`; `md-badge` | `Badge` |
| `Notice` | `GlassNotice`, `GlassPopoverNotice`, `GlassPopoverStack` | custom quiet card | custom | custom `Card` (M3 banner is tokens only) | `.nr-notice` | `HelpBox`; UITK `HelpBox` |
| `InlineAlert` | `GlassAlert` | `Text` in `critical-text` | same | `supportingText` with `isError` | `.nr-inline-alert`, `role="alert"` | `HelpText` (destructive) |
| `Toast` | addition | custom glass banner (no system toast) | custom glass banner | `Snackbar`, `SnackbarHost` | `.nr-toast`, `aria-live="polite"`; `md-gb-snackbar` | `Toast`; `ShowNotification` |
| `Spinner` | `GlassSpinner` | `ProgressView()`; spinning `NSProgressIndicator` | `ProgressView()`; `UIActivityIndicatorView` | `CircularProgressIndicator`, `LoadingIndicator` | `.nr-spinner`; `md-circular-progress` | `CircularProgress` |
| `ProgressBar` | addition | `ProgressView(value:)`; bar `NSProgressIndicator` | `ProgressView(value:)`; `UIProgressView` | `LinearProgressIndicator` | `.nr-progress-bar` on `<progress>`; `md-linear-progress` | `LinearProgress`; UITK `ProgressBar` |
| `Skeleton` | `GlassSkeleton` | `.redacted(reason: .placeholder)` | same | custom placeholder | `.nr-skeleton`, parent `aria-busy` | `ListViewItem.isLoading` |
| `EmptyState` | addition | `ContentUnavailableView` | `ContentUnavailableView`; `UIContentUnavailableConfiguration` | custom | `.nr-empty-state` | none |
| `Message` | addition | custom | custom | custom | `.nr-message` in `role="log"` | `ThreadMessage` |
| `PromptComposer` | addition | `TextEditor` in the painted well + send `Button` | `TextField(axis: .vertical)` + send `Button` | `TextField` + `IconButton` | `.nr-prompt-composer` | `ThreadComposer` |
| `ProofTag` | addition (on `GlassTag`; `menuNoProof`) | custom | custom | custom | `.nr-proof-tag` | none |
| `ProofSeal` | addition (LibreChat `Seal.tsx`, `ProofGlyph`; no Gateway equivalent) | `Canvas` or `Path` from the key | same | `Canvas` `drawPath` | `.nr-proof-seal` (inline SVG) | none |
| `AgentRun` | addition (`GlassActivityRow`, `GlassSpinner`) | custom `DisclosureGroup` of steps | same | custom | `.nr-agent-run` on `<ol>` | `Thread` (nearest) |
| `ToolCall` | addition (`GlassToolTile`, `GlassTool`) | custom `DisclosureGroup` | same | custom | `.nr-tool-call` on `<details>` | `AccordionItem` (nearest) |
| `Logo` | `GlassBrandMark` (the "N" only), `GlassBrandMarkDrawing` (the N drawn on), `GlassNearWordmark` (the wordmark from the kit's paths) | vector asset `Image` | vector asset `Image` | `VectorDrawable` `Image` | `.nr-logo` inline `<svg>` | `Image` |

Rules the table implies:

- Apple has no checkbox on iOS, no system chip, tag, toast, stat card or tooltip on touch. Draw those from the tokens, and on iOS use a checkmark row or a `Switch` in place of a `Checkbox`.
- Apple has no FAB. The primary action is a prominent toolbar button (`.glassProminent` on iOS 26+, the `primary` `Button` kind in a Mac `ActionBar`). Android and web may use a FAB only where the M3 pattern calls for one.
- Native presentation on Apple wins for system-level prompts and sheets on touch. The painted `Modal` replaces `.sheet` and `.alert` inside the macOS app, as trace-commons does, so every confirmation follows the NDS-15 ladder.
- The material-web reference is a spec source. Never import `md-*` elements into a product surface.

[M3: §8b crosswalk] [Liquid Glass: API mapping] [trace-commons: components, Tauri React components] [Unity App UI: component catalog]

## Color roles

Our products read the parent tokens on every platform. The M3 and Apple columns name the role each token stands in for, which tells you which system color to replace when you wrap a native control (`.tint(accent)`, a Compose `ColorScheme` slot) and which system color a reviewer should expect to see. The M3 to Apple pairs follow the hybrid mapping: `primary` is the accent or tint, `on-surface` is `label`, `on-surface-variant` is `secondaryLabel`, `outline-variant` is `separator`, `surface` and `surface-container-*` are the system backgrounds of the content layer, and `error` aligns with `systemRed`.

Unity names are shortened. **E** is a Unity Editor variable (`--unity-colors-<name>`); **A** is an App UI variable (`--appui-<name>`).

| Parent role | trace-commons key (`glass.tokens.json`) | M3 color role | Apple semantic color or material | Unity |
|---|---|---|---|---|
| `scene`, `scene-warm` | `sceneBase`, `sceneWarm` | `surface-dim` | the desktop; iOS `systemBackground` | E `default-background`; A `backgrounds-50` |
| `scene-glow-1..3` | none (#1146 `--tc-scene-glow-1..3`) | none | none (wallpaper) | none |
| `glass-veil` | `glassVeil` | none; glass tint over `surface-container` | `NSGlassEffectView.tintColor` (a quarter of the veil) with the veil painted over; `UIGlassEffect.tintColor` | none (App UI has no translucency) |
| `pane-fill` | `paneFill` (gradient; one stop in flat) | none; part of the glass recipe | painted over the material | none |
| `pane-base` | `paneBase` | `surface-container` | `windowBackgroundColor`; iOS `systemBackground` | E `window-background`; A `backgrounds-100` |
| `pane-opaque` | `paneOpaque` | `surface` | the Reduce Transparency ground; `windowBackgroundColor` | E `window-background`; A `backgrounds-100` |
| `card` | `cardFill` (gradient) | `surface-container-high` | iOS `secondarySystemGroupedBackground`; macOS `quaternarySystemFill` | A `backgrounds-200` |
| `card-quiet` | `cardFillQuiet` | `surface-container-low` | macOS `quinarySystemFill` | A `backgrounds-200` |
| `card-hover` | `cardHover` | hover state layer (`on-surface` 8%) | none | A `base-200` |
| `control` | `controlFill` (gradient) | `surface-container-highest`; tonal `secondary-container` | `controlColor`; `.bordered` bezel | E `button-background`; A `alias-actions-background-color-default` |
| `control-hover` | `controlHover` | hover state layer | none | E `button-background-hover`; A `alias-actions-background-color-hover` |
| `well` | `wellFill` | `surface-container-highest` | `tertiarySystemFill` | E `slider_groove-background`; A `backgrounds-50` |
| `field` | `fieldFill` | `surface-container-highest` (filled field) | `textBackgroundColor`; iOS `tertiarySystemFill` | E `input_field-background`; A `alias-field-background-color-default` |
| `consent` | `consentFill` | `surface-container-low` | none | E `helpbox-background`; A `backgrounds-200` |
| `popover` | `popoverFill`, `nodeCardFill` | `surface-container` | material `.popover`; `NSPopover` | E `tooltip-background`; A `backgrounds-200` |
| `menu` | `menuFill` | `surface-container` (Expressive `surface-container-low`) | material `.menu` | A `base-100` + `alias-menu-border-color-default` |
| `scrim`, `scrim-modal` | `scrim`, `modalScrim` | `scrim` (32%) | system dimming behind sheets and alerts | A modal backdrop (black 40%) |
| `inactive-dim` | `inactiveDim` | none | inactive-window dimming (`controlActiveState`, `appearsActive`) | none |
| `hairline` | `hairline` | `outline-variant` | `separatorColor`, `separator` | E `default-border`; A `backgrounds-300` |
| `rule` | `rule` | `outline-variant` (divider) | `separatorColor` | E `toolbar-border`; A `base-400` |
| `edge-hc` | `edgeHighContrast` | `outline` (high-contrast scheme) | the Increase Contrast border; `accessibilityShowBorders` | A `alias-control-border-color-default` |
| `row-hover` | `rowHover` | hover state layer | none | E `highlight-background-hover`; A `alias-actions-quiet-background-color-hover` |
| `toggle-off` | `toggleOff` | switch track `surface-container-highest` | system switch track | A `alias-control-background-color-default` |
| `toolbar-glyph` | `toolbarGlyph` | `on-surface-variant` | `labelColor` | E `toolbar_button-text`; A `alias-icon-primary` |
| `toolbar-glyph-off` | `toolbarGlyphHidden` | `on-surface-variant` | `tertiaryLabelColor` | A `alias-icon-secondary` |
| `toolbar-expanded` | `toolbarExpanded` | `secondary-container` | toolbar item highlight | E `toolbar_button-background-checked`; A `alias-actions-selected-background-color-default` |
| `text-primary` | `textPrimary` | `on-surface` | `label`, `labelColor` | E `default-text`; A `alias-text-primary` |
| `text-secondary` | `textSecondary` (+ `textSecondaryHighContrast`) | `on-surface-variant` | `secondaryLabel` | E `label-text`; A `alias-text-secondary` |
| `text-tertiary` | `textTertiary` (+ `textTertiaryHighContrast`) | `on-surface-variant` | `tertiaryLabel` | A `foregrounds-50` |
| `text-placeholder` | `placeholder` | `on-surface-variant` | `placeholderText` | A `foregrounds-50` |
| `text-on-status` | `textOnStatus` | `on-error` | none | none |
| `accent` | `purple`, `controlSelected`, `toggleOn`, `ctaFill` (flat) | `primary` | `controlAccentColor`, `.tint()`, `accentColor` | E `highlight-background`; A `alias-actions-accent-background-color-default` |
| `accent-pressed` | `ctaFill` darkened by `GlassPress` | `primary` + pressed state layer | system pressed state | A `alias-actions-accent-background-color-active` |
| `text-on-accent` | `textOnAccent`, `textOnSelected` | `on-primary` | `alternateSelectedControlTextColor` | none (white) |
| `accent-text` | `purpleText` | `primary` as text | `linkColor` | E `link-text`; A `alias-control-foreground-color-selected` |
| `accent-soft` | `purpleSoft` | `primary` as a mark | `controlAccentColor` as a mark | A `accent-100` |
| `accent-tint` | `tintAccent` | `primary-container` | none | A `alias-actions-selected-background-color-default` |
| `tab-ember`, `tab-ember-halo` | `tabEmber`, `tabEmberHalo` | `primary` (tab indicator) | none | A `tabitem-indicator-emphasized-color` |
| `focus-ring` | none (system ring; #1146 `--tc-purple-text`) | `secondary` (focus indicator) | `keyboardFocusIndicatorColor` | E `button-border_accent-focus`; A `alias-control-outline-color` |
| `selection` | `selection` | `secondary-container` (list selection) | `selectedContentBackgroundColor` | E `highlight-background`; A `alias-highlight-background-color-default` |
| `menu-hover` | `menuHover`, `menuSelection` | `tertiary-container` (Expressive menu selection) | menu highlight | A menu hover (black 10%) |
| `positive`, `positive-text`, `positive-tint` | `statusOn`, `statusOnText`, `tintOn` | none; a custom role harmonized to `primary` | `systemGreen` | A `alias-semantic-positive` |
| `caution`, `caution-text`, `caution-tint` | `statusAsk`, `statusAskText`, `tintAsk` | none; a custom role | `systemOrange` | E `warning-text`; A `alias-semantic-warning` |
| `critical`, `critical-text`, `critical-tint` | `statusOutside`, `statusOutsideText`, `tintOutside` | `error`; `error-container` for the tint | `systemRed` | E `error-text`; A `alias-semantic-destructive` |
| `neutral`, `neutral-tint` | `statusOff`, `tintNeutral` | `outline` | `systemGray` | A `foregrounds-25` |
| `destructive-text` | `destructiveText` | `error` | `systemRed` (destructive role) | A `destructive-100` |
| `badge-fill` | `badgeFill` | `error` (badge) | system badge red | A `destructive-100` |
| `surface-chart` | none (`paneOpaque` under the map) | `surface-container-lowest` | `controlBackgroundColor` | A `backgrounds-100` |
| `chart-grid` | none (ink alphas) | `outline-variant` | `gridColor` | E `default-border` |
| `data-1..8` | `chartSeries1` to `chartSeries4` (Gateway's Shared and Kept pair stays product vocabulary) | none | Swift Charts default palette, replaced | A palette `color-<hue>-800` |
| `ink` | `ink` | `on-surface` at a state-layer alpha | `labelColor` at an alpha | A `transparent-black-*`, `transparent-white-*` |
| `brand-blue`, `brand-tile`, `brand-paper`, `brand-ink` | none (logo kit) | none | none | none |
| `gateway-purple` | `purple` | none | none | none |

Rules for the mapping:

- M3 has no glass roles. Every glass role has an opaque fallback that equals an M3 role: `pane-base` is `surface-container`, `pane-opaque` is `surface`. Under Reduce Transparency, forced colors, Android below API 31 and Linux, the fallback is what people see.
- Apple's own accent setting does not apply inside our apps. The root `.tint(accent)` replaces it, as trace-commons sets it at the window root. A Gateway window shows the parent's Near AI blue in both appearances (NDS-22).
- Never use Unity's saturated highlight blue or the M3 baseline purple as a stand-in. Both systems are benchmarks for structure only.
- Status roles have no M3 equivalent. On Android, keep them as custom roles beside `ColorScheme` (see Implementation) and never squeeze them into `tertiary`.

[M3: §8c item 6] [Liquid Glass: tint rules] [Unity Foundations: color variables] [Unity App UI: semantic and alias tokens]

## Type

One step scale, four renderings (NDS-4). Apple renders every step through a text style, so the macOS text size setting and Dynamic Type scale it; Android renders through M3 roles in sp; web uses rem on a 16px root. Sizes are size/line height.

| Step | macOS text style (compact) | iOS text style (touch, Large) | M3 role (Android) | Web (regular) |
|---|---|---|---|---|
| `micro` | `.caption2` 10/13 bold | `.caption2` 11/13 bold | `labelSmall` 11/16, 500 | 11/14 bold (0.6875rem) |
| `eyebrow` | `.caption2` 10/14 bold, +0.8 tracking, uppercase | `.caption` (caption1) 12/16 bold | `labelMedium` emphasized 12/16, 700 | 11/16 bold, +0.8 |
| `caption` | `.subheadline` 11/16 | `.footnote` 13/18 | `bodySmall` 12/16 | 12/16 (0.75rem) |
| `label` | `.callout` 12/16 medium | `.subheadline` 15/20 medium | `labelLarge` 14/20, 500 | 13/18, 500 |
| `body` | `.body` 13/18 | `.body` 17/22 | `bodyLarge` 16/24 | 14/20 (0.875rem) |
| `body-strong` | `.body` semibold 13/18 | `.headline` 17/22 semibold | `titleMedium` 16/24, 500 | 14/20, 600 |
| `title` | `.title3` 15/20 semibold | `.title3` 20/25 semibold | `titleLarge` 22/28 | 16/22, 600 |
| `heading` | `.title2` 17/22 semibold | `.title2` 22/28 bold | `headlineSmall` 24/32 | 20/26, 600 |
| `display` | `.title` 22/28 bold | `.title` (title1) 28/34 bold | `headlineMedium` 28/36 | 28/34, 700 |
| `number` | `.largeTitle` 26/34 bold, tabular | `.largeTitle` 34/41 bold, tabular | `headlineLarge` 32/40, 500, tabular | 32/40, 700, tabular |
| `mono` | `.subheadline` monospaced 11/16 | `.footnote` monospaced 13/18 | `bodySmall` in mono 12/16 | 12/18 mono |
| `hero-display` | not used | iPad heroes only, size from `@ScaledMetric` | `displayLarge` 57/64 | 57/64, 700 |
| `hero-figure` | not used | iPad heroes only | `displayMedium` 45/52 | 45/52, 700, tabular |

Rules:

- On Apple, name the text style and never a point size. trace-commons' generator fails when a step's size differs from its macOS text style's default, and the parent keeps that check.
- The iOS letter-spacing values in the `ios-*` styles are SF's built-in tracking at those sizes. They exist so web mockups of iOS screens match. Native code adds no tracking except the eyebrow's +0.8.
- Android emphasis is weight only (the M3 emphasized roles). Web and Windows shells use the `web-*` styles under Segoe UI Variable or the `system-ui` stack.
- Unity App UI sizes (body 12 at Small, 14 at Medium) sit close to `mac-body` 13 and `web-body` 14. A dense pro panel uses the `mac-*` steps under `.nr-dense`, never below 10.

[trace-commons: type tokens] [M3: typography] [HIG: typography] [Unity App UI: scale]

## Sizes and breakpoints

Units first. One Apple point, one Android dp and one CSS pixel are the same layout unit, about 160 to the inch. Text scales separately: Dynamic Type and the macOS text size on Apple, sp on Android, rem on the web.

### Layout classes

Classify by the window or container width (NDS-12), never by device. Apple size classes only pick idiom components.

| Parent class | Width | Token | Apple size class and where it lands | Android | Web query | Panes | Primary navigation (NDS-13) | Margin |
|---|---|---|---|---|---|---|---|---|
| Compact | under 600 | below `bp-medium` | iPhone portrait (compact × regular); iPhone landscape (compact × compact; Pro Max regular × compact); iPad Slide Over and narrow split | phone, folded foldable | `(max-width: 599px)` | 1 | bottom tab bar: iOS floating glass `TabBar`, Android 64dp bar | `margin-compact` 16 |
| Medium | 600-839 | `bp-medium` | iPad portrait, iPad half and two-thirds split (regular × regular) | tablet portrait, unfolded | `(600px <= width < 840px)` | 1 | iPad sidebar-adaptable tab bar; collapsed `NavigationRail` 96 | `margin-medium` 24 |
| Expanded | 840-1199 | `bp-expanded` | iPad 11" landscape, 13" portrait; iPhone Pro Max landscape; small Mac windows | tablet landscape | `(840px <= width < 1200px)` | 2 | expanded rail 220-360 or `Sidebar` | `margin-expanded` 24 |
| Large | 1200-1599 | `bp-large` | iPad 13" landscape; laptop Mac windows; visionOS default window 1280 × 720 | desktop windows | `(1200px <= width < 1600px)` | 2-3 | `Sidebar` or the three-pane window | 24 |
| Extra-large | 1600 and up | `bp-xlarge` | MacBook Pro 16", external displays | desktop | `(min-width: 1600px)` | 3 | `Sidebar`; three panes | 24; running text capped at `size-readable-width` |

Two desktop-only widths come from trace-commons: a window opens with the inspector pane from `bp-inspector` (900) and with the content (map) pane from `bp-map` (1100). On Compose, opt into the large classes with `currentWindowAdaptiveInfo(supportLargeAndXLargeWidth = true)`. On iOS, measure with `GeometryReader` or `containerRelativeFrame`. On the web, prefer container queries over viewport queries.

Height classes matter only for short windows: compact under 480 (iPhone landscape, compact vertical size class) keeps one pane and a minimized bar; expanded at 900 and up allows a top and bottom split.

### Control heights and targets

The parent ladder against each platform's own. NDS-7 keeps the Mac ladder 26 / 28 / 30 / 34 rather than the system's 24 / 28 / 36.

| Token | Value | macOS system | iOS, visionOS | Compose M3 | Unity App UI | Web density |
|---|---|---|---|---|---|---|
| `size-control-dense` | 20 | `.small` 20 | none | none | Small scale, md control 20 (Editor rows 18-20) | `.nr-dense` |
| `size-control` | 26 | `.regular` is 24 | none | none | Medium scale, sm 24 | compact small controls |
| `size-control-large` | 28 | `.large` 28 | visionOS mini 28 | XS button 32 (nearest) | Medium scale, md 30 | `.nr-regular` controls |
| `size-cta-small` | 30 | none | none | none | none | modal action bars |
| `size-cta` | 34 | `.extraLarge` is 36 | none | S button 40 (nearest) | Medium scale, lg 36 | action bars, the primary CTA |
| `size-control-touch` | 44 | none | iOS buttons, fields, rows; visionOS regular 44 | 40 visible in a 48 target | Large scale, lg 48 | `.nr-touch` |
| `target-pointer` | 28 (minimum 20) | pointer target | iPad pointer | precision-pointer sizing | hit padding round 16-24 controls | desktop web |
| `target-touch-apple` | 44 | none | every touch target | none | none | none |
| `target-touch-android` | 48 | none | none | `minimumInteractiveComponentSize` 48 | none | touch web |
| `target-spatial` | 60 | none | visionOS, centers 60 apart | XR 56 (use 60) | none | none |

Density tiers line up with App UI's scales: `dense` is App UI Small (the Editor density), `compact` and `regular` sit near App UI Medium, `touch` matches App UI Large. M3 density is a user opt-in that keeps 48dp targets; the parent never ships compact or dense on a touch-first device.

[M3: §8a breakpoints] [Liquid Glass: macOS control sizes] [Unity App UI: scale] [trace-commons: ThreePane.swift]

## Terminology conflicts

The same word means different things across the sources. Use the parent name in specs, code and copy reviews.

| Term | What it means where | Parent name and rule |
|---|---|---|
| Toggle | Unity Editor: a checkbox ("checkbox" is discouraged). App UI: a switch. SwiftUI `Toggle`: a switch on iOS, a checkbox by default in macOS forms. M3: a toggle button is a selectable button | `Checkbox` for forms, inspectors and multi-select; `Switch` for an immediate-effect setting. "Toggle" is never a component name |
| Segmented | M3 segmented buttons are no longer recommended; the connected button group replaces them. Apple: segmented control. App UI: compact `ActionGroup`. UITK: `ToggleButtonGroup` | `SegmentedControl`, two to five segments, for switching views inside a pane. Native on Apple; a connected button group look on Android and web |
| Navigation drawer | M3: deprecated, use the expanded navigation rail. App UI: `Drawer` (temporary or permanent). Apple: sidebar | No drawer. `Sidebar` on desktop and iPad, expanded `NavigationRail` on Android and web |
| Tabs | Apple tab bar: top-level destinations. macOS tab view: in-window pages. M3 tabs: peer content. App UI: top-level only. Unity Editor `TabView`: in-panel sections | `TabBar` for top-level destinations on phones; `Tabs` (the Ember Rule) for peer views in a pane; `SegmentedControl` for a small view switch |
| Navigation bar | M3: the bottom destination bar. Apple: the top bar with the title and back button | `TabBar` for the bottom destinations; "top bar" for the title bar |
| Toolbar | Apple: the window or bottom bar of actions. M3 Expressive: docked or floating toolbar, replacing the bottom app bar. Unity: a dockable strip | `Toolbar`: grouped actions on the navigation layer, never beside a bottom `TabBar` |
| Action bar | App UI `ActionBar`: a bulk-selection bar over a collection. Android legacy: the app bar | `ActionBar`: the footer row that carries a surface's buttons and the note above them |
| Sheet | Apple: a modal card (attached to the window on macOS, detents on iOS). M3: bottom or side sheet. App UI: `Tray`. trace-commons `GlassSheet`: the padded column inside a pane | `Sheet` for touch and side presentations with detents; `Modal` for desktop dialogs |
| Dialog, alert, modal | Apple: alert, confirmation dialog, sheet. M3: dialog. App UI: `Modal`, `Dialog`, `AlertDialog`. trace-commons: `GlassModal`, `GlassConfirmation` | `Modal`, with the confirmation layout for NDS-15 consent and irreversible actions |
| Snackbar, toast | M3: snackbar. Apple: none. App UI: `Toast` | `Toast`, polite, with Undo for reversible actions |
| Chip, tag, badge | M3 chips are interactive. trace-commons: `GlassChip` (status pill), `GlassTag` (verdict), `GlassBadge` (count). App UI `Chip` may be deletable | `Chip` is interactive or a filter; `Tag` is a read-only verdict; `Badge` is a count of decisions owed |
| Rail | M3: the navigation rail. trace-commons: the edge rail, a screen-edge launcher | `NavigationRail` and `EdgeRail` are separate components |
| Inspector | Apple `.inspector`: a trailing column. Unity: the Inspector window. M3: side sheet | `PropertyInspector` for edited properties; the inspector pane for read-only detail |
| Highlight, selection | Unity "highlight" is selection. Apple "selection". M3 `secondary-container` | `selection` (solid accent with `text-on-accent`) for a selected row |
| Accent | Apple: the user's system-wide accent. M3: `primary` from a seed. Unity: "accent" ramp | `accent`, set per product theme (NDS-1); overrides the system accent inside the app |
| Elevation | M3: tone levels 0-5. App UI: shadows 0-24. Unity Editor: flat, no shadows. Apple: glass and materials | Layers (navigation, content, floating, modal) with `shadow-float` and `shadow-modal` only |
| Density, scale, control size | App UI: Small, Medium, Large scale. Apple: `controlSize` mini to extraLarge. M3: opt-in density and XS-XL sizes | Density tiers `compact`, `regular`, `touch`, `dense` set on a container |
| Focus ring | Apple: the system ring. M3: 3px `secondary` indicator. App UI: 2px outline at 2px offset | `focus-ring`, 2px at 2px offset, keyboard focus only (NDS-5) |

[M3: status overview] [Unity: conflicts to resolve] [Liquid Glass: components by platform] [trace-commons: component catalog]
