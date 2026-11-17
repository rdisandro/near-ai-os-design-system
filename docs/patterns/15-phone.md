# Phone patterns

Phones are the compact class: under 600 wide in portrait, and compact height in landscape. One pane shows at a time, navigation sits at the bottom within thumb reach, and every target meets the touch floor. iPhone uses the system's Liquid Glass bars and sheets; Android uses Material 3 navigation, app bars, sheets and the FAB (NDS-3). Mobile web follows the Android patterns with our web components (see Web patterns).

The screen is an opaque pane: `pane-base`, or `pane-opaque` under Reduce Transparency. Only chrome floats in glass, and only over content that scrolls beneath it (NDS-9). Type uses the `ios-*` and `android-*` steps, which follow Dynamic Type and Android font scale.

## Anatomy of a phone screen

| Region | iOS | Android | Rule |
|---|---|---|---|
| Top safe area | Status bar, Dynamic Island | Status bar, display cutout | Nothing interactive inside it; bar backgrounds extend under it |
| Top bar | Navigation toolbar: large title on root screens, inline when pushed | Top app bar: small or medium flexible | Title, Back, at most three action groups |
| Content | Opaque screen, scrolls under both bars | Opaque screen | Margins `margin-compact` 16; text up to `size-readable-width` |
| Floating action | Prominent toolbar button | FAB, bottom trailing | One per screen |
| Bottom bar | Floating glass `TabBar` | Navigation bar, 64 dp | 3 to 5 destinations |
| Bottom safe area | Home indicator | Gesture handle or buttons | Bars pad above it; content scrolls under it |
| Keyboard | Keyboard layout guide | `imePadding` | The focused field and its action stay visible |

Draw edge to edge on both platforms and apply the system insets: `safeAreaInset` and the keyboard layout guide on iOS; `WindowInsets.safeDrawing` and `imePadding` on Android (edge to edge is mandatory from Android 15); `viewport-fit=cover` and `env(safe-area-inset-*)` on the web. In landscape, the side insets hold controls clear of the Dynamic Island and the rounded corners.

## Bottom navigation

**iOS.** Use the system tab bar. It floats in Liquid Glass at the bottom, with icon above label in portrait and icon beside label in landscape.

- Use three to five tabs, each one word with a filled SF Symbol. Never disable or hide a tab; an empty destination shows an `EmptyState`.
- Put search in a trailing search tab when search spans the whole app.
- A bottom accessory above the tab bar is for something app-wide and persistent. A running agent fits: "Research run · Step 3 of 7" with Stop, the same on every tab. A screen-specific action never goes there.
- The bar minimizes on scroll only when it has an accessory; tapping a tab or scrolling to the top restores it.

**Android.** Use the M3 navigation bar: 64 dp, three to five destinations, a 56 by 32 dp pill indicator behind the selected icon, labels always shown in `android-caption`. On API 31 and up it takes `blur-bar` under `glass-veil` once content passes beneath it; below API 31 it is `pane-base`.

- Selecting the current destination again scrolls it to the top.
- The bar may hide on scroll down and return on scroll up, but never while TalkBack is on.
- Never show the navigation bar and a navigation rail together.

**Both.** Tabs are places; actions never go in the tab bar. Badges count only what needs the person: Gateway's Traces tab counts decisions owed, capped at 99+, and shows a dash when the count is unknown. In a chat thread the `PromptComposer` takes the bottom edge, and the tab bar hides while the thread is pushed. Keep the composer, Send and Stop in the same place on every screen that has them.

**Back.** iOS pushes screens with a Back button at the leading edge of the toolbar, a symbol with no "Back" text, plus the edge swipe. Android uses the system Back with predictive back: the gesture previews the screen it returns to. Every pushed screen is reachable by the platform's Back.

[HIG: tab bars] [M3: navigation bar]

## Top bars and titles

| | iOS | Android and mobile web |
|---|---|---|
| Root screen | Large title, drawn by the system, collapsing to inline as content scrolls | Medium flexible bar (112 dp, title in `android-display`, up to 2 lines), compressing to small on scroll |
| Pushed screen | Inline title, Back at the leading edge | Small bar (64 dp, title in `android-title`), Back arrow at the leading edge |
| Actions | Trailing, at most three groups, one prominent | One or two trailing actions; more go in a toolbar or menu |
| Separation from content | System scroll edge effect | `blur-bar` under `glass-veil` once content passes under the bar; never a shadow |

- Keep titles under 15 characters and never use the product name as a screen title.
- The parent scale has no step for M3's large flexible bar (36 sp); use the medium bar.
- Give icon-only actions an accessible name and a `Tooltip` text that names the action ("Start new chat").
- Never mix a text button and an icon in one group of a glass bar; text buttons get their own group.

## Search

