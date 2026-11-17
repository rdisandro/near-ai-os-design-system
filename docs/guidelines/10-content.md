# Writing and content

Words are part of every component, and the components write none of them. Each product keeps one copy source that every shell reads (NDS-16); this section sets the voice, the rules that copy follows, and the vocabulary Near AI products share. Examples come from Gateway, where the rules were proven, and from Near AI agent scenarios.

## Voice

Near AI's voice is **direct, and centered on proof rather than promises.** It says what happened, what will happen to the person's data, and what they can check.

- **Concede imperfection first.** When a check has limits, say so before anything else. "Nothing matched a pattern. That is not the same as nothing being there." The admission is what makes the next sentence credible.
- **Never name the mechanism; state the data consequence.** People care where their data goes and whether anything was lost, and the pipeline that moved it means nothing to them.

| Avoid | Write |
|---|---|
| "The privacy filter redacted 3 secrets." | "3 secrets were replaced before this preview." |
| "Ingest failed; claim released." | "Nothing was sent. Nothing has been lost; your queue is unchanged." |
| "Routing via the ironwire proxy." | "Claude Code sends its calls here, and this computer answers them." |
| "Canary check passed." | "Verified." |

- **Promise nothing about privacy or security.** No sentence says private (as a promise), secure, encrypted, anonymous or protected. Describe what happens instead: "Nothing is sent unless you say so." "You decide what gets shared."
- **Trust relaxes what may be sent, never what may be said.** A person who turns on Automatic still reads the same honest sentences about what leaves their machine.
- **Never state a number you cannot honor.** No turnaround times, success rates or ETAs without a reliable source. Elapsed time counts up from a real instant ("approved 12s ago"); it never counts down to a deadline the app cannot see.
- **Write from the person's side.** Use "you". Avoid "we", because nobody can tell who "we" is ("Couldn't load your traces", never a "we're having trouble" phrasing). System chrome never says "I"; an assistant may speak as "I" inside a conversation, and nowhere else.
- **Tone follows the moment.** Neutral and plain for failures, refusals, money, data and irreversible actions; warmer for a finished setup or a first contribution. Never playful about data.
- **State lines are full sentences with terminal punctuation.** "Nothing is waiting." "The watcher isn't running." Labels, buttons and headings take no period.

[trace-commons: §6.3 voice and tone] [HIG: writing]

## The UI copy rules

These rules come from trace-commons' UI copy guide and apply to every Near AI product.

1. **Buttons name actions.** Use an action verb, or a verb and an object, in one or two words. Go longer only when a shorter label would mislead. Never shorten to a vague "OK".

| Long | Short |
|---|---|
| Keep on this Mac | **Keep** |
| Request server refresh | **Refresh** |
| Custom setup instead | **Customize** |
| Send this trace now | **Submit** |
| Send this trace for review | **Send** |
| Move to my Near AI account | **Move** |
| Create comparison task | **Create task** |
| Save user-reported outcome | **Save outcome** |

Explanations and confirmations have no word limit; buttons do.

2. **Name what this click does.** A button that opens settings says **Review settings**; **Turn on** is reserved for the button that actually turns something on. A notice's **Dismiss** and a trace's **Not this one** do different things, so they are different copy keys. Prefer the person's action to the machinery ("Refresh", never "Request server refresh").
3. **Move essential context beside the action.** Consequences, immutability, scope, consent and destructive effects sit in visible copy next to the button or in its confirmation: "Load more" carries "{size} remaining"; "Save" carries "A saved specification cannot be changed."; "Send" carries the destination and scope ("3 traces, 4.2 MB, to the server that receives your traces"); "Skip" says what skipping sets up. A tooltip or accessible name alone is not enough. Copy about taking the primary action sits directly above the action bar, in secondary text, full width.
4. **Titles and buttons have separate jobs.** The title names the task; the button names the act. "Create new passkey" / **Create**. "Launch managed session" / **Launch**. "Clear episode assessment" / **Clear**. Keep separate copy keys even when the visible words match.
5. **Repeated controls are distinguishable to assistive technology.** The accessible name is the visible action plus its object: "Save episode assessment", "Refresh saved specifications". Wire it into each platform's accessibility API.
6. **Navigation names things; choices name values.** Sections are noun phrases ("Data uses", "Change log"), and a heading repeats the navigation label that leads to it. Choices are values: "1 hour", "Until morning", "Until resumed".
7. **Update every reference when a label changes.** Instructions that cite a button ("Choose Refresh"), search hints, confirmations, accessible names, test fixtures and docs change with it.
8. **Keep shared copy shared.** Edit the owning copy table and update every consumer; never write shell-local prose. Keep old payloads readable while clients catch up.

