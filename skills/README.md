# Chimera Agent Skills

## Overview
Skills are stateless, deterministic capability packages that runtime Chimera agents may invoke to perform specific actions.

A Skill represents **what an agent can do**, not how it reasons.

Skills are intentionally constrained to:
- Reduce hallucination
- Enforce governance
- Enable testability and auditing

## Design Principles
- **Stateless**: Skills do not retain memory between calls
- **Deterministic**: Same input → same output (or explicit failure)
- **Isolated**: No direct access to developer tools or internal state
- **Contract-First**: Inputs and outputs must match defined schemas

## Skill Lifecycle
1. Agent selects a Skill based on its goal
2. Agent provides structured input
3. Skill executes via MCP or internal logic
4. Output is returned for validation or further reasoning

## Skill Execution Model

- Skills are functionally stateless:
  - They do not retain memory between invocations.
  - They do not write to local or long-term storage.
- Any external side effects (API calls, file writes, blockchain interactions):
  - Must be explicitly declared in the skill interface.
  - Are executed only through MCP-managed tools.
- Skills may read inputs and return outputs only.
- Persistence, memory updates, and financial actions are handled outside skills by governed system components.

## Skill vs MCP
- **MCP Servers**: External bridges (APIs, databases, filesystems)
- **Skills**: Agent-facing capabilities that may internally use MCP

Runtime agents may never call MCP servers directly — only through Skills.

## Required Skill Structure
Each skill directory must contain:
- README.md (contract & intent)

## Available Skills (Draft)
- skill_fetch_trends
- skill_generate_content
- skill_publish_status
