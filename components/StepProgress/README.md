# StepProgress

Step progress shows where the person is in a short fixed sequence, such as first-run setup, as nodes or labels joined by a line; the steps are reached in order, never chosen ahead.

## When to use

- A setup or onboarding flow of three to five steps (Tools, Uses, Traces, Private AI, Join).
- A multi-step task whose steps have names the person will recognize later.
- Not for navigation between peer views (`Tabs`), not for a long job's completion (`ProgressBar`), and not for an agent run's steps (`AgentRun`).

## Anatomy

1. **List** `.nr-steps`, an ordered list; steps share the width equally.
2. **Node** `.nr-steps__node`: a 14 circle (`space-14`). Done and current: `accent-soft` with a 2px `accent-tint` ring. Pending: `well` with the `shadow-check` rim.
3. **Connector**: a 2px line between nodes, 6 clear of each node (`space-6`), centered on them. `accent-soft` into a reached step, `rule` into a pending one.
4. **Label** `.nr-steps__label`: under the node, 6 below. Eyebrow step, uppercase; `text-primary` for the current step, `text-tertiary` for the rest.
5. **Vertical** (`--vertical`): the node leads, the label sits 10 beside it, the connector runs down between nodes, 24 between steps. The current label is semibold.
6. **Thread** (`--thread`): no nodes. The labels sit in one centered line, each joined to the next by a stretch 38 wide (`space-32` + `space-6`). A travelled stretch is a 2px glowing line in `accent-soft`; the stretch into the current step leads with a gradient to a lighter tint of it; a stretch still to come is dotted in `scene-rule`. The current label is `text-primary`, passed labels `text-secondary`, the rest `text-tertiary`.

Put the type class on the step (`li`); the vertical node centers on the first line with `1lh`.

## Sizes by density

| | compact (macOS) | regular (web) | touch iOS | touch Android | dense |
|---|---|---|---|---|---|
| Layout | horizontal; thread on the first-run stage | horizontal | vertical, or horizontal for 3 short labels | vertical, or horizontal | not used |
| Label | `mac-eyebrow` | `web-eyebrow` | `ios-label` (vertical) | `android-label` (vertical) | |
| Node | 14 | 14 | 14 | 14 | |
| Connector | 2 | 2 | 2 | 2 | |

## Variants

- **Horizontal** (default): up to five steps with one-word labels.
- **Vertical** (`--vertical`): phones and long labels ("Choose folders to watch").
- **Thread** (`--thread`): the first-run stage on the scene (NDS-32). It sits at the top of every step but Welcome and the finish, and connects the step titles as the person moves along. A passed step's label is a button back to it (`.nr-steps__back`); steps ahead are not.

## States

| State | Node | Label |
|---|---|---|
| Done (`--done`) | `accent-soft`, `accent-tint` ring | `text-tertiary` |
| Current (`aria-current="step"`) | `accent-soft`, `accent-tint` ring | `text-primary` (semibold when vertical) |
| Pending | `well`, `shadow-check` rim | `text-tertiary` |
| Failed step | the node stays current; the step's page shows an `InlineAlert` | unchanged |

No hover, pressed or focus states on nodes: they are not controls. In the thread, a passed step's label is a button: hover takes `text-primary`, focus draws the ring.

## Behavior

- The flow's own Back and Continue buttons in its `ActionBar` move between steps. Clicking a node does nothing. In the thread, clicking a passed step's label goes back to it, keeping every answer.
- Going back keeps the later steps pending; a flow that branches redraws the list for the chosen branch.
- **Motion**: node and connector fills change on `duration-fast` with `ease-standard`. In the thread the stretch fills over 0.52 s and its label lights 0.42 s after the fill starts; Back runs it in reverse. Nothing moves, and nothing changes gradually under Reduce Motion.

## Accessibility

- An `ol` with an `aria-label` from the product ("Setup progress"); the current step carries `aria-current="step"`. The thread is not a heading; the step's title under the graphic is.
- Each step speaks its label and its state in words from the product's copy (done, current step, not started), as visually hidden text. The component authors no words; with no state words, a step speaks only its label.
- Nodes are hidden from assistive tech.
- `accent-soft` holds 3:1 on `pane-opaque`. The pending node is drawn with the `shadow-check` rim, and state also lives in the label ink and the text alternative, so color is never the only cue.
- **The product supplies**: step labels, the current index, the state words, the list's label.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| Custom `GlassStepProgress`; the thread in `FirstRunStage` | Custom (no system step indicator; a `ProgressView` is a bar) | Custom (M3 has no stepper) | Custom: this CSS |

## Do and don't

- Do use the names the flow's pages use, as nouns.
- Do show the step progress at the top of every step's page, in the same place.
- Don't make nodes clickable or style them as buttons. Only the thread's passed labels go back.
- Don't show the thread on a welcome or a finish screen.
- Don't use more than five steps; split the flow or use a `ProgressBar` with "Step 3 of 7".
- Don't show it for a single step.

## Source

`GlassStepProgress` in `macos/Sources/TCDesign/Components/Navigation.swift`: "Not a tab control: the steps are not chosen, they are reached"; 14pt circles in `purpleSoft` with a 3pt ring at 25% when done or current (centered on the edge, so about 1.5pt shows, drawn here as the 2px `accent-tint` ring), `wellFill` when pending, 2pt connectors with 6pt insets, eyebrow labels, and `StateValues` (done, current, pending) from the core. The thread is the animated first run's step bar (owner, 2026-10-22: "a progressive thread that connects to each screen title sequence and highlights the step title"): `FirstRunStageLayout.segment(before:current:)` (travelled, leading, ahead) in `Views/FirstRun/FirstRunStage.swift`, segment width 38, the leading gradient to #a8dcff (drawn here as a lighter mix of `accent-soft`), a 0.52 s fill and the label 0.42 s later, hidden on Welcome; #1558. The vertical variant is an intentional addition for phones.
