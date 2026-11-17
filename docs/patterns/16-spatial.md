# Spatial patterns

Near AI products are tools for reading, deciding and directing agents, so in space they are windows. On Apple Vision Pro they run in the Shared Space beside other apps; on Android XR they run as spatial panels in home space. Immersion, volumes and 3D are exceptions a product must justify.

A visionOS point measures an angle. Dynamic scale keeps a window the same apparent size at any distance, so the parent's pt values carry over. The default visionOS window (1280 by 720 pt) is in the large class, and the default Android XR panel (1024 by 720 dp) is in the expanded class (NDS-12).

## Spatial surfaces

| Surface | visionOS | Android XR | Near AI use |
|---|---|---|---|
| Window or panel | Upright glass plane; default 1280 by 720 pt, opening about 2 m away; close button, window bar and resize controls from the system | Spatial panel; default 1024 by 720 dp at 1.75 m, 32 dp corners; up to 2560 by 1800 dp | Every product surface: chat, agent runs, Traces, Private AI, Settings |
| Ornament or orbiter | Controls on a plane just in front of the window; system tab bars and toolbars are ornaments | Orbiters hold the rail, app bar and navigation bar | Navigation and the window's toolbar |
| Auxiliary window | A second window with one task and a close button | A second panel | A review ("Look inside"), a detached run, Settings |
| Volume | Bounded 3D content viewable from any angle | 3D content in a panel group | Only 3D artifacts an agent produced or a person inspects |
| Immersive space | Full Space: mixed, progressive or full | Full space | Rarely; see Immersion |
| Widget | Placed on a wall or surface; elevated or recessed; paper or glass | No equivalent | Glance: what is waiting, what is running |

## Windows are glass

visionOS windows use the system's glass, the original glass material. It is unmodifiable, adapts to the light and color of the room behind it, and has no Dark Mode setting. Keep the glass background on every window; prefer translucency to opaque fills.

- Never paint `glass-veil` or `pane-fill` over a visionOS window. The parent's painted glass (NDS-7, Glass and materials) is for macOS, iOS and iPadOS, where a desktop or wallpaper sits behind the pane. In space the system glass and its vibrant text carry legibility.
- One window is one glass surface. Group the regions inside it with the system materials, never with nested glass; custom containers use `glassBackgroundEffect` with the implicit display mode, so they draw glass only when nothing around them already does.
- Paint content-layer elements with materials and the dark theme's marks:

| Parent role | visionOS rendering |
|---|---|
| `control`, a selected `ListRow`, a `Button` on the window | Thin material |
| Section grouping: `card`, the sidebar or list column | Regular material |
| `well`, `field` drawn on top of regular | Thick material |
| `text-primary`, `text-secondary`, `text-tertiary` | Vibrant label, secondary label, tertiary label (tertiary for inactive text only) |
| `accent`, status marks (`positive`, `caution`, `critical`), `data-1` to `data-8` | The values of `dark`, or `gateway-dark` for Gateway, because window glass reads dark |
| Charts (`BarGraph`, `StatCard` sparkline) | The dark theme's opaque `surface-chart`, inset as a card. Charts never plot on glass |

- Buttons on a window use the thin material. Only buttons floating free in space use glass.
- `shadow-float` and `shadow-modal` do not apply; the system's depth, lighting and shadow separate layers.
- Corners: the system draws the window's. Content inside is concentric with it, down to `radius-tile`. Prefer capsules (`radius-pill`) and circles for controls, because corners draw the eye.
- Under Increase Contrast use the `dark-hc` mark values. Under Reduce Transparency the system makes the glass more opaque; never substitute a painted fill.

[Liquid Glass: visionOS] [HIG: windows] [HIG: materials]

## Ornaments and orbiters

Navigation and frequent controls move out of the window, onto ornaments (visionOS) or orbiters (Android XR). Content stays in the window. The destinations and commands are the same ones Navigation and commands defines for every platform.

| Parent component | visionOS | Android XR |
|---|---|---|
| `TabBar`, `NavigationRail` | Vertical tab bar ornament on the window's leading edge; labels appear when people look at it | Navigation rail orbiter on the leading edge |
| `Toolbar` (window actions) | Toolbar ornament along the bottom edge, on a plane in front of the window | App bar orbiter at the top center |
| `Sidebar` | A sidebar column inside the window; for a deep hierarchy, a sidebar inside one tab | List pane inside the panel |
| Inspector | `.inspector` column inside the window | Second pane, or a second panel |
| `Sheet`, `Modal` | Sheet centered in the field of view, pushing its window back; system alerts | Basic dialog; never a full-screen dialog |
| `Menu`, `Popover` | System menus and popovers | M3 menus |

