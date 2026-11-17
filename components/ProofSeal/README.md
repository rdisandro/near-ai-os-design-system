# ProofSeal

A seal drawn from a deployment's attested signing key: a guilloché that only that key can produce, shown wherever a proof from that key appears, so a person can see at a glance that the header's proof and a reply's signature come from the same model (NDS-43).

## When to use

- Where a deployment signs its replies with an attested key: as the glyph of the header proof pill (the deployment's checks), of each reply's `ProofTag`, and at the top of their popovers.
- On the verification page for a deployment, large, with its seal code.
- Not where proof is a ledger fact without a key (Gateway's Private AI ledger keeps the plain `ProofTag` glyphs). Not as decoration, a logo or a loading animation.

## Anatomy

Drawn in a 200-unit box centered on the origin, with 0.9 non-scaling strokes.

1. **Bands**: two woven rings, `r = 84 + amp · sin(lobes · t + phase + j · π)` for j = 0, 1, with lobes 14 to 20 and amp 4 to 5.5. Stroke `proof-text`.
2. **Rose**: three petal curves, `r = 58 + amp · sin(lobes · (t + turn)) · (0.65 + 0.35 · cos(wave · t + phase))`, with lobes 5 to 9, wave 2 to 4, amp 12 to 16, each turned a third of a lobe from the last. Stroke `accent-soft`.
3. **Parameters**: bytes 0 to 6 of the key choose band lobes, band amp, band phase, rose lobes, rose wave, rose amp and rose phase. The same key always draws the same seal.
4. **Center**: a 10-lobe badge, 40% of the seal, in `proof-text` with a check in `proof-tint`; a spinner while checking; a cross on `critical` when the check failed; a dash when there is nothing to check.
5. **No key**: a dashed ring at r 84 in `rule` in place of the bands and rose.
6. **Seal code**: the first four and last four hex digits of the key, uppercase, joined by "·" ("89FB·4350"), in `<tier>-mono`, with Copy. This is the seal's text form.
7. **Match box** (reply popover): the seal at 20 and one sentence on `proof-tint` saying whether this reply's seal matches the header's, with "Show in header".

## Sizes

| Where | Size | Notes |
|---|---|---|
| Verification page | 160 or more | With the seal code under it |
| Header popover | 56 | The deployment's seal |
| Reply popover | 44 | The signing key's seal |
| Header proof pill | 20 | The rose drops out at glyph sizes; the bands and badge remain |
| Reply `ProofTag` | 14 | Same |

## Variants

- `--verified` (default): bands, rose, badge with a check.
- `--checking`: a spinner in the center; the bands appear only once the key is known.
- `--failed`: the bands of the key that was presented, a `critical` badge with a cross.
- `--none`: no key yet, or a signature that is not the model's (Gateway signed): the dashed ring and a dash.

## States

| State | Treatment |
|---|---|
| Evidence arrives | The seal stamps in once (scale 0.9 to 1, opacity 0.4 to 1) on `spring-expressive`, about 9% overshoot (the Near AI chat uses 420 ms), and one shine crosses it 250 ms later over 900 ms (`--stamp`). Only when the result arrives, never on a timer. |
| Shown again | Drawn at rest. A seal never replays its stamp on scroll or reopen. |
| Show in header | The header pill pulses its ring twice (1100 ms each); the seal itself does not move. |
| Reduce Motion | No stamp, no shine, no spin; the center glyph shows the state. |
| Increased contrast | Strokes and badge as in the standard theme; the host pill takes its `edge-hc` edge. |
| Forced colors | Every stroke and the badge in `CanvasText`, the check in `Canvas`. |

## Behavior

- The seal is drawn on the client from the key the attestation returns, so the drawing is the evidence, not an image the server sends.
- Same key, same seal: the header and every reply signed by the deployment show identical seals; a reply signed by another key shows a different one, and its popover says so in words.
- The seal never stands in for the proof word. The tag or title around it always carries "Verified", "Checking" or "Check failed".

## Accessibility

- The drawing is hidden from assistive technology. The proof word, the popover title and the seal code are text.
- The seal code is selectable and copyable, and read digit by digit ("Seal 8 9 F B, 4 3 5 0") through its accessible label from the product.
- Every state differs by its center glyph and its word, never by color alone.
- `proof-text` on `proof-tint` holds 4.5:1 (7:1 in the `-hc` themes); the bands and badge hold 3:1 against the popover.
- **The product supplies**: the key, the seal code's label, every word around the seal.

## Platforms

| SwiftUI/AppKit (macOS) | SwiftUI/UIKit (iOS/iPadOS) | Jetpack Compose M3 | Web |
|---|---|---|---|
| A `Shape` built from the key's parameters, stroked with `StrokeStyle(lineWidth: 0.9)` in a `Canvas` | Same | `Canvas` with `drawPath` and a `Stroke(width = 0.9f)` | Inline SVG (`.nr-proof-seal`) with `vector-effect: non-scaling-stroke`, paths computed from the key at render |

## Do and don't

- Do draw the seal from the key on every surface; never ship it as a static image.
- Do show the seal code beside any seal large enough to read, so people can compare seals in words.
- Don't animate the seal while waiting. A spinner in the center is the waiting state; the stamp is the arrival.
- Don't use the seal for a call with no key, a gateway-only signature or an outside model.
- Don't recolor the seal with a product accent beyond `accent-soft` in the rose.

## Source

Intentional addition from the Near AI chat: `Seal.tsx` and `geometry.ts` (the guilloché and seal code), `Shield.tsx` (header pill) and `Signature.tsx` (reply tag) in nearai/LibreChat PR #4 (open), which apply the owner's "Verification UX concepts" canvas, Direction C (2026-10-16 to 10-22): "the animation is the evidence arriving, never a timer" and "the same seal shows in the header popover and under every reply signed by that deployment."
