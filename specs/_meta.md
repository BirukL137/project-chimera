# Project Chimera — Master Meta Specification

## Purpose
Project Chimera is an autonomous influencer system designed to operate as a governed, scalable agentic infrastructure.
Its purpose is to enable persistent AI agents to research trends, generate content, and manage engagement while remaining safe, auditable, and spec-driven.

## Core Principles
- Spec-Driven Development (SDD)
- Explicit intent over implicit behavior
- Governance before autonomy
- Human-in-the-loop for safety and finance

## Authority & Decision Boundaries

Project Chimera enforces strict authority separation:

- **Human Operator**
  - Final authority over: deployment, spending, persona changes, and external publication.
  - May veto or halt any agent action at any stage.

- **Orchestrator Agent**
  - Coordinates task flow only.
  - Cannot finalize actions, spend funds, or invoke external tools directly.

- **Planner / Worker Agents**
  - Generate plans and proposals only.
  - All outputs are advisory and non-executable.

- **Judge / Evaluator Agents**
  - Provide scoring, risk flags, and recommendations.
  - Cannot approve execution.

- **Execution Boundary**
  - Any action that is external, irreversible, or financial requires explicit Human Operator approval.


## Non-Goals
- Real-time conversational chatbots
- Direct API calls that bypass MCP
- Fully autonomous financial decisions without approval

## Hard Constraints
- All external interactions MUST occur via MCP servers
- No implementation code may be written without a ratified specification
- Skills must be stateless, deterministic, and side-effect bounded
- Runtime agents may not access developer MCP tools

## Governance & Safety
Human-in-the-loop (HITL) review is mandatory for:
- Financial transactions
- Ambiguous or low-confidence content
- Policy or persona boundary violations

## Specification Authority Order
1. specs/_meta.md (highest authority)
2. specs/functional.md
3. specs/technical.md
4. research documents and README files (non-authoritative)

## Financial Authority & Wallet Safety

- Agents may propose financial actions but cannot execute them.
- All spending requires:
  1. Human Operator approval
  2. Explicit confirmation of amount, purpose, and destination
- Wallet credentials are never accessible to agents.
- MCP mediates all financial interactions with enforced spending limits.

## Memory & Persona Governance (Initial Guardrails)

- Long-term memory, persona DNA, and governance configuration:
  - Are read-only to agents by default
  - May only be modified by the Human Operator
- All changes must be logged and auditable.
- Detailed mutation policies are deferred to a later phase.

## Deferred Governance Enhancements

- Skill determinism guarantees and replayability constraints
- Runtime-level enforcement of governance beyond specification

These are acknowledged and intentionally deferred until post-MVP stabilization.