- **iOS.** Put search in the bottom toolbar or in a search tab. When focused, the field slides up above the keyboard. Use top placement only when a sheet occupies the bottom.
- **Android.** Put a search bar (56 dp pill) at the top, or a search action in the top bar. Focused search opens full screen and Back closes it.
- Show the scope in the placeholder ("Search traces", "Search chats and runs"). One search covers the whole app; a list's own filter only narrows that list.
- Show recent searches before typing, with a way to clear them. Never show them on shared surfaces such as widgets.
- If one field can both search and ask Near AI, make the mode explicit: the results list ends with an "Ask Near AI" row, and nothing is sent until the person picks it.

## Sheets, full-screen tasks and alerts

**Sheets.** Use a `Sheet` for a scoped task tied to the current screen. One sheet at a time.

| | iOS | Android |
|---|---|---|
| Detents | Medium (about half) and large; medium only when the task is short | Opens at up to half the screen, can be pulled to full |
| Handle | Grabber when resizable; a tap cycles detents and VoiceOver can operate it | 32 by 4 dp handle in a 48 dp band; a tap cycles heights |
| Shape | Half sheets inset from the screen edge, opaque at full height | `radius-sheet` 28 top corners |
| Buttons | Cancel leading, Done trailing in the top toolbar; Back replaces Cancel after the first step | Close leading; the confirming action trailing |
| Dismiss | Swipe down, Cancel or Done | Scrim tap, drag down, predictive back |

- Never show Done alone, and never Cancel, Done and Back together.
- If dismissing would lose typed text, keep it as a draft, or ask with an action sheet ("Keep draft" / "Discard").
- Use a nonmodal sheet for settings people adjust while watching the result, such as generation settings over a streaming answer.

**Full-screen tasks.** Use a full-screen task for multistep or long work: first run, writing a long brief for an agent, the "Look inside" review. On iOS present it full screen with Cancel or Close at the leading edge; on Android use the full-screen dialog (56 dp header, Close leading, the confirming action trailing). Full-screen dialogs are for the compact class only; at medium and up they become a `Modal`.

**Alerts.** Confirmations follow the ladder (NDS-15): reversible actions act at once and offer Undo; irreversible and consent actions confirm. Use the system alert on iOS and the M3 basic dialog on Android, with Cancel leading and the action trailing (NDS-19), destructive drawn as destructive and never the default. On iOS 26, action sheets anchor to the button that opened them.

**Gateway worked example: "Look inside".** The read-only review becomes a full-screen task with Close only. Under the title sit the sizes card ("would send 48 KB · on disk 212 KB", in `ios-mono`) and a `SegmentedControl`: Transcript / Search original / Turn index / Search. The Search segment focuses its field when chosen. Submit stays on the trace's screen and Dismiss in its menu, never inside the review (NDS-31).

[HIG: sheets] [M3: bottom sheets]

## Lists, swipe actions and pull to refresh

**Rows.** Build lists from `ListRow`: at least 44 pt on iOS (`size-control-touch`) and 56 dp for one line on Android (72 dp for two). The whole row is the target. On a phone, tapping a row opens it; persistent selection belongs to wider layouts.

**Swipe actions.** Offer swipe actions for the most common row actions, always with a menu alternative.

- iOS uses `swipeActions` on the leading and trailing edges. Android Compose uses swipe-to-dismiss for one action, or no swipe at all; a long press and the row's overflow `Menu` carry everything.
- Put the same actions, in the same order, in the context menu (long press) and the row's overflow menu. The top of the context menu matches the swipe actions.
- At most three actions per edge, each with a label and a symbol.
- A full swipe may run a reversible action at once, followed by an undo `Toast`. A destructive action only reveals its button, and then confirms if the product's ladder says so.
- Gateway's trace rows: swipe leading for Look inside; swipe trailing for Dismiss (confirms in a `Modal`, Cancel leading and Dismiss the destructive action). Submit stays a visible button on the row, never a swipe, because it sends.

**Pull to refresh.** Use it on lists that read from a server or a daemon: History, Submissions, agent runs, the model list. Never on a list that already updates live.

- Keep the held rows visible while refreshing. A failed refresh keeps them and adds an `InlineAlert` or a section `Notice` with Retry.
- Also offer Refresh in the screen's menu, for people who cannot perform the pull.
- iOS uses `refreshable`; Android uses the M3 pull-to-refresh indicator.

[HIG: designing for iOS] [M3: lists]

## The primary action: FAB or prominent toolbar button

| Platform | Primary action | Placement | Rules |
|---|---|---|---|
| Android and mobile web | FAB, medium (80 dp) on phones; extended FAB when a label helps | Bottom trailing, 16 dp from the edges, above the navigation bar | One per screen, constructive only ("New chat", "New run"). Never disabled: hide it when it cannot act. The extended FAB collapses to its icon on scroll down and returns on scroll up. Never alongside a floating toolbar |
| iOS | A prominent (tinted glass) toolbar button | Top trailing, or in the bottom toolbar on screens without a tab bar | One prominent item per bar. Compose-style actions use a symbol with an accessible name |

