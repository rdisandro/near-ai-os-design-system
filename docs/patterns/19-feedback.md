# Feedback and states

Every screen resolves to exactly one state, and every message lands on exactly one rung of a ladder. An absent signal never renders as healthy, and the right message is the quietest one the person will actually see. This section defines the state model, the gate that sits in front of it, the message ladder, notifications, progress, and the small marks (badges, haptics) that report status. It uses `StatusLabel`, `Tag`, `Badge`, `Notice`, `InlineAlert`, `Toast`, `Spinner`, `ProgressBar`, `Skeleton`, `EmptyState`, `GetStartedCard` and `Modal`.

## The state model

Every surface that shows data from a service (a local core, an account, a model) draws one of these states.

| State | Meaning | What to draw | Gateway example |
|---|---|---|---|
| Loading | Nothing has been read yet | A text line, or a `Spinner` with a line after 200 ms; a `Skeleton` only for a first-load list on web or mobile | "Reading local queue..." |
| Empty | The read succeeded and there is nothing | `EmptyState`: the product's sentence and at most one action | "Nothing is waiting." |
| Error | A read or an action failed | A section read: `Notice` in the `critical` tone with Refresh, keeping held data. An action: `InlineAlert` under its control | "That check couldn't be run just now. Nothing changed." |
| Offline | The service or network is not answering | A health `Notice` with the product's sentence; last values stay, marked as not current | "The watcher isn't running." |
| Paused | The person paused it | `StatusLabel` "Paused" with a `neutral` dot and a Resume action; paused activity drawn grey | "Paused until morning" |
| Unknown | The service answered without the signal this view needs | "—" or the product's unknown word, with no status dot | "Status unavailable" |
| Ready | Everything the view needs was reported | The content | |

### Precedence

When signals disagree, the highest state wins. The order is fixed and tested (trace-commons `ScreenState`):

1. **Offline** (core down). Whatever was last read stays on screen under the product's line, never drawn as current.
2. **Stale.** Any other failed read resolves to Unknown and ranks above Loading and Paused, because what is on screen is out of date.
3. **Loading.** Never drawn as empty or zero.
4. **Paused.** Drawn as paused, never as healthy.
5. **Unknown.** A signal the view needs is missing.
6. **Ready.** Empty is a Ready view with no items.

- A missing input never lands on Ready. If the service did not say whether watching is paused, the view is Unknown.
- Show Empty only from Ready. "Nothing is waiting." over a queue that could not be read is a false statement.
- A reload never replaces held data. While a view refreshes, keep the last render in place; do not flash a skeleton or spinner over content people were reading.
- Split held data by meaning. Content (lists, transcripts, documents) stays visible after a failed read, under a `Notice` and a "Last updated 14:02" caption in `text-tertiary`. Values whose meaning changes with time (counts, statuses, balances) switch to "—" when they go stale.

[trace-commons: ScreenState.swift, ScreenStateTests] [HIG: loading]

## The gate triad

A surface backed by a service resolves a gate before it applies the state model. The gate decides whether the screen can show its content at all.

| Gate | When | What to draw |
|---|---|---|
| Down | The service refused to start or is not running | A health `Notice` (no action unless an action can fix it): the product's title over the refusal sentence, for everyone, signed in or not |
| Awaiting | The service has not yet said whether setup is needed | A standalone, labelled `Spinner` in place of the content |
| Signed out | Setup or sign-in is required | A `Notice` in the `caution` tone with one primary button that starts sign-in or first run; or, where a section can show its frame without data, the sign-in line below |
| Open | Nothing is in the way | The state model applies |

- Resolve the gate in the order Down, Awaiting, Signed out, Open.
- Never gate a section that works before sign-in (Gateway: parts of Settings, the Private AI tab before onboarding).
- **Signed out inside a section.** When only one section needs an account, say it once, beside the section heading: "No data" in `text-secondary`, an en dash in `text-tertiary` (hidden from assistive tech), then a **Sign in** link that starts sign-in. The section's cards carry no sign-in sentences of their own. A card that must say it on its own (a balance tile seen without its heading) is head-only: "Sign in required" as its subtitle in caption style, and a small primary **Sign in** in the head's trailing slot, where Refresh sits once signed in (owner, 2026-11-02). That subtitle carries no dot, an exception to "status is a dot plus words" (NDS-16) because it names a prerequisite, not a state; the dot and Refresh return once signed in.
- Settings rows use the same three outcomes at row level: awaiting shows a standalone `Spinner`; failed or down shows an "unavailable" line, with Retry only when the read failed; answered shows the control.

[trace-commons: MonitorNavigation.swift, SettingsStateRow.swift]

