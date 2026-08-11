# PIPELINE CONTROL RULES — CANONICAL REFERENCE

Single source of truth for cross-agent control-flow mechanics referenced by Agents 01–08. Agent-specific responsibilities remain defined in each agent's own README; this file defines only the shared mechanics that must behave identically regardless of which agent triggers them.

## 1. QC REVISION-CYCLE CAP

Applies whenever Agent 07 returns QC_REVISION_REQUIRED for a specific defect on a specific asset/package.

- Each revision attempt on the SAME defect increments REVISION_COUNT for that defect.
- Maximum 3 revision cycles are allowed for the same defect on the same asset.
- On each QC pass, Agent 07 must identify: BLOCKING_DEFECT, RESPONSIBLE_AGENT, REVISION_COUNT.
- If the same BLOCKING_DEFECT remains unresolved after REVISION_COUNT = 3:

  status = ESCALATION_REQUIRED

  route to Agent 01.
- Agent 01 then decides one of: revise the strategy (route to Agent 03), replace the asset/concept, or request Daryna's direct decision.
- No agent may attempt a 4th automatic revision cycle on the same defect without Agent 01's explicit decision.
- Different defects on the same asset each get their own REVISION_COUNT (fixing hook wording does not consume the visual-quality counter, etc.).

## 2. QC_BLOCKED vs PRODUCTION_BLOCKED