- Keep ornaments few, frequent and visible. Hide them only during immersive viewing.
- An ornament is never wider than its window, and the window never shrinks below its toolbar's width (there is no menu bar to fall back on).
- Use borderless buttons in ornaments; they take the system hover effect.
- No pull-down menus in the toolbar ornament, because they cover the window controls. Turn a one-item menu into a toggle; move a longer one into the window as a popover.
- Supplemental content goes into an adjacent window, never into an ornament.
- On Android XR, place orbiters 20 dp from the panel, or overlap it by at most 12 dp and never more than half the orbiter's height.
- A volume gets at most one extra ornament, never on the edge that holds its toolbar or tab bar.

[HIG: ornaments] [M3: XR]

## Targets and gaze

**Targets.** The spatial target is `target-spatial` 60 pt (NDS-10; see Layout, density and targets). Android XR asks for 56 dp; use 60 on both.

- Visible buttons come in the system sizes (28, 32, 44, 52 and 64 pt). Whatever the visible size, keep item centers at least 60 pt apart, or leave at least 16 pt clear around each item. Eyes make small involuntary movements, and this spacing absorbs them.
- Never let interactive elements overlap.
- Give a multi-part component one hover region: a `ListRow` with a title, a `Tag` and a trailing button highlights as one shape, with the button as its own target only when it is 60 apart.

**Gaze is never reported.** An app is never told where a person looks before they pinch. Design as if looking were invisible, because to the app it is.

- No gaze analytics and no logic triggered by looking. A message is never marked as read because it was looked at; a `ToolCall` never expands on a look; a run never pauses when people look away.
- Hover feedback is the system's, drawn outside the app. Use the standard components, which provide it. Custom hover effects are allowed but sparse, and they too run out of process.
- Hover delays: none for subtle cues (a slider knob), short for expanding the tab bar, long for a `Tooltip`. Tooltip text names the action, verb first, never an instruction.
- Keyboard focus is separate from gaze hover. When a keyboard or game controller drives focus, the focus ring rules apply (NDS-5).

**Input.** Prefer indirect input: look, then pinch with the hand at rest. Use direct touch only for near, brief manipulation. Support a keyboard, a trackpad, a game controller and voice, and never require a particular hand or both hands. Dictation is a first-class way to fill the `PromptComposer`; the system keyboard opens as its own movable window.

**Visual calm.** Keep motion and bright, high-contrast objects out of the periphery. Never fill the field of view with a repeating pattern, which creates false depth. Gateway's flow map draws a tiled Near AI "N" texture behind its nodes; on visionOS, drop the texture and keep the plain ground.

**Look to Scroll.** Opt into Look to Scroll for reading views: a long agent answer, a transcript in "Look inside". Leave it off in dense, control-heavy panes such as the Traces tree and Settings.

[HIG: eyes] [HIG: spatial layout]

## Depth and placement

- Use depth for hierarchy only. A sheet pushes its window back; an ornament sits a little forward. Limit the number of depth levels, because refocusing tires the eyes.
- Never give text depth, and never extrude glyphs. Reserve depth for large elements such as toolbars and tab bars.
- Keep any 3D content inside a window shallow and inset; deep content is clipped.
- Anchor content in the room, never to the head. Place windows at least 1 m away for sustained reading. Apps open in front of the person; let them move windows rather than moving windows for them.
- On Android XR, place the panel's center 5 degrees below eye level and keep primary content in the central 41 degrees.
- Use dynamic scale for every interactive window. Fixed scale is for true-to-life objects only.
- Avoid too many windows. One product window, plus an auxiliary window when a task needs one, is the norm.

## Volumes

A volume is for content that is genuinely three-dimensional. Near AI surfaces are text, lists, cards and charts, which stay in windows.

- Use a volume when an agent returns a 3D artifact (a USDZ model, a scanned object) or a person inspects one.
- Keep charts and the Gateway map in windows. A 2D chart turned into 3D is harder to read and has no text alternative.
- Prefer dynamic scale unless the object is shown at real size. Pin 2D labels to points on the model as attachments, billboarded so they always face the viewer.
- The volume's close button and window bar turn to face the viewer; keep the baseplate and its glow.

## Immersion

Use the least immersion each moment needs, and let people choose when to enter and leave.

