# Motion

Motion explains a change: where something came from, where it went, what responded to a touch. It is calm by default. Fades and fills use one curve; anything that moves uses a spring; nothing moves under Reduce Motion (decision NDS-11).

## The one curve

`ease-standard`, cubic-bezier(0.2, 0.8, 0.2, 1), is trace-commons' single curve. Use it for every change that does not move: fades, fill changes, hover, press, focus, color, opacity.

| Duration | Value | For |
|---|---|---|
| `duration-fast` | 150ms | Hover and press fills, focus ring, checkbox, chip selection |
| `duration-reveal` | 180ms | A compact pill or row expanding in place |
| `duration-standard` | 220ms | Modal fade, pane show and hide, menus appearing |
| `duration-slide` | 250ms | Footers and peeks sliding in, sub-list swaps |
| `duration-slow` | 300ms | Large-surface fades on the web and Android |
| `duration-spin` | 800ms | One spinner turn (`ease-linear`) |
| `duration-pulse` | 1600ms | One skeleton pulse (to `opacity-skeleton` and back) |

`ease-exit` (cubic-bezier(0.3, 0, 1, 1)) is for elements leaving for good on the web.

## Springs

Anything that changes position or size uses a spring, defined by stiffness and damping ratio. Native code uses the parameters; the web uses the `linear()` rendering of the same spring and its settle time.

| Token | Stiffness | Damping | Settles | For |
|---|---|---|---|---|
| `spring-spatial-fast` | 1400 | 0.9 | 224ms | Small moves: a switch knob, a segment's selection, a tab indicator |
| `spring-spatial` | 700 | 0.9 | 317ms | Panes opening, sheets, popovers and menus growing from their source |
| `spring-spatial-slow` | 300 | 0.9 | 484ms | Full-screen and window-level changes |
| `spring-effects` | 1600 | 1.0 | 231ms | Color, opacity and blur that must not overshoot |
| `spring-expressive` | 800 | 0.6 | 360ms | One or two hero moments per product |
| `spring-ember` | 322 | 0.85 | 488ms | The main-tab ember gliding between tabs (Gateway) |

The standard springs are Material 3's standard motion scheme (damping 0.9), the closest match to Apple's calm defaults. The expressive spring is Material Expressive's fast spatial spring; it overshoots by about 9%, so keep it for content-layer hero moments: a first contribution, a completed agent run, onboarding's last step. Never use it for navigation, chrome or anything a person does many times a day.

| Platform | How to write a spring |
|---|---|
| SwiftUI | `.spring(response: 2π/√k, dampingFraction: ζ)`; for `spring-spatial` that is response 0.237, damping 0.9 |
| Jetpack Compose | `spring(dampingRatio = ζ, stiffness = k)`, or the M3 `MotionScheme.standard()` and `.expressive()` |
| Web | `transition: transform var(--duration-spring-spatial) var(--spring-spatial)` |

## Choreography