**QC_BLOCKED** — Agent 07 cannot complete review because required evidence, input, or an asset is missing or unverifiable. This is a QC-stage state (Agent 07's QC_DECISION field).

**PRODUCTION_BLOCKED** — production cannot continue because a required production dependency (tool access, credits, missing asset, unresolved product fact) is unavailable. This is a run-level state (Agent 01's FINAL_STATES).

Routing (applies to any agent that detects a block, not only Agent 07):

- The agent that detects the block reports a structured BLOCK_REASON to Agent 01. It does not resolve the block itself and does not invent the missing information.
- Agent 01 determines the recovery route (retry, reroute to another specialist, request clarification from Daryna, or fallback per Section 4).
- A QC_BLOCKED result (from Agent 07) becomes a run-level PRODUCTION_BLOCKED only if Agent 01 cannot unblock it through routing.

## 3. CONCEPT SELECTION AUTHORITY

- Agent 03 evaluates the available strategic directions and RECOMMENDS/RANKS the strongest concept using its strategic decision criteria.
- Agent 01 holds final orchestration approval authority: it approves Agent 03's recommended concept, or sends it back to Agent 03 if evidence is insufficient, before production proceeds.
- No other agent (04, 05, 06, 07, 08) may independently replace the approved concept.
- Any material change to the approved concept, once production has started, must route back through Agent 01 for re-approval before continuing.

## 4. KLING/REMOTION VIDEO FALLBACK — CANONICAL ROUTE

- Agent 06 attempts video production only when an approved video execution tool is available and authorized. See §11 for how Agent 06 selects between KLING, REMOTION, and KLING_PLUS_REMOTION for a given concept — that selection happens before this fallback chain is relevant.
- If Kling is unavailable, fails, or lacks credits/quota/access: Agent 06 does not go straight to a static fallback. It first checks whether the SAME approved concept can be produced with Remotion alone from existing approved assets (previously generated clips, approved covers/photos, typography, captions, transitions, music) — no new AI motion generation required.
  - If yes: produce it with Remotion. This is a full video deliverable, not a degraded fallback — Agent 06 returns VIDEO_READY_FOR_QC through the normal path, `PRODUCTION_TOOL: REMOTION`.
  - If no (the concept genuinely requires AI-generated motion/footage that doesn't exist and can't be assembled from approved material): Agent 06 sets VIDEO_PRODUCTION_BLOCKED = TRUE with BLOCK_REASON and reports to Agent 01 ONLY. Agent 06 does not route directly to Agent 05.
- Agent 01 then routes the SAME approved concept to Agent 05 for the strongest feasible static alternative (carousel, single-image post, or Story package) — whichever best preserves the original objective.
- The fallback must preserve: the same core concept, the same campaign objective, the same product truth — unless Agent 01 explicitly authorizes a strategy change (in which case it routes back through Agent 03 first).
- The fallback package still passes through Agent 04/05 as needed and then Agent 07 QC before owner review.

## 5. ANTI-REPETITION — CANONICAL TAXONOMY

Single classification enum, used identically by every agent that performs anti-repetition evaluation:

NEW
ACCEPTABLE_ITERATION
TOO_REPETITIVE

Dimensions checked (at minimum): topic, concept, hook, angle, format, visual concept, CTA, copy pattern, story structure (where relevant).

Role split:

- **Agent 02** supplies competitor/trend intelligence and recent-history evidence. It does not issue the final classification, only flags candidates for evaluation.
- **Agent 03** applies the canonical classification during strategy/concept planning, using Agent 02's evidence plus LiorTales history.
- **Agent 07** performs the final anti-repetition QC check before approval, using the same canonical classification, as the last gate before a package can be QC_APPROVED.

A TOO_REPETITIVE classification at any stage requires a materially improved variation, not a synonym-level change.

## 6. HANDOFF TO AGENT 05 — CANONICAL CONTRACT

Before Agent 05 begins visual production work, it must receive, jointly from Agent 03's Content Strategy Brief and Agent 04's Copy Package:

RUN_ID
APPROVED_CONCEPT
TARGET_PLATFORM
SELECTED_FORMAT
PRIMARY_OBJECTIVE
PRIMARY_AUDIENCE
HOOK (direction from Agent 03, final wording from Agent 04)
CONTENT_STRUCTURE (story structure / slide structure)
CREATIVE_BLUEPRINT (full — see §8; not summarized)
COPY_OR_SCRIPT (final audience-facing copy from Agent 04)
CTA (objective from Agent 03, final wording from Agent 04)
REQUIRED_PRODUCT_FACTS
PROHIBITED_CLAIMS
VISUAL_CONSTRAINTS (brand rules, continuity requirements)
ANTI_REPETITION_STATUS / CONSTRAINTS

If any of these fields is missing or contradictory, Agent 05 does not guess. It returns VISUAL_INPUT_INCOMPLETE and requests correction through Agent 01 — never directly interrogating Agent 03 or Agent 04 in a way that bypasses orchestration.

## 7. FINAL STATIC ASSET EXECUTION

- Agent 05 owns visual creative direction AND is the production owner for the FINAL_VISUAL_ASSET on static formats (single image, carousel, Story package), unless a separate approved execution tool/agent is explicitly designated for a given run.
- Agent 06 remains the sole production owner for video/Reel assets.
- Agent 07 never generates, edits, or produces any asset. It reviews only.
- Agent 01 orchestrates the handoff but does not silently execute creative work itself.

## 8. COMPETITOR BENCHMARK & COMPARATIVE CREATIVE GATE

Canonical rubric for connecting real competitor evidence to a stronger original LiorTales execution, and for verifying that strength survives all the way to the finished asset. Used by Agent 03 (building the Creative Blueprint), Agent 07 (the pre-production Competitor Comparison Gate and the post-production Concept Fidelity check), and received in full by Agents 04 and 05.

**Creative Blueprint fields** (Agent 03 builds this from Agent 02's PER-REFERENCE EVIDENCE before anything reaches Agent 04 or Agent 05):

REFERENCE (competitor + URL)
MECHANIC_TO_KEEP
WHAT_NOT_TO_COPY
LIORTALES_UPGRADE
FIRST_FRAME
FIRST_3_SECONDS
PEOPLE_PRESENT
ACTION_SEQUENCE
EMOTIONAL_PROGRESSION
PRODUCT_REVEAL
CAMERA_AND_COMPOSITION
PACING
PAYOFF
WHY_OUR_EXECUTION_IS_STRONGER

A concept without a concrete event, reveal, change, or reaction is INVALID and must not proceed. Atmosphere descriptions ("warm," "cozy," "magical," "happy family") are never a substitute for this event sequence, and no agent downstream of Agent 03 may collapse the blueprint back down to one.

**Comparative scoring dimensions** (score both the REFERENCE and the PROPOSED LiorTales execution, 1–10 each):

HOOK
CURIOSITY
EMOTION
HUMAN_REALISM
STORY
SCROLL_STOP_POWER
PRODUCT_DESIRE
MEMORABILITY

**Pass condition**: the LiorTales execution must show credible improvement over the reference in at least 3 of these 8 dimensions. A merely-acceptable score on its own is not sufficient.

**Fail condition**: fewer than 3 improved dimensions → STATUS: FAIL → route back to Agent 03. The concept must not reach Agent 04, Agent 05, or any generation tool while failing.

This rubric is applied at two distinct points in a run:

1. **Pre-production** (Agent 07, before Agent 04/05 begin work): reference vs. Creative Blueprint.
2. **Post-production** (Agent 07, after generation): the finished asset is checked for fidelity to the *approved* blueprint (did the event survive generation?) — this is Agent 07's Concept Fidelity QC area, not a re-run of the comparative score from scratch.

## 9. PRODUCT ASSET LOCK (BOOK COVERS)

Canonical rule for any content depicting a LiorTales book. The confirmed approved master covers (registry: `shared/product/product-bible.md` §18) are locked product assets — each is a complete, immutable image, not a description to reinterpret.

**Whenever a book appears in a concept**, Agent 03's Creative Blueprint must name:

BOOK_USED
APPROVED_MASTER_COVER
CANVA_ASSET (the exact asset ID from the registry)
WHERE_THE_BOOK_APPEARS
HOW_THE_COVER_REMAINS_VISIBLE
PRODUCT_FIDELITY_METHOD

Generic wording ("a personalized children's book") is invalid whenever a real LiorTales book is shown — a specific title from the confirmed registry must be selected.

**Never regenerate the cover.** The approved cover image must never be redrawn, regenerated, approximated, redesigned, recolored, retitled, re-typeset, given different characters, or substituted with a similar or generic AI-generated book. The complete existing cover image is immutable.

**Generation method:** never ask a generative tool (Canva, Kling, OpenAI, or other) to recreate, redraw, approximate, or edit the cover artwork itself — this includes masked/inpainting-style generative edits confined to the cover region. Masking a region so a generative model can fill it is not compositing, and is forbidden for cover pixels regardless of how small the masked area is. The only acceptable method is: generate the surrounding human scene/motion with a neutral placeholder book-cover plane, then deterministically composite the exact approved cover asset onto that plane — a geometric transform (e.g. perspective warp) of the source file's own pixels, never a second generative pass over the cover region. Canonical implementation and contract: `shared/production-tools/openai-image-pipeline.md`. For video, if generation mutates the cover, generate the human motion separately and insert/track the exact approved cover asset during editing using the same deterministic method.

**PRODUCT_ASSET_MISSING**: if the selected approved cover asset cannot be accessed, STOP. Never substitute another book. Report as a block per §2 routing (to Agent 01).

**QC**: Agent 07 verifies the final asset against the named Canva source asset — see the Product Asset Identity QC area in `agents/07-quality-control-brand-guardian/README.md`.

Referenced by Agents 03, 05, 06, and 07 rather than duplicated.

## 10. HANDHELD PRODUCT COMPOSITING — CAPABILITY GATE

Applies whenever a concept requires a person to physically grip/hold an approved LiorTales book, cover-first, in frame — distinct from the book resting, standing, propped, or otherwise visible without being gripped by a hand. The general §9 compositing method ("perspective, scale, and masking adjustments only") is proven reliable for placements where the book is not hand-gripped; it is not, by itself, sufficient for handheld shots.

**Capability test** — before any handheld concept proceeds to generation, confirm the currently available production tools can simultaneously preserve all four of:

1. the exact approved cover (§9 — unaltered pixels);
2. realistic physical book geometry (thickness, edges, spine/page block);
3. natural hand/finger occlusion (fingers convincingly in front of or wrapped around the book);
4. believable contact shadows and scene-matched lighting.

**If the available tools cannot verifiably satisfy all four simultaneously:**

status = HANDHELD_PRODUCT_COMPOSITING_UNSUPPORTED

This is not a run-level block and must not stop the content workflow or be escalated to Daryna as a failure. The agent that would have produced the handheld shot (Agent 05 for static, Agent 06 for video) reports HANDHELD_PRODUCT_COMPOSITING_UNSUPPORTED to Agent 01, which routes the SAME approved concept back through Agent 03 for an automatic redesign into the strongest non-handheld composition that preserves the same emotional event, people, and payoff.

**Redesign, do not downgrade.** The people, reaction, story, surprise, humor, and scroll-stop power of the original concept must remain equally strong. Preferred non-handheld compositions (select whichever best fits the concept, not a fixed order):

- the approved book standing or propped on a table/surface while the child/family reacts beside it;
- the approved book revealed inside an open gift box;
- the book lying naturally on a bed/table while the child points at or gestures toward it;
- the child mid-unwrapping, with the approved book already visible beside/in front of them, not yet gripped;
- the book positioned in the foreground (resting, not held) while the parent/child emotional interaction happens behind or around it;
- other arrangements where the exact approved cover remains a separate, cleanly composited flat product placement — not held in a hand — and still reads as physically believable.

**Never invent a replacement cover to enable a handheld shot.** If no non-handheld redesign can preserve both the required emotional event and the exact approved cover, that is a §9 PRODUCT_ASSET_MISSING-class stop — not a license to substitute AI-generated book art.

**Reserved for real handheld shots:** a hand genuinely gripping the exact book cover, with correct geometry, occlusion, and shadow, is reserved for (a) an actual photograph of a real printed LiorTales proof copy, or (b) a production tool verified to support true perspective-correct compositing with occlusion masking. The OpenAI scene-generation + deterministic cover-compositing pipeline (`shared/production-tools/openai-image-pipeline.md`) is a candidate for (b) — it is not the prior Canva/Kling flat-overlay toolset — but passing through that pipeline is not itself a pass: each shot still must clear the four-criteria Capability Test above before being accepted as handheld-realistic, including confirming an occlusion mask was actually supplied and used.

Referenced by Agents 03, 05, 06, and 07 rather than duplicated.

## 11. VIDEO PRODUCTION ROUTE SELECTION (KLING / REMOTION)

Canonical routing logic for Agent 06 choosing how to produce a video asset. Remotion (`shared/production-tools/remotion-video-pipeline.md`) is an additional execution tool alongside KlingAI — not a replacement, and not a second, parallel video-production architecture. Both tools operate inside Agent 06's existing ownership, inputs, quality standards, PRODUCT ASSET LOCK obligations (§9, §10), and handoff-to-Agent-07 contract; only `PRODUCTION_TOOL` changes.

**KLING** — use when the concept requires AI-generated realistic human motion that doesn't already exist: cinematic family scenes, gifting moments, children interacting naturally, or other footage that must be generated rather than assembled from existing material.

**REMOTION** — use when the video can be produced by programmatic assembly of already-existing approved material: approved LiorTales book covers, product images, photos, previously generated clips, typography, captions/subtitles, transitions, motion graphics, slide/carousel-style sequences, hook/CTA/end-card overlays, and music/audio where available. Remotion is deterministic, code-driven composition — the same category of tool as the deterministic image compositor, not a generative model.

**KLING_PLUS_REMOTION** — use when a concept needs both: Kling generates the AI motion/footage first, then Remotion assembles the finished Reel from that footage plus captions, typography, transitions, hook/CTA overlays, music, and any approved product assets, and renders the final file.

**Selection is Agent 06's to make**, based on the Creative Blueprint and Visual/Video brief it receives — not a question to route to Daryna. Route to Daryna only if the brief itself is genuinely ambiguous about whether new footage must be generated (a missing-input problem, handled as `VISUAL_INPUT_INCOMPLETE`/`QC_INPUT_INCOMPLETE` per the normal missing-input routing) — not as a routine production choice.

**PRODUCT ASSET LOCK applies identically regardless of route.** Remotion must place the exact approved cover/asset file exactly as provided — never redraw, regenerate, approximate, or replace it. Remotion's deterministic placement model means it cannot itself introduce a generative cover-fidelity failure, but Agent 06 must still supply the exact registered source file, not a description of it, and Agent 07 QC (areas 15/16) applies at whatever the finished asset shows regardless of which tool(s) produced it.

**Fallback interaction:** see §4. If Kling is blocked, Agent 06 checks REMOTION feasibility on the same concept before escalating to Agent 01 for a static fallback — Remotion is attempted before the concept is downgraded to static, not after.

Referenced by Agent 06, and by Agent 07 when reviewing `PRODUCTION_TOOL` on a video package.

## 12. STATIC/CAROUSEL VISUAL PRODUCTION ROUTE (OPENAI-PRIMARY)

Canonical routing logic for how Agent 05 sources the core imagery of static/carousel assets. OpenAI image generation (`shared/production-tools/openai-image-pipeline.md`, tooling: `tools/openai-image-pipeline/`) is the primary visual generator for carousel core lifestyle imagery — Canva is no longer the default source of that imagery, and Canva's own AI image generation is not an acceptable substitute for it. This section does not replace or duplicate §9 (PRODUCT ASSET LOCK) or §10 (HANDHELD PRODUCT COMPOSITING) — both apply identically under this route whenever a slide depicts an approved book cover.

**Mandatory precondition — storyboard.** Before any generation, Agent 05 must produce the slide-by-slide storyboard defined in `agents/05-visual-creative-director/README.md` §STORYBOARD. Generation without an approved storyboard is not a valid production step.

**OPENAI_VISUALS + EXACT_PRODUCT_COMPOSITING + CANVA_ASSEMBLY** — the default route:
1. Agent 05 generates each slide's core lifestyle/scene imagery with `generate_scene.py`, per the storyboard (people, environment, emotional beat, framing). Slides that do not depict a book cover use this output directly as the finished core image — there is no compositing step for them.
2. Whenever a slide depicts an approved LiorTales book, the exact registered cover is composited onto the generated scene per §9's deterministic method (`compose_cover.py`) — OpenAI never generates, redraws, or approximates cover artwork at any point, for any slide.
3. Canva assembles the finished slide on top of the generated imagery: typography, logo, CTA, graphic accents, spacing, and export. Canva is an assembly layer under this route, not a generation source — do not let Canva's own AI image generation or template layouts replace or substitute the generated imagery, and avoid defaulting to a Canva-template aesthetic.

**CANVA_ASSEMBLY (fallback)** — used only when the OpenAI route is unavailable, blocked, or fails (credits, quota, access, or a `PRODUCT_ASSET_MISSING`/capability-gate stop per §9/§10): Canva may assemble a carousel from already-approved, previously-generated, or previously-QC-passed imagery only. Canva's own AI image generation must not be used as a default fallback for core imagery — falling back to it requires the same block/escalation routing as any other production-tool failure (§2), not a silent substitution.

**Selection is Agent 05's to make**, based on the storyboard and the Creative Blueprint — not a question routed to Daryna, unless the input itself is genuinely incomplete (`VISUAL_INPUT_INCOMPLETE`, per §6's missing-input routing).

**Composition variety and QC are unchanged by this route.** The 2-slide composition-repetition cap (`shared/brand/visual-identity-guide.md` §12; `agents/05-visual-creative-director/README.md` §CAROUSEL) and Agent 07 QC area 17 apply identically regardless of which tool generated the imagery.

Referenced by Agent 05, and by Agent 07 when reviewing imagery source/`PRODUCTION_TOOL` on a static/carousel package.
