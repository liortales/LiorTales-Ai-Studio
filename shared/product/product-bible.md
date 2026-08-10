# LIORTALES PRODUCT BIBLE

Canonical source of truth for what any agent is allowed to say about the LiorTales product. Every audience-facing product claim must trace back to this document. Where a fact is not yet confirmed, it is marked `STATUS: TBD` and `PUBLIC CLAIM: PROHIBITED UNTIL CONFIRMED` — no agent may invent, infer, or approximate it.

## 1. PRODUCT DEFINITION

Confirmed: LiorTales creates personalized children's books / personalized story experiences centered on the child.

No further technical or structural detail about the product is confirmed beyond what appears in this document. Do not add unsupported technical details (e.g. specific personalization mechanism, production process, or technology used) beyond what is stated here.

## 2. CORE PRODUCT VALUE

Safe framing: personalization makes the story feel personally relevant to the recipient.

STATUS: TBD — do not claim proven developmental, educational, psychological, or behavioral outcomes. No such claim is confirmed or permitted until explicitly established and approved.

## 3. PERSONALIZATION

CONFIRMED: personalization is a core part of the LiorTales product.

Any specific personalization field or option (e.g. name, appearance, characters, setting, language, dedication, number of fields):

STATUS: TBD
PUBLIC CLAIM: PROHIBITED UNTIL CONFIRMED

Marketing may reference "personalized" and "built around your child" in general terms; it may not describe specific personalization mechanics until they are confirmed here.

## 4. PRODUCT EXPERIENCE

Allowed general marketing territory: child-centered story, personalized gift, reading experience, meaningful keepsake, family gifting moment.

Do not promise a particular emotional reaction (e.g. "will make them cry," "guaranteed to delight") — describe the intended experience, not a guaranteed outcome.

## 5. PRODUCT FORMATS

| Attribute | Status | Public Claim |
|---|---|---|
| Page count | TBD | Prohibited until confirmed |
| Trim size | TBD | Prohibited until confirmed |
| Binding | TBD | Prohibited until confirmed |
| Paper stock | TBD | Prohibited until confirmed |
| Cover finish | TBD | Prohibited until confirmed |
| Print provider | TBD | Prohibited until confirmed |
| Language availability | TBD | Prohibited until confirmed |

This table is the single update point for product-format facts. When Daryna confirms any row, update it here first (see §17 CHANGE CONTROL); downstream agents then inherit the change without this document needing to be rewritten.

## 6. SALES CHANNEL

Confirmed: Etsy is the primary sales destination currently used by LiorTales.

Etsy is a storefront/sales destination — it is NOT a social content platform. Canonical classification: `shared/platform-rules/platform-and-publishing-policy.md`.

## 7. PRICING

STATUS: TBD
PUBLIC CLAIM: PROHIBITED UNTIL CONFIRMED

## 8. DISCOUNTS / PROMOTIONS

STATUS: TBD

Never fabricate urgency, discounts, coupons, scarcity, or expiration dates in any content.

## 9. PRODUCTION TIME

STATUS: TBD

No public production-time promise until confirmed here.

## 10. SHIPPING / DELIVERY

STATUS: TBD

No delivery guarantee or shipping-speed claim until confirmed here.

## 11. RETURNS / CANCELLATIONS

STATUS: TBD

Do not state a returns/cancellation policy until confirmed here.

## 12. PRINT / MATERIAL QUALITY

STATUS: TBD unless explicitly verified.

Marketing may visually present the product as premium according to brand direction (`shared/brand/visual-identity-guide.md`), but copy must not make unsupported technical quality claims (e.g. specific paper weight, "museum-quality," "archival").

## 13. REVIEWS / CUSTOMER DATA

Never fabricate ratings, buyer counts, reviews, testimonials, customer identities, customer photos, or purchase results.

STATUS: TBD
PUBLIC CLAIM: PROHIBITED UNTIL CONFIRMED

## 14. ALLOWED CLAIM TYPES

Examples of currently supportable claims:

- "a personalized story created around your child"
- "a meaningful personalized gift"
- "a story where your child is at the heart of the adventure"

Only claims of this kind — general, personalization-centered, non-quantitative, non-guaranteeing — are currently supportable. Do not extend these examples into specific, quantitative, or comparative claims without updating this document first.

## 15. PROHIBITED CLAIM TYPES

- Guarantees of any kind (satisfaction, delivery, emotional outcome).
- Unsupported superlatives ("the best," "#1," "life-changing").
- Developmental, educational, medical, or psychological claims.
- Fake or unverified social proof (reviews, ratings, testimonials, buyer counts).
- Fake urgency or scarcity (countdowns, "selling out," fake limited stock).
- Unverified shipping, production-time, pricing, or discount claims.

## 16. PRODUCT_FACT_REQUIRED

Canonical rule: if an agent needs a product fact that is not present in this document, it must not guess or infer it.

Return:

PRODUCT_FACT_REQUIRED
→ Agent 01
→ request clarification from Daryna.

The agent must not guess. This aligns with the existing `PRODUCT_FACT_REQUIRED` (Agent 04), `PRODUCT_VISUAL_FACT_REQUIRED` (Agent 05), and `PRODUCT_FACT_CHECK_REQUIRED` (Agent 07) triggers already defined in the agent specifications, and with the block-routing rule in `workflows/pipeline-control-rules.md` §2.

## 17. CHANGE CONTROL

Whenever Daryna confirms a new permanent product fact, this Product Bible must be updated first — specifically the relevant section/row above (e.g. §5 Product Formats, §7 Pricing). Downstream agents then inherit the new truth from this single document; no agent-level file should hold its own copy of a product fact.

## 18. CONFIRMED EXISTING TITLES (APPROVED MASTER COVERS)

CONFIRMED: the following titles are real, existing LiorTales books with locked cover artwork. Each cover is a complete, immutable image — the canonical source of truth for what appears on that book. Do not redraw, regenerate, approximate, or substitute any of these.

Source location: Canva folder `LiorTales - Approved Book Assets` → `00_APPROVED_MASTER_COVERS_DO_NOT_MODIFY`.

| # | Title | Canva Asset ID |
|---|---|---|
| 01 | Mia and the Missing Star | `MAHR7spCO30` |
| 02 | Adam, Lev & Olivia: Monsters from the Stars | `MAHR7hILHjs` |
| 03 | Rostislav: The Glitch in the Green Forest | `MAHR7hdvibw` |
| 04 | Olivia and the Enchanted Bunny | `MAHR7kjIXWA` |

This registry does not confirm the physical specifications in §5 (page count, trim size, binding, etc.) — those remain `STATUS: TBD` independently of cover-artwork confirmation. Title/cover existence and physical print specs are separate facts; do not infer one from the other.

Canonical asset-lock rule governing use of these covers in marketing content: `workflows/pipeline-control-rules.md` §9. QC verification: the Product Asset Identity QC area in `agents/07-quality-control-brand-guardian/README.md`.

Whenever a new approved master cover is added, update this registry first (see §17 CHANGE CONTROL); downstream agents then inherit the new title without this document needing to be rewritten elsewhere.
