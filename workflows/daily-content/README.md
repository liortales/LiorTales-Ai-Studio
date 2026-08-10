# DAILY CONTENT WORKFLOW

The execution contract used when the LiorTales Daily Routine starts a content-production run. It connects the existing 8 agents into one deterministic pipeline. It does not define new agents or new responsibilities — it sequences the responsibilities already defined in `agents/01-…` through `agents/08-…/README.md`, and defers to the canonical governance files for shared control-flow rules:

- `workflows/pipeline-control-rules.md` — revision-cycle cap, QC_BLOCKED/PRODUCTION_BLOCKED, concept-selection authority, Kling/video fallback route, anti-repetition taxonomy, Handoff-to-Agent-05 contract.
- `shared/brand/language-policy.md` — Russian/American-English language policy.
- `shared/platform-rules/platform-and-publishing-policy.md` — platform list, Etsy classification, scheduling ownership.

**The system has exactly 8 agents. This document does not create a 9th.**

## PURPOSE

DEFAULT MODE: REVIEW_MODE.

PRIMARY RULE: every scheduled daily run produces exactly ONE strongest finished content package.

Possible finished formats:

- Reel / short-form video
- single-image post
- carousel
- Story package containing 1–3 connected frames

Do not produce multiple unrelated finished concepts in one daily run.

## SYSTEM ENTRY

A run begins when triggered by:

1. scheduled LiorTales Daily Routine;
2. manual Run Now;
3. explicit manual content-production request from Daryna.

Agent 01 creates the run record:

RUN_ID
RUN_TYPE
OPERATING_MODE
OBJECTIVE
RUN_DATE
AVAILABLE_TOOLS
AVAILABLE_EVIDENCE
PLATFORM_CONTEXT
PRODUCTION_CONSTRAINTS
REVISION_COUNT = 0

Agent 01 is the orchestration authority for the complete run (`agents/01-content-director/README.md`).

## STAGE 1 — AGENT 02: RESEARCH & INTELLIGENCE

Agent 01 sends the research task to Agent 02.

Agent 02 evaluates current trends, competitor/content patterns, audience signals, platform opportunities, recent LiorTales content, and available analytics evidence — labeling each item FACT / OBSERVED_PATTERN / INFERENCE / OPPORTUNITY / RISK.

Agent 02 returns its structured intelligence brief (Handoff-to-Agent-03 package — see `agents/02-competitor-trend-intelligence/README.md`).

Agent 02 does NOT choose the final content concept.

NEXT: Agent 03.

## STAGE 2 — AGENT 03: STRATEGY & CONCEPT RECOMMENDATION

Agent 03 receives RUN_ID, OBJECTIVE, Agent 02's intelligence, available performance evidence, recent-content history, and production constraints.

Agent 03 identifies the strongest audience opportunity, determines the primary objective, recommends/ranks the strongest concept, proposes platform and format, establishes content angle and CTA objective, and checks strategic repetition (canonical taxonomy, see ANTI-REPETITION below).

Agent 03 does NOT write final audience-facing copy.

Agent 03 sends its recommendation to Agent 01. **Agent 01 performs final concept/orchestration approval** — this is Agent 03's recommendation becoming Agent 01's decision, per the canonical Concept Selection Authority rule (`workflows/pipeline-control-rules.md` §3).

After Agent 01 approval, SELECTED_CONCEPT becomes locked. Any material concept change later in the run must return to Agent 01 — no other agent may make it unilaterally.

NEXT: Agent 04.

## STAGE 3 — AGENT 04: COPY & STORYTELLING

Agent 04 receives the Agent-01-approved strategy.

Agent 04 produces only the copy fields required for the selected format (hook, audience-facing copy/caption, CTA, voiceover, subtitles, on-screen text, slide/carousel copy, Story-frame copy — see the COPY PACKAGE output in `agents/04-copywriter-storytelling/README.md`).

Audience-facing content: natural American English (`shared/brand/language-policy.md`).

Agent 04 must NOT independently change the core concept, objective, audience, or strategic angle.

If the strategy is unusable: `STRATEGY_CLARIFICATION_REQUIRED` → Agent 01 (never resolved by contacting Agent 03 directly).

After copy is ready, Agent 03's Content Strategy Brief and Agent 04's Copy Package together form the canonical Handoff-to-Agent-05 Contract (`workflows/pipeline-control-rules.md` §6).

NEXT: Agent 05.

## STAGE 4 — AGENT 05: VISUAL PRODUCTION

