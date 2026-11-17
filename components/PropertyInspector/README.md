# PropertyInspector

A labelled column of editable properties for the selected thing (an agent run, a model, a folder), grouped by foldouts, with mixed, invalid, disabled and unit-bearing values, for inspector panes on desktop and web.

## When to use

- The inspector pane of a three-pane window or a pro-tool panel: settings of the selection that people tune and compare.
- Editing several selected items at once (3 agent runs), where values can differ.
- Use `KeyValueList` for read-only facts, a `Modal` or a settings page for app-wide settings (NDS-21), and a form for a one-time task.

## Anatomy

1. **Panel**: regular inspector padding `inspector-padding-y` 18 by `inspector-padding-x` 16; dense padding 8 top and bottom, `dense-padding-left` 18 (the foldout arrows sit in it), `space-4` right. Groups `card-gap` 10 apart (dense `space-8`).
2. **Header**: the selection's name (heading step, one line) and a caption in `text-tertiary` ("Changes apply to all three.").
3. **Group**: an `Expander` (foldout). In a regular inspector each group sits on a quiet card; in a dense one it has no container and its arrow sits in the gutter. A nested group indents one level: `dense-indent` 15 in dense, the expander's chevron column plus gap in regular. At most 6 levels.
4. **Row**: a two-column grid. Label column 40% of the row, never under 96 (2 x `space-48`), `text-secondary`, one line, truncated, with the full label and its help in a tooltip. Value column takes the rest; `space-8` between them. Rows `--nr-gap` apart: 2 dense (`space-2`), 8 regular.
5. **Value well**: `field` fill, `radius-control` (dense `radius-dense` 3), height `--nr-h-control`, padding `space-10` (dense `space-6`); numbers in tabular figures; a unit after the value in `text-tertiary` ("tokens", "s", "NEAR"). Menus show the value and a 10 chevron. Booleans use `Checkbox` (`accent`). Other inputs come from `TextField`, `NumberField`, `Select`, `Slider` and `Switch` at the same density.
6. **Help line**: caption under the value, `text-tertiary`, at most 200 characters. **Message line**: caption in `critical-text` for an invalid value.

The panel lays out without horizontal scrolling down to 275 wide and is designed at `size-pane-inspector` 293.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Row height | 28 (`size-control-large`) | 28 | 44, label above value | 48, label above value | 20 (`size-control-dense`) |
| Row gap | 8 | 8 | 12 | 12 | 2 |
| Group gap | 10 | 10 | 24 (section) | 24 (section) | 8 |
| Label / value type | `mac-label` | `web-label` | `ios-body` | `android-body` | `web-caption` |
| Well radius | `radius-control` | `radius-control` | `radius-control` | `radius-control` | `radius-dense` |
| Indent per level | 22 | 22 | none (push a page) | none (push a page) | 15 |

On touch the inspector becomes a settings-style list: one value per row, nested groups open as pages or sheets, never as deep indents.

## Variants

- **Regular inspector**: groups on quiet cards (Gateway's inspector sections).
- **Dense inspector** (`.nr-dense`): Unity-style pro panel, no containers, arrows in the gutter.
- **Multi-selection**: the header names the count; values that differ show the mixed state.
- **Read-only rows** sit beside editable ones as plain text values (no well).

## States

| State | Treatment |
|---|---|
| Default | well on `field`, value `text-primary` |
| Hover | menu wells take `control-hover`; text wells keep `field` |
| Focus | 2px `focus-ring` 2px outside the well; the label stays put |
| Editing (live) | the well shows the value as it changes; previews may follow it |
| Committed | Return, leaving the field, releasing a scrub or closing a menu commits one undo step |
| Mixed | text and number wells show "—" (or the product's mixed word) as the placeholder; a checkbox shows its dash; a menu shows the mixed word. Typing a value applies it to all; Esc keeps them mixed |
| Invalid | 1px `critical` inner edge and the reason on the message line; on commit the value returns to the last valid one |
| Disabled | label and value at `opacity-disabled`, with the reason as the help line or tooltip |
| Hidden | a value that does not apply right now is not drawn; its dependants appear under their trigger when it turns on |
| Increased contrast | wells get the 1px `edge-hc` edge |

## Behavior

- **Live vs committed**: fields emit a change while people type, drag or scrub, and a commit at the end. Only the commit writes, creates an undo entry and reaches the agent or server. Esc reverts to the committed value. Slow or costly properties may commit only on Return.
- **Scrub**: dragging a numeric label left or right changes the value (Shift x10, Option or Alt x0.1); the cursor shows `ew-resize`. Arrow keys nudge.
- **Expressions and units**: number wells accept a unit or a simple expression and show the canonical form after commit.
- **Hide or disable**: disable when the value matters but cannot change now, and say why; hide when it does not apply. Never hide a button.
- **Keyboard**: Tab walks the wells in order; foldout headers are in the tab order; Return commits; Esc reverts.
- Motion: well fills on `duration-fast`; foldout chevrons on `spring-spatial-fast`. Nothing moves under Reduce Motion.

## Accessibility

- Each label is a `<label for>` (or `aria-labelledby`) of its control. Mixed values add a description ("Mixed values") and `aria-checked="mixed"` on checkboxes.
- Invalid wells set `aria-invalid` and point `aria-describedby` at the message line; help lines are descriptions too.
- Disabled controls use the native disabled state so assistive tech does not offer them, and keep their reason readable.
- Units are part of the accessible value ("4,096 tokens").
- Labels in `text-secondary` and help in `text-tertiary` hold 4.5:1 on a pane and on `card-quiet`.
- The consumer supplies every label, unit, help line, mixed word and message. The component authors none.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| The `.inspector` pane holding a `Form` with `.formStyle(.columns)` or a custom `Grid`; `DisclosureGroup` foldouts; native `TextField`, `Picker`, `Toggle(.checkbox)`; `NSNumberFormatter` units | `.inspector` on iPad regular width; a grouped `Form` on iPhone with `NavigationLink` for nested groups | A `LazyColumn` of `ListItem`s with trailing controls; nested groups as new destinations; `OutlinedTextField` with a suffix for units | `.nr-property-inspector` with `.nr-expander` groups and `.nr-property-inspector__row` grids |

## Do and don't

- Do let the indent eat the label column. Don't scroll the inspector sideways.
- Do show "—" for mixed values. Don't show the first item's value as if it were everyone's.
- Do disable with a reason. Don't hide a control that people expect to find.
- Do commit on Return and on leaving the field. Don't send every keystroke to an agent.
- Don't put high-traffic properties inside a collapsed foldout.

## Source

Intentional addition for dense desktop and web panels. Grounded in Unity Editor Foundations (inspector padding 18 / 4 / 8, 2px field gap, 8px group gap, 15px indent to 6 levels, 275 minimum width, foldouts, hide versus disable, revert on invalid) and App UI (units, live versus committed changes, undo at commit points), with mixed values specified here because neither source does. Gateway's own inspector sections (`InspectorSection` with `GlassExpander` on a quiet card, `GlassPaneInsets.inspector`) set the regular form [trace-commons §5.4]. HIG inspectors and split views set the pane.
