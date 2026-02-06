---
# Chimera Runtime Skills

## What a Skill is

A **Skill** is a governed, agent-facing capability that performs a bounded action via a **contract-first JSON interface**.

Skills define **what an agent can do** (capabilities), not how it reasons.

## Why Skills exist

Skills exist as a controlled capability layer to:

- Keep **authority boundaries** explicit (agents cannot touch external systems directly)
- Improve **auditability** (structured inputs/outputs)
- Reduce **unsafe autonomy** by forcing actions through constrained contracts
- Improve **testability** by requiring deterministic behavior

## Core principles

- **Stateless**: no hidden memory across calls.
- **Deterministic**: same declared input → same output, or explicit failure.
- **Contract-first**: inputs/outputs must match the JSON schema defined in each skill README.
- **Orchestrator-governed**: skills are selected, permitted, and invoked under orchestrator policy; agents do not expand their own capabilities.
- **No direct external access by agents**: only skills may interface with external bridges (via MCP); runtime agents never call MCP directly.

## High-level lifecycle

1. **Request**: an agent requests a specific skill by name with structured JSON input.
2. **Validate**: the skill validates input against its contract (or fails explicitly).
3. **Execute**: the skill performs the bounded action (internally using governed tool bridges as needed).
4. **Return**: the skill returns structured JSON output for evaluation, logging, and next-step reasoning.

## Available skills

- `skill_fetch_trends/`
- `skill_download_video/`
- `skill_transcribe_audio/`