## Unknown is never zero

- Draw an unknown value as "—" or the product's unknown word, and give it an accessible value in words ("unavailable"). Pick one form per product and use it everywhere.
- Never draw unknown as 0, as "On", as "Off", or as "(0 distinct)". Show 0 only when the service reported zero.
- Draw an unknown status as the word alone, with no dot. Unknown is neither on nor off.
- Draw a `Badge` whose count is unknown as "—". The menu-bar status item hides its badge at zero or unknown and draws its attention mark instead (NDS-33).
- **Hide, don't dim.** A control whose state is not yet known stays hidden until the answer arrives; it never appears disabled or off in the meantime. An action that cannot run in a row or card (Reconnect with the tool missing, actions on a session the app cannot control) is hidden, not disabled. Toolbar toggles are the exception: they keep their place and disable (NDS-41).
- Never draw a dead or unknown service as healthy in a status icon, menu-bar item, widget or chart. Data that could not be read appears as absent (a gap, or flat neutral marks with a label), never as activity or as zero.
- Write terminal unknowns as states with their own word and rules (Gateway: "Status unavailable" has no Withdraw action).

## The message ladder

Choose the lowest rung the person will see at the moment it matters, and put the message where the problem is. One event gets one message on one rung.

| Rung | Component | Scope | Lifetime | Use for | Never for |
|---|---|---|---|---|---|
| 1. Inline alert | `InlineAlert` | One control or request | Until the next attempt or the fix | A failed request, an invalid value, a refusal | Anything not tied to a control |
| 2. Notice | `Notice` | A section, pane or screen | Until resolved or acknowledged | Conditions that persist: paused, down, consent changed, offers, prompts | Confirming a finished action |
| 3. Toast with Undo | `Toast` | The window | See *Toasts* | Confirming a reversible action, with Undo | Errors, decisions, consent |
| 4. Modal confirmation | `Modal` | Blocks the window | Until answered | Irreversible and consent actions only (NDS-15) | Reversible actions, information |
| 5. System notification | OS notification | Outside the app | Until seen or cleared | Background completions; approvals needed while the app is not in front | Anything the open app already shows; marketing |

- **Move up only when a lower rung cannot be seen or the stakes demand a decision.** A notification while the app is in front is replaced by a quiet update in place.
- **Inline alert.** A caption-sized line in `critical-text`, with no frame, directly under the control or button row it refers to. A boxed alert reads as a disabled text field.
- **Notice.** On desktop a notice floats (NDS-25): an opaque plate (`pane-opaque`, `radius-card`, padding 12) over the top of its tab, under the tab bar, that pushes nothing down. A 30 pt tone coin leads (a `pane-opaque` disc with a 2 pt ring and the tone's glyph, or the tool's logo when a tool is the subject), then the title in `body-strong` with an optional `Tag`, the summary in caption, a **Details** expander for everything the decision does not need, and the actions. Its call to action is a primary `Button`; Not now, Decline and Dismiss are links. A notice that only acknowledges has an X in place of a Dismiss link. Its own failures appear as a refusal line (`InlineAlert`) inside it. A notice with no action is a health banner. In compact web and phone layouts, where a floating plate would cover the content, the same parts sit inline above the content and push it down.
- **Notice stack.** Popover notices stack with the newest in front. Up to two earlier plates peek 8 pt out behind it (three drawn at most), each scaled by 1 − 0.04 per level and drawn at 90% and 70% opacity. A new notice slides in on `spring-spatial` while the stack holds still. A stack anchored to a tab's top flows down; one anchored to a map's foot flows up. Notices that cannot be acknowledged (a held gate) have no X. A batch of the same event (several traces arriving) collapses into one notice with a count.
- **Activity log.** Operations that need a record (agent steps, changes on this machine) go to a log the person can open, never to a stream of toasts.

### Unity's tiers, mapped

| Unity Foundations | Scope | Near AI |
|---|---|---|
| Dialog | The whole app | `Modal` confirmation |
| Window banner (fades after 4 s) | The active window | `Toast` |
| Help box (under the control, at most 200 characters, one button and one link) | A section or property | `InlineAlert` or `Notice` |
| Console log | Operations | Activity log (`AgentRun` log, Settings > Changes on this machine) |

### Problem, cause, solution