9. **Name a link by where it goes.** A link that opens another place says so ("Open Traces"), never the title of the step it sits under. A text link that leaves the surface ends with a right arrow glyph, never a typed character.
10. **Say each thing once.** A notice, card or dialog states each fact once. When two lines say the same thing, keep the one beside the action.

Review every copy change against the same list: one- or two-word actions; a clear target; consequences visible; separate keys; distinguishable accessible names; headings matching navigation; every consumer updated; wording ratchets run. Report any platform the change did not exercise. Never raise a wording baseline to hide new prose, and never imply an approval that has not happened. [trace-commons: docs/ui-copy-guide.md]

## What stays visible and what goes behind "i"

Short surfaces keep one idea per line and move explanation out of the way. Nothing is removed in the move: the full text stays one click away.

- **A choice** shows its first line. The rest of its description sits behind an "i" info button after the line's last word, named "More about {title}".
- **A long disclosure** shows its first two sentences, then a **Learn more** link that expands the rest in place. The expanded text replaces the short form; it does not repeat it.
- **Never behind "i"**: status, failures, prerequisites, consequences of the action beside it, and irreversible warnings. These stay on the page (rule 3). An "i" never sits inside a button.
- **A notice** shows only what the decision needs; the rest folds behind its **Details** expander. A consequence that a shared computer turns on stays visible (NDS-25).
- **A get-started step** is a title over one short line, with any explanation behind an "i" (NDS-39).

[trace-commons: Insights rule, 2026-10-15; owner, 2026-11-02]

## Restricted words on Private AI surfaces

Private AI and the tool-connection ("harness") screens describe where an agent's calls go. These words either promise something or expose plumbing, and they never appear there:

| Restricted | Why | Write instead |
|---|---|---|
| private (as a promise), secure, encrypt, anonym-, protect | Promises a property the screen cannot prove | State the consequence: "Calls from Claude Code are answered on this computer." |
| proxy, backend, route, routing, endpoint, localhost, ironwire | Names the mechanism | "{tool} sends its calls here", "this computer answers them" |
| credit, earn | Implies a currency or a reward | "Manage billing", never "Manage credits" |
| Vendor or model-host names | Implies a relationship or exposes a supplier | The destination's name: "Private AI" |

One privacy sentence is allowed, because the copy source owns it and states a mechanism the person controls: "Add a privacy layer to AI models you are already using." It heads the Private AI tab and the website's Private AI section, and nothing else on those surfaces repeats or extends the claim. Two current drafts conflict with this table and stay unapproved until the owner rules: Gateway's Private AI guide card ("Earn credit", "Calls go through Private AI and use your credit.") and the website's "Paid with your Near AI credit."

Elsewhere in Gateway: "Share automatically" appears nowhere (the modes are Ask, Automatic and Never); no consent label begins with "Training"; the scan screen never headlines "PII filter" or "Near AI"; detector keys such as `secret:aws access key` are internal and never shown as a reason. [trace-commons: §6.4]

## Terminology

Use one word per concept, everywhere, with no synonyms. A product's glossary lives with its copy source.

### Near AI names

