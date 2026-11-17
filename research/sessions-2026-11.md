# Design decisions from the product sessions (2026-09-15 to 2026-11-03)

The system's first version (2026-10-13) was derived from trace-commons' source code. Between 2026-09-15 and 2026-11-03 the owner designed three products in Claude Code sessions, and many of those decisions either came after the system was written or were never written into it. This note records where NDS-22 to NDS-50 came from, so a later reader can check them against their source.

## What was read

62 sessions, reduced to the owner's prompts and the assistant's replies (tool output dropped), about 2.9 MB of text. Each finding was checked against the product repositories on 2026-11-03.

| Product | Repository | Sessions | Dates | State checked against |
|---|---|---|---|---|
| Gateway (the macOS app, called Trace until 2026-11-04; bundle "Near.ai") | trace-commons | 55 | 2026-09-15 to 11-03 | `main` at `e2a1ad9d7` (2026-11-03) |
| Private chat ("Private AI", "Near AI private Chat") | nearai/LibreChat | 5 | 2026-10-23 to 11-03 | PR #4 (proof seal) and PR #5 (Near AI OS shell), both open |
| Marketing site for the macOS app | nearai-gateway-website (was nearai-macos-website) | 2 | 2026-10-27 to 11-04 | `main` at `865dab2` |

The sessions that matter most, by product:

- **trace-commons.** #1146 WYSIWYG front-end refactor (09-29); TCDesign glass contract and token source (10-02); menu-bar and FTUX reviews (10-05); app cleanup, nudges, edge rail and theme exploration (10-08 to 10-12); the parent design system's commissioning (10-13); Insights (10-15); design cleanups (10-15 to 10-21, #1460, #1490, #1514); menu-bar item (10-21, #1539); animated first run (10-21 to 10-22, #1558); design cleanup (10-23, #1585); app icons (10-26, #1663); tooltips (10-27, #1672); AI Balance card (10-27, #1755); the Cyber-Classical theme trial (10-27, scrapped); window placement (10-30, #1775); design updates (11-02, #1888); the design comparison (11-03).
- **nearai/LibreChat.** Near AI OS UX architecture (11-03, PR #5); verification UI for attestation (11-03, PR #4); per-check attestation results (11-03); the Private Chat design comparison (11-03).
- **nearai-gateway-website.** The site build (10-27 to 10-30), element by element after a full retheme was reverted; the version archive (11-03).

## Decision sources

| ID | Product | Session (date) | Shipped as |
|---|---|---|---|
| NDS-22 | trace-commons | Design cleanup and updates (10-19) | #1514; flat themes track the parent since 10-20 |
| NDS-23 | trace-commons | TCDesign glass contract (10-02) | R14 in `GlassBackdrop.swift`, `GlassStyle.swift` |
| NDS-24 | trace-commons | #1146 refactor (10-05, web) and Design clean up (10-19, macOS) | #1146 (web, unmerged), #1460 |
| NDS-25 | trace-commons | Design clean up (10-19); Design updates (11-02) | #1481 (`GlassPopoverNotice`), #1888 |
| NDS-26 | trace-commons, LibreChat | Animated FTUX (10-21 to 10-22); Near AI OS UX architecture (11-03) | #1558 (`GlassBrandMarkDrawing`); LibreChat PR #5 |
| NDS-27 | trace-commons, LibreChat, website | Design cleanup (10-23); UX architecture (11-03); site build (10-28) | #1585 (`GlassNearWordmark`); PR #5; `865dab2` |
| NDS-28 | trace-commons | PR #1857 (11-02); design comparison (11-03) | #1857 (guard test `no_commons_name_in_copy`) |
| NDS-29 | trace-commons | App UI cleanup (10-09) | #1303 |
| NDS-30 | trace-commons | Design updates (10-12); staging-audit rulings (10-29) | #1747, #1749, #1750 |
| NDS-31 | trace-commons | General fixes (10-08); Design cleanup (10-23); staging audit (10-29) | #1585, #1765 |
| NDS-32 | trace-commons | Animated FTUX (10-21 to 10-22) | #1558, revised by #1584, #1611, #1685, #1784 |
| NDS-33 | trace-commons | Menu bar icon and UI (10-21); Design cleanup (10-23) | #1539, #1585 |
| NDS-34 | trace-commons | Design cleanup (10-23); staging audit (10-29) | #1585, #1888 |
| NDS-35 | trace-commons | Design clean up (10-19 to 10-20); window placement (10-30) | #1490, #1775 |
| NDS-36 | trace-commons | Design updates (11-02) | #1888 (`GlassRefreshPill`) |
| NDS-37 | trace-commons | Design clean up (10-15); Design updates (11-02) | #1460, #1888 (`GlassRuleTabs`) |
| NDS-38 | trace-commons | Design cleanup (10-22 to 10-23) | #1585 |
| NDS-39 | trace-commons | Design updates (11-02) | #1888 (`GetStartedCard`, `InsightsSampleBanner`) |
| NDS-40 | trace-commons | AI Balance card (10-27); Design updates (11-02) | #1755, #1888 |
| NDS-41 | trace-commons | General fixes (10-10); Design updates (11-02) | #1888 |
| NDS-42 | trace-commons | #1235 FTUX review (10-05); App UI cleanup (10-08) | on `main` before 10-13 |
| NDS-43 | LibreChat | Verification UI for attestation (11-03) | PR #4, open |
| NDS-44 | LibreChat | Near AI OS UX architecture (11-03) | PR #5, open |
| NDS-45 | website | Site build (10-27 to 10-30) | `751a349`, `ada2f16`, `865dab2` |
| NDS-46 | trace-commons | Cyber-Classical light and dark themes (10-27) | not committed |
| NDS-47 | trace-commons | Apple app icons from the Near AI logo (10-26) | #1663 |
| NDS-48 | all | The owner's review of this update (11-04) | this repository |
| NDS-49 | LibreChat | The owner's review of this update (11-04) | this repository |
| NDS-50 | trace-commons | The owner's review of a side-by-side comparison (11-04) | this repository; trace-commons still to apply |

## What was not adopted

- **The chat's breakpoints and drawer.** LibreChat keeps its stock 640 and 768 breakpoints and a navigation drawer below 768. The owner ruled on 2026-11-04 to leave them out of the system for now (NDS-49), so NDS-12 and NDS-13 stand.
- **The chat's stronger hover steps.** The owner asked for more contrast on list and picker selection; the chat drew opaque grey steps on its opaque shell. The parent's `row-hover` already matches the lighter step, so no role changed; an opaque shell steps its own greys.
- **The current chat as an accent tint.** The chat marks the open conversation with `accent-tint` instead of `selection`. The assistant chose it and the owner did not answer, so `Sidebar` records it as the chat's variant.
- **Marketing copy.** "Private by default, always" and "Paid with your Near AI credit" break app-surface rules; open question 8.
- **The Cyber-Classical app theme.** Scrapped (NDS-46). The site keeps its own Cyber-Classical-derived look under NDS-45.
- **Hero promotion gradients on Gateway's Home.** Shipped in trace-commons but not ruled on as a system rule; `Card` keeps "no two-hue gradient" and records Gateway's state.

## How to repeat this

Session transcripts live under `~/.claude/projects/<project>/*.jsonl`. Keep only `user` and `assistant` text blocks, drop tool results, read them in date order, and check each decision against the repository's `main`. Later sessions overrule earlier ones; a decision in an open PR is the owner's direction until the PR lands or is withdrawn.