- Build the FAB from `IconButton` (or `Button` for the extended form) on the `accent` fill with `text-on-accent`.
- Keep `Toast`s above the FAB and the tab bar, never over the composer.

## Touch targets

| Platform | Target floor | Visible control | Token |
|---|---|---|---|
| iOS | 44 by 44 pt | Buttons, fields and rows 44 tall | `target-touch-apple`, `size-control-touch` |
| Android | 48 by 48 dp | 40 dp visible inside a 48 dp target | `target-touch-android` |
| Mobile web (`pointer: coarse`) | 48 by 48 px | As Android | `target-touch-android` via `.nr-touch` |

- Never shrink a target below the floor to fit a dense screen (NDS-10). Reduce the number of controls instead.
- Give small glyph controls (an info button, a clear button in a field, a 22 pt tool tile) an invisible hit area up to the floor.
- Leave about 12 pt between targets with a visible shape; in bars, let neighboring hit areas touch so a near miss still lands.
- Checkboxes and radios are 22 on touch, inside a full-row target.
- Put the actions people use most in the bottom half of the screen.

## Keyboards

- Pin the `PromptComposer` above the keyboard. Its accessory row may hold task-relevant `Chip`s (suggested replies, attach), on glass that matches the bars.
- In the `PromptComposer`, Return inserts a line and the Send button sends. Single-line fields name their return key for the task: Search in a `SearchField`, Next between fields, Done on the last one, Go on an invite code.
- Set the semantic content type of every field (email, URL, one-time code, username with passkey) so the right keyboard and autofill appear. Mobile web sets `inputmode`, `autocomplete` and `enterkeyhint`.
- Focus a field on arrival only when typing is the screen's purpose: a search screen, or a new chat. Never pop the keyboard over a screen people came to read.
- Let the keyboard dismiss interactively as people scroll the transcript.

**Text size.** Support Dynamic Type up to AX5 and Android font scale up to 200%. At accessibility sizes, stack a row's inline parts (time, status, trailing button) under its title, and never truncate a message. Scale content first; tab labels and bar icons may stay put.

## Haptics

Use the semantic haptic tokens from Feedback and states, so each platform plays its own pattern.

| Token | Phone moment | iOS | Android |
|---|---|---|---|
| `success` | A run the person is watching finishes | Notification feedback: success | `CONFIRM` |
| `warning` | It finished with something to check | Notification feedback: warning | None |
| `error` | A run fails, or an action is refused | Notification feedback: error | `REJECT` |
| `selection` | A picker or slider moves through detents | Selection feedback | `CLOCK_TICK` |

System controls (switches, pull to refresh, iOS swipe actions, sheet detents) play their own feedback; never add a second haptic on top. Mobile web has none.

- Never play a haptic per streamed token or per step of a run.
- Pair every haptic with a visible change; the product works fully without haptics.
- Respect the system setting, and offer an in-app switch in Settings > General.

[HIG: playing haptics]

## Long agent runs: Live Activities and notifications

An agent run can outlast a person's attention. The phone carries it outside the app without spamming them.

| Moment | In the app | Outside the app (iOS) | Outside the app (Android) |
|---|---|---|---|
| Running | `AgentRun` with its steps and `ToolCall`s | Live Activity: Lock Screen, Dynamic Island | Ongoing notification in an "Agent runs" channel, with determinate progress when steps are known (the Android 16 progress style where available) |
| Needs an answer | An approval card in the run | Live Activity changes to "Needs you" and a tap opens the approval; Time Sensitive notification only if the request expires within the hour, otherwise Active | High-importance notification only if it expires within the hour, otherwise Default |
| Finished | Result streamed in | Live Activity ends with a summary; Active notification | Ongoing notification replaced by a result notification |
| Failed | `InlineAlert` in the run with the reason and Retry | Active notification naming what stopped and what to do next | Default notification |

**Live Activities.**

- Use them for runs that last minutes to hours, never past 8 hours.
- Design every presentation. Compact puts the product glyph and the step ("3/7") on the leading side and elapsed time on the trailing side, snug to the camera. Minimal shows live progress, such as the step count. Expanded and the Lock Screen view show a generic run name, the current step in words ("Reading 14 sources"), and one control.
- The one control is Stop, which works from the Lock Screen. Approvals happen in the app, after unlocking, where the person can see what they approve.
- Show a status dot with words, never color alone. Elapsed time counts up from the real start ("12 min").
- Update only when something changes, animate for 2 seconds at most, and never animate on the dimmed Always-On display.
- End the activity the moment the run ends, leaving a summary on the Lock Screen for 15 to 30 minutes ("Finished · 7 steps · 18 min").
- Use one activity for several runs ("2 runs active") rather than one each.
- Offer a switch to turn Live Activities off in Settings > Notifications.