- Write errors and warnings in that order, in at most three short sentences: "Couldn't save the profile because the handle is taken. Choose a different handle."
- State the data consequence: "Nothing changed.", "Nothing has been lost.", "Your queue is unchanged."
- Never prefix "Error:" or "Warning:". The tone dot and the word already say it. Map severity to tone: an error (will not complete) is `critical`, a warning (completes but may surprise) is `caution`, information is `neutral`.
- Never blame, never joke, never put codes in the title. Put codes and technical detail in an `Expander` with a `CodeBlock`.
- Concede limits plainly: "Nothing matched a pattern. That is not the same as nothing being there."
- Write state titles as full sentences with terminal punctuation ("Nothing is waiting.", "The watcher isn't running.").
- Explain every disabled control in words beside it. A tooltip alone does not count.

See *Writing and content* for voice and the banned-word lists.

[Unity Foundations: errors and messaging] [trace-commons: ShellNotices.swift, StatCard.swift] [HIG: feedback]

## Toasts

- **One at a time, on every platform.** A new toast replaces the current one. The replaced action stays undoable through Mod+Z and the Edit menu. Gateway's timed trace cards are the exception: they stack like popover notices, newest in front with earlier ones peeking, and a batch collapses into one card with a count.
- **Placement.** Compact windows: bottom center, above the tab bar or composer, `margin-compact` from the edges. Medium and wider: bottom leading of the window or of the pane that caused it, `margin-medium` from the edges. Never over navigation or the composer. Toasts sit at `z-toast`.
- **Surface.** The floating layer: `popover` over `blur-floating`, with `shadow-float`. See *Glass and materials*.
- **Content.** The product's sentence, one line where possible and two at most, plus at most one text action (Undo, View, Retry). No icon, no filled button. A close `IconButton` is optional.
- **Timing without an action.** At least 4 seconds, longer for longer text, 10 seconds at most. The timer pauses while the toast is hovered or focused.
- **Timing with Undo.** The toast stays until the person acts, dismisses it, or a newer toast replaces it, and never expires while the window is in the background. When the undo itself has a real deadline, count up from the action ("Archived 12 s ago"), never down to a deadline the app cannot see.
- **Accessibility.** Announce politely through a live region, without moving focus. Make the toast reachable with F6 (web, Windows, Linux) or the platform's region shortcut. Esc dismisses it when focused, and focus returns to where it was.
- **Motion.** Enter from the bottom edge on `spring-spatial-fast`; exit with a `duration-fast` fade. Fade only under Reduce Motion.
- **Never** use a toast for an error that needs action, for consent, or as the only record of anything important. A toast that confirms something must also leave visible evidence in place (the row moved, the label changed).
- **Persistent undo regions.** Where approvals are consequential, a product may keep a persistent undo card instead. Gateway keeps its offers, approval and undo region above the Traces tree on the Traces tab, and at the top of the inspector on the other tabs, with a live line counting up from the approval, Undo bound to Return, and a Dismiss link (owner, 2026-10-06).
- **Partial results never look like success.** When an approve is skipped or only partly applied, the toast or the region's line says what was withheld, in the core's words, and is never drawn in the success style. Undo survives selecting another item.

[M3: snackbar] [Unity App UI: toast] [trace-commons: InspectorPrompts.swift]

## Notifications

Ask for notification permission in context, after someone starts something that benefits from it (a long agent run), never at launch. Keep an in-app notification settings screen with a switch per category.

| Level | Use for | Breaks through Focus | Android channel | Windows |
|---|---|---|---|---|
| Passive | Digests, suggestions | No | Low importance | Default, silent |
| Active (default) | A run finished, a reply is ready | No | Default importance | Default |
| Time Sensitive | An approval that expires within the hour | Yes | High importance | High priority |
| Critical | Never used | | | |

- Use Time Sensitive only for something happening now or within an hour. Never send marketing as Time Sensitive, and send marketing only after a separate opt-in.
- Never repeat a notification for the same event, even if it was ignored.
- When the app is in front and showing the result, update it quietly in place.
- Errors the person can see in the app stay in the app. A failure that ends a background run the person started becomes an Active notification with the outcome word and Review.
- Never put prompts, outputs or personal content in a notification. Set a hidden-preview line ("Run finished").
- Write the title short, with no ending punctuation, and the body as full sentences, never hand-truncated.
- Offer at most four actions (three on Android), named by their result, non-destructive first, with no "Open app". Gateway allows exactly Review and Not now, and no notification action may upload, send, approve, delete or buy.
- Group notifications by run or conversation, and update one notification per run instead of posting new ones.
- Badge the app icon with decisions owed only (see *Badges*).

[HIG: managing notifications] [HIG: notifications] [trace-commons: shell shared design, notification actions]

## Progress

