# Project Chimera — Master Meta Specification

## Purpose
Project Chimera is an autonomous influencer system designed to operate as a governed, scalable agentic infrastructure.
Its purpose is to enable persistent AI agents to research trends, generate content, and manage engagement while remaining safe, auditable, and spec-driven.

## Core Principles
- Spec-Driven Development (SDD)
- Explicit intent over implicit behavior
- Governance before autonomy
- Human-in-the-loop for safety and finance

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
