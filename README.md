# LiorTales-Ai-Studio

This repository is the LiorTales multi-agent content production system. It coordinates a set of specialized agents — from trend research and strategy through copywriting, visuals, video, quality control, and publishing/analytics — to plan, produce, and review content for LiorTales.

## Repository Structure

- `/agents` — one folder per specialized agent (content direction, research, strategy, copywriting, visuals, video, QC/brand guardian, publishing/analytics), each with a README describing its role.
- `/shared` — shared reference material used across agents: brand guidelines, product info, platform rules, research, analytics, and cross-cutting production-tool contracts (`/shared/production-tools`).
- `/workflows` — process definitions for how agents work together (daily content, manual content, performance feedback) and the canonical cross-agent control mechanics (`pipeline-control-rules.md`).
- `/outputs` — content artifacts moving through the pipeline: drafts, approved, published, and reports.
- `/tools` — executable production tooling invoked by agents during content generation. Currently: the OpenAI scene-generation + deterministic cover-compositing pipeline used by Agents 05 and 06 (`tools/openai-image-pipeline/`).
- `/product-assets` — versioned, committed LiorTales product IP required by production tooling. Currently: the approved master book cover files (`product-assets/approved-master-covers/`), hash-pinned via `tools/openai-image-pipeline/covers_registry.json`. Not secrets — committed deliberately so any container that clones this repo has what the pipeline needs.

The 8 agent roles and shared brand/product/workflow rules are fully specified. `/tools` holds the first piece of executable application code in this repo; further integrations will be added separately.
