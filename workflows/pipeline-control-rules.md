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

## 4. KLING / VIDEO FALLBACK — CANONICAL ROUTE

- Agent 06 attempts video production only when an approved video execution tool is available and authorized.
- If video execution is unavailable, fails, or lacks credits/quota/access: Agent 06 sets VIDEO_PRODUCTION_BLOCKED = TRUE with BLOCK_REASON and reports to Agent 01 ONLY. Agent 06 does not route directly to Agent 05.
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