| Expected wait | Show |
|---|---|
| Under 200 ms | Nothing |
| 200 ms to 5 s | A `Spinner` or a specific text line (Android may use the M3 loading indicator) |
| Over 5 s, duration known | A determinate `ProgressBar` with specific words |
| Over 5 s, duration unknown | An indeterminate `ProgressBar` with specific words, switched to determinate as soon as the duration is known |

- **Prefer determinate.** It lets people decide whether to wait, switch tasks or stop.
- **Never switch shapes.** A spinner never becomes a bar and a bar never becomes a spinner. If progress may become known, start with an indeterminate bar.
- **Keep it moving and pace it honestly.** Never jump to 90% in 5 seconds and crawl through the rest. If work stalls, say why and what to do.
- **Use specific words.** "Scrubbing 3 traces", "Uploading 18 KB of 42 KB". Avoid "Loading", "Authenticating", "Please wait".
- **Place it where the work is.** Put progress after the control that started it, in the same view; one bar for a sequence of tasks. A linear bar sits on the edge of the container that is loading; a spinner sits where the content will appear, or inside the button that started the work, with the label kept.
- **Let people stop.** Offer Cancel when stopping is harmless, Pause and Cancel when cancelling loses progress, and confirm before discarding progress.
- **Hand long work to the background.** Let people navigate away, and report completion through the notification rules.
- **Spinner.** One turn per `duration-spin` (800 ms) on `ease-linear`; inline at text size, standalone at `size-glyph` or larger. It stops turning under Reduce Motion and its words carry the state. An unlabelled spinner is hidden from assistive technology; a standalone spinner has a label.
- **Text lines are indicators too.** Gateway loads its lists with a line ("Reading local queue...") and no spinner, which is the preferred form in compact desktop panes.

[HIG: progress indicators] [M3: progress indicators, loading indicator] [Unity Foundations: progress bar]

## Skeletons

- Use a `Skeleton` only for the first load of content whose layout is known (list rows, cards, history) on web and mobile. A row skeleton has a title bar at 90% width and a sub-line at 65%.
- Pulse from full opacity to `opacity-skeleton` (0.5) and back over `duration-pulse` (1600 ms). Hold it static under Reduce Motion.
- Hide skeletons from assistive technology; the region carries the loading word.
- Replace skeletons progressively as content arrives, with no layout jump.
- Never show a skeleton on a refetch, for a single value (use "—" until it is known), or in a shape that could be mistaken for zero or empty data.
- Compact desktop panes use text lines instead. Gateway ships a skeleton component and never uses it.

## Empty states

`EmptyState` is centered in its region with text held to `size-readable-width`. Use one of three kinds:

| Kind | When | Content |
|---|---|---|
| Blank | Nothing here yet, or nothing matches | One sentence and at most one action ("Add folder", "Clear filters") |
| Idle | Nothing is selected | "Select a trace to see its details." No action |
| First use | The feature has never been used | A `GetStartedCard` in place of the content it explains, or a short welcome and one primary action |

- Write the product's sentence as a full sentence with a period. An optional glyph sits above it (Gateway: the tray glyph at 22 pt).
- Keep "no results for these filters" distinct from "nothing exists", with a Clear filters link.
- Never use warning or error glyphs in an empty state, and never merge an empty state with an error.
- Never put information people need later in an empty state; it disappears.

### Getting started and sample data