**Notifications.**

| Level (iOS) | Android importance | Use |
|---|---|---|
| Passive | Low | Digests, suggestions |
| Active | Default | A run finished or failed |
| Time Sensitive | High | An approval that expires within the hour |
| Critical | Never used | |

- Never put prompt or output text in a notification, a Live Activity or a widget; these surfaces are visible to others. The hidden-preview line is generic ("Response ready").
- Give a notification up to four actions on iOS and three on Android, non-destructive first. Never put Approve, Send or Run first, and never add an "Open app" action.
- Send one notification per event, never a repeat for the same thing.
- When the app is in front, update the screen quietly instead of notifying.
- Errors from a run the person is watching appear in the run itself and never also as a notification.
- Ask for notification permission at the moment a person starts a long run, from a `Switch` in the run's header ("Notify me when this finishes"), never at launch.

[HIG: Live Activities] [HIG: notifications]

## Widgets and controls

**Widgets.** A widget is a glance card: one idea, deep-linked to the exact screen.

- Good fits: agent status (Running, Idle, Needs you), recent threads, a New chat button. For Gateway: Waiting and Contributed counts, each a number with its word, plus the Watching / Paused status as a dot with words.
- Widgets are periodic, never live. Show when the data was read ("Updated 14:02"), and use a Live Activity for real-time progress.
- An unknown count shows a dash, never zero. Stale data is labeled, never hidden behind a placeholder; the gallery placeholder is a `Skeleton`.
- On the Lock Screen, redact thread titles and show counts only. Anything on the Lock Screen is visible to others.
- Support the light, dark, clear, tinted and accented appearances: mark the accent group, and keep meaning in words and shapes, since color may be removed. A logo, if any, is small and top trailing.
- Write the gallery description as a verb phrase for all sizes ("See what's waiting for your review.").
- Android uses resizable Glance widgets with the same content rules.

**Controls.** A Control Center or Lock Screen control (iOS) and a Quick Settings tile (Android) run one action without opening the app. Gateway's watcher fits: a toggle between Watching and Paused, with on and off symbols, an in-progress state while the change applies, and the value read back from the daemon, never assumed. Consequential actions require unlocking.

## Onboarding and permissions

Defer commitment. Nothing stands between a new person and the product's value: no sign-in, setup, permission prompt, tutorial or upsell before it is needed.

- A Near AI chat app opens on the `PromptComposer` with a few starter prompts, never on a carousel.
- Ask for an account at the first action that needs one, passkey first, with the Near AI account as the account (see Web patterns).
- Teach in context: a tip near the feature, one or two sentences, at most one tip a day, gone once the feature has been used.
- Ask for a permission when the feature that needs it is first used, after one line that names the consequence ("Microphone access lets you dictate prompts."). Ask during onboarding only for a permission the product cannot work without.
- When a permission is declined, the feature shows an `EmptyState` with a "Review settings" button that opens the system settings. Never ask again on your own.
- The launch screen matches the first screen with no logo or text on iOS; Android shows the system splash with the app icon on the first screen's color. Restore the last thread, scroll position and draft on relaunch.

**Gateway worked example: the first run.** The desktop stage (NDS-32) becomes the full screen. The step thread sits at the top (hidden on Welcome), then the step's graphic, then the title under it in two weights with one bold phrase and no period, then the content-width card, then the `ActionBar` pinned above the home indicator: Back leading, the primary action trailing ("Get started", "Continue", and "Start sharing" at Join). Sign-in is the last step and has no Skip; nothing before it is held back for an account, and an Automatic picked earlier reads "Turns on once you sign in." Nothing starts ticked, and Continue waits for one tool. The step's failure shows as an `InlineAlert` after the card. On Uses the required scope is ticked and locked, with "required" inline after its title in `positive-text` (NDS-42); Start sharing is prominent but never answers Return.

[HIG: onboarding] [HIG: managing accounts]

## Offline and poor connections

- Keep showing what was loaded, with its time, and add a status `Notice`: "You're offline. Showing values from 14:02."
- An unknown value is a dash, never zero, never "on".
- Keep drafts in the `PromptComposer`. Send waits for the connection and says why it is unavailable; a queued prompt is never sent later without the person sending it again.
- Reversible decisions may queue and apply on reconnect (Keep). Irreversible ones are unavailable offline, with the reason beside them ("Submitting needs a connection.").
- Retry reads automatically with backoff, offer a Retry button, and reopen a closed event stream after 5 seconds.
- Pull to refresh while offline shows the offline notice and keeps the rows.

See Feedback and states for the full state vocabulary, and AI and agent patterns for runs, approvals and streaming.