- **Grow from the source.** Menus, popovers, sheets and inspectors grow from the control that opened them (`spring-spatial`) and return to it when dismissed. Liquid Glass does this natively on Apple; emulate it on the web with View Transitions or a FLIP animation.
- **Navigation uses the platform default.** Push, pop, back swipe and predictive back are the system's; never replace them with custom or bouncy transitions.
- **Panes on the desktop** open by growing the window to the right on the `duration-standard` clock and the one curve. Near the screen's edge the window slides left only as far as the new pane needs, in the same animation; closing a pane shrinks the window from the right and the left edge stays put (NDS-35). Nothing else in the window moves. While the window's edge is dragged, panes follow the frame directly; never animate their widths frame by frame.
- **Nothing fidgets.** Ambient loops (a shimmer, an aurora, a pulsing glow) run at most once on appearance or on a slow interval (trace-commons' map shimmer runs once, then every 40 seconds) and never behind text people are reading. Cards carry no shimmer: Gateway tried a card shimmer at 6, 15 and 18 second intervals and a revolving lighthouse light, and the owner removed them all (NDS-40). Every ambient effect stops while its window cannot be seen and is not drawn at all under Reduce Motion.
- **Ambient pixel field (on trial).** Gateway's Private AI guide card draws a dithered field of 5pt squares on a 6pt pitch, rising from the bottom trailing corner, rippling and drifting between three data blues at 10 frames a second, faded before it reaches the text and clipped to the card (NDS-40). It is the one sanctioned motion behind a card's words, framed by the owner as a try; don't copy it elsewhere until it is kept.
- **Press feedback** is a fill 8% darker on `duration-fast` on Apple, the web, Windows and Linux. Android may add Material's shape morph on press for buttons outside glass chrome.
- **Streaming output** appears in place without moving what is above it. Keep the reading position; never auto-scroll a person who has scrolled up.
- **Numbers** that update live change in place with tabular digits; do not count up decoratively. Two moments may count up: first run's own figures as their screen appears (traces found, tools that can connect), and a balance as new credit lands (NDS-40). A Back to an earlier step shows the figure at once; the count never replays.
- **Celebration only on a real arrival.** When credit actually lands, Gateway bursts small gold coins from the balance tile (44 coins over 1.7 s, spilling past the tile but never past the clipped edge) while the figure counts up. Never celebrate a promise, a projection or an action the person took; under Reduce Motion the coins are held still for 1.6 s and then go.

## Brand moments

The few places where a mark or a greeting moves (NDS-26). Each runs on appearance, never in a loop that competes with reading, and has a Reduce Motion end state.

| Moment | Motion | Reduce Motion |
|---|---|---|
| The N draws itself (first-run Welcome, a chat's welcome) | A marker stroke inks the N along its center line from inside the lower-left hook to the upper right, 1 s on `cubic-bezier(0.65, 0, 0.35, 1)` after 0.2 s, with a white pen-tip dot riding the stroke's front; the glow behind it fades in during the draw | The N is drawn, no tip |
| The Welcome shine | One soft band, leaning forward, crosses the N about 1.5 s after the screen opens and then every 15 s, clipped to the mark and traveling fully off it | No shine |
| Greeting | The title rises 28 and fades in over 1.6 s on `cubic-bezier(0.33, 1, 0.68, 1)`; the subtitle follows 0.3 s later. Whole lines, never letter by letter | In place, no rise |
| Welcome glow | `scene-glow-brand` fades in over 2 s behind the composer, once | Shown, no fade |
| Thinking mark | The N's glyph turns and beats on a 2 s loop while a light chases its stroke every 1.1 s, only while the model works | The still N |
| Process (first run) | Shared actors (the N, the tool tiles) move between steps instead of each step building its own; the tools burst from the N into a ring with a slight overshoot, a soft sweep passes once, found tools stay | Each step shows its end state |

- A Back to an earlier first-run step does not replay what already played.
- Long brand curves (1 to 2 s) belong only to these moments. Everything a person drives stays on the durations and springs above.

**Proof follows the evidence.** A proof animates only when its result arrives, never on a timer (NDS-43). A sealed proof stamps in (scale 0.9 to 1, 420 ms, on a spring with about 9% overshoot) and a shine crosses it once (900 ms, 250 ms after). The deployment's proof pill folds to its seal on `spring-spatial`. Checks that run in parallel resolve together.

## Reduce Motion

Under Reduce Motion (`prefers-reduced-motion`, Android's remove-animations setting), every change jumps to its end state:
- fades may remain, at `duration-fast`, but nothing slides, scales or bounces;
- springs, shape morphs and glass morphing stop;
- blur never animates;
- spinners stand still with their label, skeletons stop pulsing;
- loops hold one frame, and ambient effects (the map shimmer, the pixel field) are not drawn;
- celebrations hold their first frame briefly and go;
- desktop panes change the window frame at once.

trace-commons checks Reduce Motion in every component that animates; every parent component does the same.

## Haptics

On iPhone and Android, pair a light impact with a switch flipping, a selection snapping and a pull-to-refresh threshold; a success notification haptic with a completed send; an error haptic with a refused action. Never use haptics for streaming text, hover or anything continuous. Respect the system's haptics setting.