- **One card for every "how this starts" surface** (NDS-39). Insights before any traces, the Private AI tab before a tool is connected and Home's Traces section before a folder is watched all use `GetStartedCard`: a title, an optional lead line, numbered steps of a title over one line with any explanation behind "i", and at most one action, a text link that names its destination ("Open Traces"). No graphic, no gradient.
- **It takes the place of what it explains.** The card shows while that content is empty, and the content returns in its place. A close X, where offered, removes it for good on this device; the content's own empty state takes over.
- **Sample data is labelled and inert.** When a surface shows sample content to explain itself, a banner sits above it: a `caution-tint` fill with no border, `radius-control`, padding 12 by 8, a glyph that means sample (`testtube.2`), the title "Sample data shown below" in label semibold and the line "Your own data will replace it once trace activity is provided." in caption (the owner's words). The sample under it is drawn at 0.55 opacity, takes no input and is hidden from assistive technology, so it never reads as the person's own.

[Unity Foundations: empty states] [HIG: writing, empty states] [trace-commons: GetStartedCard.swift, InsightsGetStarted.swift (#1888)]

## Badges

- A `Badge` counts **decisions owed** only: items waiting for the person's decision. Never queue depth, totals, credit or unread promotions.
- A count of 0 draws no badge. An unknown count draws "—" and is read as "unavailable"; the menu-bar status item hides it instead (NDS-33). Cap at 99+.
- Draw the count in `text-on-status` on `badge-fill`, or use the subtle variant inside a tab or segment.
- Badge the app icon (Dock, Home Screen, taskbar) with the same count. Android shows a launcher dot.
- A dot on a tab or segment is color only, so its accessible value carries the words.
- Never show a badge to attract attention without a decision behind it.

[trace-commons: Indicators.swift, MenuBarStatusTests] [HIG: notifications, badging]

## Undo over confirmation

Act at once and offer Undo. Confirm only what cannot be undone or what grants consent (NDS-15).

| Action | Treatment | Example |
|---|---|---|
| Reversible | Act now; `Toast` with Undo; Mod+Z | Archive a thread, keep a trace on this Mac |
| Destructive but recoverable | Act now with Undo; no confirmation | Move a draft to Recently deleted |
| Irreversible | `Modal` confirmation; the destructive action trailing and never the default | Delete an account, withdraw a contribution |
| Irreversible send or consent | `Modal`; the send drawn prominent with no Return key; consent may be gated by a `Checkbox` | Go public, send for witness review |
| One-click send from a row | The row's Submit pill sends at once, dimming the row with a `Spinner` while it sends; the review stays one click or Return away on the same row (NDS-31) | Submit a trace from the Traces tree or the edge rail |
| In place, or where sheets are unreliable | An inline confirmation in a `well` beside the control | Withdraw in a history row, a mode change in the menu-bar panel |

- Warn only before loss that is unexpected and irreversible. No warning when loss is the expected outcome.
- Title a confirmation with the action and its object, explain the consequence in the body, and repeat the verb on the button ("Withdraw"). Cancel leads and the action trails (NDS-19). Never Yes, No or OK.
- Name every undo by its action ("Undo Archive"), support multiple levels, and after undoing scroll to and highlight what came back.
- Keep Return on the safe action. In Gateway, Return is bound to Undo and never to Submit.

[HIG: undo and redo] [HIG: alerts] [trace-commons: Modal.swift]

## Celebrations

A celebration marks a real arrival, never a timer (NDS-40).

- **Only on the event itself.** Gateway bursts small gold coins out of the Near AI balance tile when credit lands, and the figure counts up during the burst: 44 coins over 1.7 s, spilling up to 120 pt beyond the tile but never past a clipped edge, drawn above the cards that follow it only while it runs. A refresh during the burst never cuts it short.
- **One per event, and only where the person can see it.** No celebration plays while the window is hidden, and none repeats for the same arrival.
- **Reduce Motion** holds a still frame of the burst for about 1.6 s, then clears it.
- **Never decorative.** No shimmer, sweep or glow loops on cards (Gateway removed its card shimmer, owner 2026-11-02). Ambient effects follow *Motion*.

[trace-commons: CoinBurst.swift, BalanceArrivalFlourish.swift (#1755)]

## Haptics

Haptics reinforce what the screen already shows. Use semantic haptic tokens so each platform plays its own pattern.

| Token | Meaning | iOS | Android |
|---|---|---|---|
| `success` | Something the person started finished | Notification feedback: success | `CONFIRM` |
| `warning` | It finished with something to check | Notification feedback: warning | None |
| `error` | It failed | Notification feedback: error | `REJECT` |
| `selection` | A value moves through discrete steps (picker, slider detents) | Selection feedback | `CLOCK_TICK` |

- Play one haptic per event, always with a visual change. Never per token, per keystroke or on routine taps.
- Follow the system setting and offer an in-app switch. The app works fully without haptics.
- On macOS, use the trackpad's alignment pattern only when a dragged item snaps into place. The web and Windows have no haptics.

[HIG: playing haptics]

## Platform mapping

| Pattern | macOS | iOS, iPadOS | Android | Web, Windows, Linux |
|---|---|---|---|---|
| Inline alert, notice | Same components on every platform | Same | Same | Same |
| Toast | Bottom leading of the window, floating glass | Bottom, above the tab bar | Snackbar position and behavior, parent tokens | Bottom leading of the window |
| Confirmation | `Modal` (780 wide) | Alert or confirmation `Sheet` | Dialog | `Modal` |
| Undo | Edit menu, Cmd-Z, `Toast` | `Toast` (never redefine shake or three-finger swipe) | `Toast` | `Toast`, Ctrl+Z |
| Indeterminate wait | `Spinner` | `Spinner` | M3 loading indicator | `Spinner` |
| Pull to refresh | None | Refresh control, plus automatic refresh | Contained loading indicator | None |
| Notifications | User notifications, menu bar | Interruption levels, Live Activities | Channels, ongoing notifications | App notifications; Web Push only if granted |