Agent 05 receives the canonical Handoff-to-Agent-05 package. If it is incomplete or contradictory, Agent 05 returns `VISUAL_INPUT_INCOMPLETE` → Agent 01, and does not guess.

Agent 05 owns visual direction, composition, scenes, hierarchy, visual continuity, and the production specification (`agents/05-visual-creative-director/README.md`).

**Branch by format:**

**A. Static content** (single image / carousel / Stories) — Agent 05 is the static production owner. It produces the VISUAL_PRODUCTION_BRIEF and, when an authorized execution capability is available, the FINAL_VISUAL_ASSET. If no execution capability is available for the run, Agent 05 still delivers the brief and reports its PRODUCTION_STATUS to Agent 01 rather than fabricating an asset. Agent 06 is NOT involved.

When ready: `STATIC_READY_FOR_QC` (i.e. Agent 05's PRODUCTION_STATUS indicates the FINAL_VISUAL_ASSET is complete) → Agent 07.

**B. Video / Reel** — Agent 05 produces the VIDEO_VISUAL_BRIEF only; it does not execute video itself. → Agent 06.

## STAGE 5 — AGENT 06: VIDEO EXECUTION

Agent 06 executes the approved video production brief, using an authorized video-production tool (e.g. Kling) when available during real execution (`agents/06-reels-video-producer/README.md`).

SUCCESS: `VIDEO_READY_FOR_QC` → Agent 07.

Agent 06 does NOT publish and does NOT independently change the strategy.

### Video failure / Kling fallback

If the required video-production tool lacks credits/balance, has exhausted quota, is unavailable, fails access, or otherwise cannot execute the approved production:

Agent 06 sets `VIDEO_PRODUCTION_BLOCKED = TRUE`, `BLOCK_REASON = <exact known reason>`, and reports **ONLY to Agent 01** — it must not independently contact Agent 05 to redesign the content.

Agent 01 preserves the same approved core concept, campaign objective, audience insight, core product truth, and central message, and routes the concept to Agent 05 for the strongest feasible fallback (carousel, single-image post, or Story package). Agent 04 may adapt copy only as required by the new format. Full canonical routing: `workflows/pipeline-control-rules.md` §4.

Then: Agent 05 produces the static asset → Agent 07 QC.

Do NOT generate an unrelated backup concept merely because video production failed.

## STAGE 6 — AGENT 07: QUALITY CONTROL

Every finished package MUST pass Agent 07. Agent 07 reviews; it does NOT generate assets (`agents/07-quality-control-brand-guardian/README.md`).

Checks strategy alignment, brand, product truth, factual accuracy, copy, visual quality, video quality, copyright/IP, privacy, child safety, platform suitability, originality, anti-repetition, and commercial quality.

Possible decisions: `QC_APPROVED`, `QC_REVISION_REQUIRED`, `QC_INPUT_INCOMPLETE`, `QC_BLOCKED`.

**QC_APPROVED** — package returns to Agent 01, which sets `AWAITING_OWNER_APPROVAL` and presents exactly ONE finished content package to Daryna. No publication occurs yet.

**QC_REVISION_REQUIRED** — Agent 07 identifies PROBLEM, SEVERITY, RESPONSIBLE_AGENT, REQUIRED_CHANGE, REVISION_COUNT, and routes the correction to the responsible specialist. After correction, the package returns to Agent 07. Canonical revision-cycle rule (`workflows/pipeline-control-rules.md` §1): maximum 3 QC revision cycles for the same blocking defect. If REVISION_COUNT reaches 3 and the same defect remains, `ESCALATION_REQUIRED` → Agent 01, which decides whether to revise strategy, replace the asset, replace the concept, or ask Daryna. No infinite revision loops.

**QC_INPUT_INCOMPLETE / QC_BLOCKED** — structured BLOCK_REASON returned to Agent 01, which determines recovery. No agent invents missing evidence. Canonical definitions: `workflows/pipeline-control-rules.md` §2.

## STAGE 7 — OWNER APPROVAL

DEFAULT: REVIEW_MODE.

After QC_APPROVED, Agent 01 presents the completed package to Daryna. The presentation itself (framing, summary, questions) is in Russian; the final audience-facing copy and visual/video asset inside the package remain in their produced American English — they are not translated for review.

The review package should clearly show: selected concept, platform, format, primary objective, final visual/video asset, final audience-facing copy, CTA, recommended publishing date/time, evidence summary, QC status, and relevant limitations.

Status: `AWAITING_OWNER_APPROVAL`.

If Daryna requests changes, Agent 01 routes the requested revision to the appropriate specialist.

If Daryna approves the specific package: `OWNER_APPROVAL_STATUS = APPROVED_FOR_PUBLISHING`.

Only Agent 01 may set this status, and only after explicit package-specific owner approval. Approval for one package does NOT authorize future packages.

## STAGE 8 — AGENT 08: PUBLISHING

Agent 08 may publish ONLY when `QC_DECISION = QC_APPROVED` AND `OWNER_APPROVAL_STATUS = APPROVED_FOR_PUBLISHING`. If either is absent: `DO_NOT_PUBLISH` (`agents/08-publisher-performance-analyst/README.md`).

Agent 08 verifies platform, format, asset, copy, CTA, schedule date/time, and timezone. Default operational timezone: America/Los_Angeles.

Publishing success must be confirmed by the actual connected tool/platform. Never fabricate success.

On success: `PUBLISHING_STATUS = PUBLISHED`, and publication evidence is recorded.

### Scheduling logic

Agent 08 owns analytics-backed publishing-time recommendations when sufficient performance evidence exists. Agent 03 may suggest an initial PLANNING_WINDOW. Agent 01 resolves the final scheduling recommendation and records APPROVED_SCHEDULE. If sufficient analytics do not exist, label the recommendation `TEST_SCHEDULE` rather than presenting it as analytics-backed. Full canonical rule: `shared/platform-rules/platform-and-publishing-policy.md`.

## STAGE 9 — PERFORMANCE FEEDBACK

After publication, Agent 08 evaluates available performance data, separating FACT / OBSERVED_PATTERN / INFERENCE / RECOMMENDATION.

Performance feedback must answer: WHAT_WORKED, WHAT_UNDERPERFORMED, LIKELY_CAUSES, WHAT_TO_TEST_NEXT, WHAT_NOT_TO_REPEAT.

Agent 08 returns learning to Agent 01, Agent 02, and Agent 03, and — when relevant — Agent 04, Agent 05, Agent 06.

Agent 08 provides evidence. Agent 08 does NOT take over future strategy.

## ANTI-REPETITION

Uses the canonical taxonomy already defined in `workflows/pipeline-control-rules.md` §5: `NEW` / `ACCEPTABLE_ITERATION` / `TOO_REPETITIVE`, evaluated across topic, concept, hook, angle, format, visual concept, CTA, copy pattern, and story structure where relevant.

Responsibilities in this workflow: Agent 02 supplies evidence/context; Agent 03 performs the strategic repetition check during Stage 2; Agent 07 performs the final pre-approval repetition QC during Stage 6.

## BLOCK STATE CONTROL

Uses the canonical definitions in `workflows/pipeline-control-rules.md` §2:

- **QC_BLOCKED** — QC cannot complete due to missing/unverifiable required input.
- **PRODUCTION_BLOCKED** — production cannot continue because a required production dependency is unavailable.

Any agent detecting a material block reports RUN_ID, BLOCK_TYPE, BLOCK_REASON, RESPONSIBLE_STAGE, and RECOVERY_OPTIONS to Agent 01. Agent 01 controls recovery — no agent resolves its own block by inventing missing information.

## DAILY RUN FINAL STATES

Uses only the canonical final states already defined in `agents/01-content-director/README.md`:

RESEARCHING
PLANNING
PRODUCING
QC_REVIEW
REVISION_REQUIRED
ESCALATION_REQUIRED
AWAITING_OWNER_APPROVAL
APPROVED_FOR_PUBLISHING
PUBLISHED
PRODUCTION_BLOCKED

Expected normal REVIEW_MODE endpoint before owner decision: `AWAITING_OWNER_APPROVAL`.

Expected post-approval endpoint when publication succeeds: `PUBLISHED`.

## OUTPUT STORAGE

Use the existing `outputs/` structure logically:

- `outputs/drafts/` — work still being produced (pre-QC).
- `outputs/approved/` — QC-approved, owner-approved packages, when applicable.
- `outputs/published/` — records/assets associated with confirmed publications.
- `outputs/reports/` — research, QC, and performance reports, where appropriate.

Do NOT place private customer data into public repository content.

## MANDATORY SAFETY RULES

- REVIEW_MODE is default.
- Never publish without package-specific Daryna approval.
- Never bypass Agent 07.
- Never fabricate research.
- Never fabricate analytics.
- Never fabricate tool success.
- Never fabricate product truth.
- Etsy is a storefront/sales destination, NOT a social content platform.
- Maintain child safety.
- Maintain privacy.
- Maintain copyright/IP safety.
- Agent roles stay separate.
- Exactly 8 agents exist. This workflow is NOT Agent 09.