| Name | Use | Never |
|---|---|---|
| **Near AI** | The master brand and the account ("your Near AI account"). Capital N, lowercase "ear", capital "AI", one space (owner, 2026-11-04; NDS-48) | NEAR AI, NearAI, near.ai in prose |
| **Gateway** | The macOS app, and its Windows and Linux shells (owner, 2026-11-04; NDS-48), formerly Trace. "Near AI Gateway" in full where the brand isn't already beside it: the website, the wordmark lockup (NDS-27), an install prompt | Trace, Near.ai, "the Near AI app" |
| **Near.ai** | Only where the shipping bundle still uses it until the code is renamed (`Near.ai.app`, `open -a "Near.ai"`) | Near.ai as the product's name in prose |
| **this app**, **the server that receives your traces** | What Gateway's copy says instead of "Trace Commons", which appears nowhere a person can see (owner, 2026-11-02; NDS-28) | Trace Commons, the commons, the backend |
| **Private AI** | The destination that answers an agent's calls; a proper name, read from the copy source | private inference, the proxy |

The proof words "Gateway only" and "Gateway signed" name Near AI's inference gateway, a different thing from the app. Where both can appear on one screen, write the app as "Gateway" and the proof's part as "the Near AI inference gateway" in its explanation; the short proof word stays (open question 4). A chat product built on the system calls itself by its own app name (the internal chat deployment uses "Private AI" for the app and "Near AI" for the endpoint); it never mixes them in one sentence.

### Agent and AI vocabulary

| Term | Means | Never |
|---|---|---|
| **agent** | Software that acts for the person through tools | bot, assistant (unless it is one), AI (as a noun for the agent) |
| **run** | One attempt by an agent at one task, from start to stop | job, execution, invocation |
| **tool** | Something an agent can use: a coding tool (Claude Code, Codex), a file reader, a search | plugin, skill (unless the product defines one) |
| **tool call** | One use of a tool inside a run | function call, action (in UI) |
| **model** | The AI model that produced a response; name it when the person chose it | engine, brain |
| **trace** | One recorded piece of a person's work with a coding tool: what the app watches, shows, keeps and shares (NDS-29) | session, log, dataset, sample |
| **session** | Only the coding tool's own session id, a sign-in session, or a managed agent session the app launched (NDS-29) | Any other use in user copy |
| **verified / pending / no proof** | Proof states: a proof was checked; a proof is expected and not yet checked; no proof was recorded. Each product words them from its copy source: Gateway says Verified, Pending, Gateway only, Check failed, No proof; the chat product says Checking or Signing, Verified, Gateway signed, Check failed, Not checked (NDS-43) | secure, trusted, unverified |

### Gateway's canonical words