| Mode | Where | Use in Near AI products |
|---|---|---|
| Shared Space | Beside other apps | The default for every product surface; launch here |
| Dimmed passthrough | Shared or Full Space | A focus mode for a long agent session or a "Look inside" review |
| Mixed | Full Space | 3D artifacts placed in the room |
| Progressive (120 to 360 degrees, set with the Digital Crown) | Full Space | Presentations and media only |
| Full (360 degrees) | Full Space | Not used for tools |

- Entering is always an explicit action with a labeled control. Leaving has its own labeled control ("Back to window"), and the state is saved first.
- The same rule applies to autonomous agent modes: an explicit start, a labeled way out, and the run's state kept.
- Never enter an immersive space on your own, including when a run finishes.
- In progressive and full immersion, people approaching about 1.5 m from where they started see the room fade back. Avoid those styles where people may move around.
- Keep media playing when people look away. Expect audio to duck when the app is not the one playing.

[HIG: immersive experiences]

## Typography

visionOS uses SF Pro through the system text styles and Dynamic Type. Body is 17 pt by default and nothing goes below 12 pt. visionOS body and title styles are bolder than on iPhone, and it adds extra-large titles for editorial layouts.

- Use the `ios-*` steps on visionOS. Tags and badges, which use `micro` elsewhere, take 12 pt here; the smallest sentence text is `ios-caption` (13).
- Text on glass is the vibrant label color, white by default. Text with no background behind it is bold and never has a shadow.
- Text is always 2D. Labels attached to points in 3D space billboard toward the viewer.
- Figures that describe what leaves the device stay in `ios-mono`.
- Test every screen at the smallest and largest window sizes and at the largest text size.
- On Android XR, body text is at least 14 dp.

[HIG: typography]

## How Near AI windows translate

### The three-pane window

The Mac's floating three-pane window becomes one visionOS window with columns. The panes stay inside that one window, because one window is one glass and three windows for one task are too many.

| Mac (Gateway monitor) | visionOS | Android XR |
|---|---|---|
| Window, default 1193 by 614 | One window, default 1280 by 720, resizable; layout by class | One panel, 1024 by 720 (expanded: two panes) |
| Tabs in the main pane: Home / Private AI / Traces / Insights | Vertical tab bar ornament on the leading edge, with the decisions-owed badge on Traces | Rail orbiter on the leading edge |
| Main pane: notices, list controls, the Traces tree | List column, about `size-pane-main` 440 | List pane |
| Content pane: the map | Detail column, flexible. The floating Traces / Private AI `SegmentedControl` stays in the window on thin material | Detail pane |
| Inspector, `size-pane-inspector` 293 | `.inspector` column | Side pane, or a second panel |
| Toolbar capsule: Graph, Map, Inspector, Settings | Toolbar ornament along the bottom. "Show ignored folders" stays in the list's filter menu | App bar orbiter |
| "Look inside" review sheet | An auxiliary window beside the main one, with Close | A second panel |
| Confirmations (Dismiss a trace, arm a folder) | System alert or a sheet centered in view | Basic dialog |
| Settings window | Its own window (NDS-21) | Its own panel |
| Menu-bar panel and edge rail | No equivalent. A widget carries the glance: Waiting and Contributed counts, Watching or Paused | Not applicable |

At 1280 pt the three columns fit with room to spare (440 + 293 leaves 547 for the map). When people narrow the window, the columns collapse in the same order as on iPad: the inspector first, then the map into the navigation stack.

Inside the window, the Mac's floating panes and the gaps between them become columns of one glass, separated by the regular material and `rule` lines. Cards, notices and the trace review card sit on the regular material; their buttons sit on the thin material. Gateway's accent comes from `gateway-dark`, the parent's blue since NDS-22.

### Chat and agent runs

- A thread is a window: the transcript scrolls, and the `PromptComposer` sits at the bottom of the window with a dictation button beside Send. Send becomes Stop during generation, in the same place. Streaming, approvals and stopping follow AI and agent patterns.
- Agent runs list in a sidebar column; a run's `AgentRun` and `ToolCall`s fill the detail. "Open in New Window" detaches a run so people can keep it in view beside their work.
- Live Activities do not exist on visionOS. A run in progress shows its progress in its window; when the window is closed, a notification reports the finish, the failure or a request for an answer, with the same rules as on phones.
- A widget can show the runs in progress and what is waiting. At a distance it switches to the simplified level of detail: larger type and no buttons. Up close it shows the default layout. People can scale widgets from 75 to 125%; test both ends.
- Keep reading surfaces calm: no motion beside the transcript while people read, and no animated background behind long answers.

[M3: XR] [trace-commons: MonitorWindowView.swift]
