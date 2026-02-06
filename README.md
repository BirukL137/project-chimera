# Project Chimera

Spec-driven, governable agentic infrastructure for autonomous influencer systems.

## Project Status

🚧 **Architecture & Governance Phase**

This repository currently contains:
- Ratified architectural intent
- Executable specifications
- Governance and review policies
- Failing tests that define future behavior

No production agent logic has been implemented yet by design.

## Core Philosophy

Chimera is built under the following non-negotiable principles:

- **Spec-Driven Development (SDD)**  
  Behavior is defined in specs before any implementation exists.

- **Fail-Closed Governance**  
  Ambiguity, tool failure, or policy uncertainty blocks execution.

- **MCP-Mediated Execution Only**  
  Agents never access external systems directly.

- **Human Authority is Explicit**  
  High-impact actions require Judge or human approval.

These constraints are defined in `specs/_meta.md` and apply to all future code.

## Repository Structure

```text
.
├── specs/                  # Authoritative system specifications
│   ├── _meta.md             # Vision, constraints, governance
│   ├── functional.md        # User- and agent-facing requirements
│   └── technical.md         # API contracts and schemas
│
├── skills/                 # Runtime capability definitions (no logic yet)
│   └── README.md            # Skill contracts and boundaries
│
├── tests/                  # Failing tests defining expected behavior
│
├── .github/workflows/       # CI pipeline (test-first, spec-aware)
│
├── .coderabbit.yaml         # AI review policy (simulated governance)
│
├── Dockerfile               # Reproducible execution environment
├── Makefile                 # Standardized developer commands
└── README.md                
```

## Development Workflow

1. Specifications are authored or updated in `specs/`
2. Tests are written to reflect the specifications (expected to fail)
3. CI enforces test execution and basic governance checks
4. Only after specs and tests are ratified does implementation begin

This workflow is intentionally designed to support:
- Agentic development
- AI-assisted coding
- Safe delegation of implementation to autonomous systems

## AI & Governance

- IDE agents (Cursor, Copilot, etc.) are expected to:
  - Read from `specs/` before generating code
  - Explain plans before writing implementation
- AI code review is simulated via `.coderabbit.yaml`
- Final authority always rests with human reviewers

## What Is Intentionally Out of Scope (For Now)

- Agent runtime implementation
- Platform-specific integrations
- Production deployment configuration
- Financial execution logic

These will be introduced only after specifications and governance are complete.