| Concept | Words |
|---|---|
| Folder modes | **Ask / Automatic / Never** ("Never" is an absolute exclusion; "Automatic" is a grant; owner, 2026-10-12) |
| Sharing default | **Automatic / Ask each time**, at the end of first run and at the top of Settings > Projects. A default for folders with no rule of their own; a folder's own rule always wins (NDS-30) |
| Watch state | **Watching / Paused** |
| Pause durations | **1 hour / Until morning / Until resumed** |
| Gateway actions | **Submit** (sends at once; tooltip "Sends this trace now."), **Look inside**, **Not this one** (skips this trace only; the project keeps being offered); **Dismiss** lives in the row's menu. "Contribute" and "Review" are retired on macOS buttons (NDS-31) |
| Folder actions | **Submit {count}**, **Submit as…** (NDS-31) |
| Verdicts | **Worked / Partly / Failed** |
| First run | **Get started**, **Continue**, **Back**, **Customize** (Tools only), **Start sharing** at Join. No Quick or Custom setup and no Skip. An Automatic picked before sign-in reads "Turns on once you sign in." (NDS-32) |
| Re-reading | **Refresh** for every re-read, including the ones that said Retry (NDS-36) |
| Sign-in | **Sign in** (accessible name "Sign in to Near AI"), **Sign in required** on a card, "No data – Sign in" beside a section heading |
| Sample data | "Sample data shown below" / "Your own data will replace it once trace activity is provided." (the owner's words; NDS-39) |
| Home counts | **Waiting** (decisions owed), **Contributed** (all time); "Credit pending" only beside its condition |
| Unknown | The core's **Unknown**; an unknown History status reads **Status unavailable** |
| Badge | Counts decisions owed only, never queue depth or credit; caps at **99+** |

## Numbers, dates and credit

- **Unknown is never zero.** Show "—" or the product's unknown word, never a confident 0, never "on", never "(0 distinct)". Use the dash in a cell, tile or figure slot; inside a sentence write the word ("Balance: Unknown"). A badge with no answer draws a dash and reads "unavailable"; the menu-bar status item hides its badge instead (NDS-33).
- **Credit is a record.** Show no currency symbol and no fiat estimate. Projected credit carries its condition ("+20 projected, if it is accepted") and never looks like settled credit. An estimate before an invite is a range with its condition: "An estimated 3–8 points per accepted trace, not yet settled."
- **Money estimates are open.** Gateway now shows the first-run estimate as one total, in dollars when the server sets a range (#1584), and its Not contributed card can show "You could make about {low} to {high} of inference" behind a setting. Both are fiat figures; whether they fit this rule is an open question for the owner.
- **Figures that describe what leaves the device are monospaced** (`*-mono`, tabular digits): sizes, counts sent, hashes, paths. Prose never is.
- **Dates and durations** follow the product's format from the copy source. Gateway uses "Sat 12 Sep", "52 min", "1 h 18 min", and reads trace dates in UTC so a trace never shifts a day; Insights uses ISO weeks ("analysis dates, not work dates").
- **Counts inflect in the copy source**: "1 trace", "2 traces". A shell never branches on `n == 1`.
- Use numerals for every count and measure ("3 files", "2 min"). Use locale formatting for thousands separators and decimals; never build a number string by hand.

## Capitalization and punctuation

- **Sentence case everywhere**: headings, titles, buttons, labels, menu items, tabs, tooltips. Capitalize only the first word and proper nouns (Near AI, Private AI, Claude Code).
- **Apple title-case exceptions.** On macOS and iPadOS, menu-bar menus and their items sit beside the system's title-case items ("File", "Close Window"), so they render in title case: capitalize every word except articles, coordinating conjunctions and short prepositions, and always the last word ("Show Ignored Folders"). App Shortcut phrases follow Apple's rules too. The copy source carries the title-case variant for these keys; nothing converts case by algorithm.
- **Dense tools stay in sentence case.** Unity's Editor writing guide sets labels and buttons in title case while its button page says sentence case; Near AI resolves the conflict to sentence case, inside Unity-hosted tools too.
- **Eyebrows** are uppercase by style (`*-eyebrow`); the copy source stores them in sentence case.
- No exclamation marks. No ampersands in running text. No colons at the end of headings or labels. No periods on single-sentence labels, buttons or tooltips that are fragments; a tooltip that is a full sentence ends with a period, and so does every sentence in a two-sentence tooltip.
- Use the serial comma, and the ellipsis character (…) rather than three periods.

## Platform idioms

The copy source may carry a per-platform variant where idioms differ. Shells adapt only case and punctuation on their own; any other difference is a separate, reviewed string.

| Idiom | macOS | iOS, iPadOS | Android | Web, Windows, Linux |
|---|---|---|---|---|
| Account entry | "Sign in" for a Near AI account (Gateway moved from "log in" to "Sign in") | Sign in | Sign in | Sign in |
| Command that needs more input | Menu item ends with "…" ("Export Gateway…") | Menu item ends with "…" | No ellipsis | No ellipsis |
| Settings | Settings (Mod+,) | Settings | Settings | Settings |
| Leaving the app | Quit | Not shown | Not shown | Exit (Windows), Quit (Linux) |
| Pointer verbs in instructions | Click | Tap | Tap | Click, or a neutral verb in shared strings |
| Modifier names | Command, Option, Control, Shift | As macOS, with a hardware keyboard | Ctrl, Alt, Shift | Ctrl, Alt, Shift |
| Writing a shortcut | Command-F (symbols ⌘F in menus) | As macOS | Ctrl+F | Ctrl+F |

- In strings shared across platforms, prefer neutral verbs: choose, select, open.
- Name settings by path with the platform's own section names: "Settings > General > Appearance".
- Reserve "…" for commands that need more input and for overflow; never for a command that opens a plain window of information.

## Errors

Write every error as **Problem, Cause, Solution**: what did not happen, why, and what the person can do. Put it next to the thing it is about: an `InlineAlert` under the control or the action bar, a `Notice` with Retry for a section, a field message under the field.

| Avoid | Write |
|---|---|
| "Error: ingest failed (502)." | "Your traces weren't sent. The server that receives them didn't answer. Nothing has been lost; try again in a minute." |
| "Oops, something went wrong." | "The run stopped at step 4 of 6. The model didn't respond within 2 minutes. Retry from step 4, or change the instructions." |
| "Invalid name." | "Use 64 characters or fewer." |
| "Sorry, we couldn't connect." | "Couldn't reach Private AI. This computer is offline. Connect to the internet and try again." |

- Name the failure in the person's terms. A server that can't be reached is "Can't upload right now.", not its name, its host or its status code; a status line about the app's own health names what stopped working for the person.
- No "Error:" or "Warning:" prefix; the tone and glyph already say it. No apologies, no "oops", no blame, no "we".
- Keep exact, searchable wording for each failure, and put any code on its own detail line in mono for support ("Code 502").
- State field rules positively and show them before the person fails ("Use 64 characters or fewer"); validate after the field has been touched, never on the first keystroke.
- Never alert for a common, reversible action; offer Undo. Confirm only irreversible or consent actions, and name the action and object in the confirming button.
- A request that fails keeps what was already on screen. A reload never replaces held data with an error.

[Unity Foundations: errors and messaging] [HIG: alerts]

## Empty states

An empty state explains why nothing is here and offers the next step. It never holds crucial information, because it disappears.

| Kind | When | Copy pattern | Example |
|---|---|---|---|
| Blank | Nothing exists yet, or nothing matches | A full sentence, then one action | "Nothing is waiting." with **Add folder** |
| Filtered | A filter hides everything | Name the filter, offer to clear it | "No traces match Failed." with **Clear filter** |
| Idle | Nothing is selected | "Select ___ to ___", no action | "Select a trace to see what would be sent." |
| Day zero | First use | What this place is for, then a start | "Agents you connect appear here." with **Connect a tool** |

- Use `EmptyState`: centered, one title sentence, at most one line of support, at most one action, and an optional neutral glyph (Gateway's Traces list uses `tray` at 22). Never an error or warning glyph.
- Loading is not empty. Show a specific line ("Reading local queue…") or a `Spinner` with its words; an empty state appears only once the answer is "nothing".
- Unknown is not empty either. When the answer did not arrive, say so ("Status unavailable") and offer Retry.
- A surface that is empty because it has not started yet (Insights before any traces, Private AI before a tool is connected) shows a `GetStartedCard` in place of the content it explains: a title, numbered steps of a title over one line, at most one action (NDS-39). Sample data, when shown, sits under its banner and is never read as the person's own.
- New conversations offer suggested prompts as buttons, written as things the person would ask. A chat's welcome may instead greet with a title and a one-line question ("What's on your mind?") above the composer (NDS-44).

## AI copy

- **Disclose AI.** Label content an agent or model produced where it appears ("Drafted by Claude Code", "Summary written by an agent"). Never let a person think a human wrote it.
- **Say what is actually happening.** Progress text names the work in progress: "Reading 14 traces in ~/code/near/agents…", "Running tests, step 3 of 5…". Never "Processing…" or "Thinking…" alone. Show elapsed time counting up ("2 min") rather than an estimate you cannot keep.
- **Give confidence as reasons.** Never a bare percentage or "high confidence". State the evidence: "Matches 3 earlier runs that passed." "Based on the 2 files you attached." Proof states use their product's words (verified, pending, no proof, and the chat product's checking, signing, gateway signed) in a `ProofTag`, always with a dot or glyph. Proof copy claims only what was checked ("bound to this hardware and its measured code", never "matches the published build" when nothing compared it) and blames only the check the evidence names (NDS-43).
- **Set expectations up front.** Say what the feature can and cannot do before the first use, and say that output may contain mistakes where it matters ("Check the changes before you keep them.").
- **Confirm before acting for someone.** A significant or irreversible action an agent would take (sending, deleting, paying, publishing) waits for a confirmation that names the action and the object: **Send**, with "3 files, 42 KB, to Private AI" beside it. Reversible agent actions happen at once and offer Undo (NDS-15).
- **Keep stop and recovery words short and fixed.** **Stop** ends a run (Escape, Mod+.). **Retry**, **Edit** and **Undo** sit next to the output they affect.
- **Coach on refusals.** When output is blocked or poor, say what happened in plain words and suggest a better request; never scold.
- **Feedback** is voluntary: thumbs up and down named "Good response" and "Bad response", with an optional detail field.

See AI and agent patterns. [HIG: generative AI]

## Localization readiness

Gateway ships in English only today. Every product writes as if translation were next.
- **Never concatenate sentences or fragments.** Each sentence is one string with named placeholders: "{count} traces waiting in {folder}". Code never joins "Submit" + " " + "all".
- **Counts inflect in the copy source**, through plural rules (ICU MessageFormat or Fluent), for every count. A shell never decides singular or plural.
- **One key per use.** The same English in two places gets two keys, because other languages may need two words.
- **Leave room.** Labels grow 30–40% in German and Finnish, and short labels more. Buttons hug their labels; nothing is a fixed width in English.
- **No text in images or glyphs.** Localize any glyph that contains a character.
- **Format with the locale.** Dates, times, numbers and units come from locale formatters driven by the copy source's pattern.
- **Right-to-left.** Layout mirrors through leading and trailing: Back points right, progress fills from the right, the sidebar and the navigation rail move to the right edge. Never mirror numbers, code, paths, media playback controls, logos and marks, checkmarks, clocks, or controls that point to real directions. Never reverse the digits inside a number; reverse the order of items in a counting sequence. Align a paragraph of three or more lines by its own language, which matters for mixed-language agent output; give every item in a list the same alignment. Set Arabic or Hebrew text about 2pt larger beside all-caps Latin.
- **The iPhone Duo exception.** On iPhone Duo, the vertical bar on the trailing hardware edge (status, toolbar, tab bar) is fixed to the hardware and does not mirror in right-to-left languages. Material's navigation rail does mirror.
- Test with a pseudo-locale that lengthens strings and one that flips direction.

[HIG: right to left] [M3: bidirectionality]

## Single-sourced copy

Copy is single-sourced per product (NDS-16).
- **One copy source owns every sentence.** In Gateway it is the Rust core (`crates/trace-commons-contributor`): a sentence is composed once and every shell reads it. Sentences cross to the shells already assembled, counts already inflected; a chosen sentence crosses as a `_line` and `_tone` pair.
- **Components author no words.** Every label, accessible name, value word, tooltip, placeholder and empty-state sentence is passed in by the consumer. A missing word renders empty; no component or shell supplies a fallback literal.
- **Shells adapt case and punctuation only.** A shell may apply the Apple title-case variant or the macOS ellipsis. It never paraphrases.
- **Web and mobile read the same sentences.** They come from the copy source at build time (string catalogs generated from it) or from the same core at runtime; nobody retypes them.
- **Ratchets keep it that way.** Gateway's `ShellWordingTests` hold per-file sentence ceilings and floors (19 surfaces at zero), `NudgeWordingTests` ban 28 fragments, and the FFI copy ratchet fails if a pinned core sentence appears as a Swift literal. Windows and GTK carry the same ratchet. Every product adopts the equivalent, and baselines only move down.
- **New consent wording is drafted, never built.** Draft consent sentences are listed as "Draft, needs approval" and stay out of builds until approved.
- **Other drafts are marked until approved.** A new non-consent sentence may ship marked DRAFT in the copy table; the owner approves drafts line by line. The owner's own words are recorded as approved when they land.

## Do and don't

- Do lead with what happened to the person's data, in their words.
- Do write buttons as one or two words that name the action, with the consequence beside them.
- Do keep one word per concept ("trace", not "session"), and show unknown as unknown.
- Don't promise privacy or security, name the mechanism, or use "we".
- Don't apologize, prefix "Error:", or put an error glyph in an empty state.
- Don't build a sentence from parts, branch on a count in a shell, or write words inside a component.
