# Tooling Strategy — Project Chimera

## Purpose

This document defines the **developer-facing tooling layer** used during Chimera’s design and implementation.

These tools are **not accessible to runtime agents** and exist solely to:
- Improve developer productivity
- Enforce spec-first workflows
- Maintain auditability and safety boundaries

---

## Authority Boundary (Developer Tools vs Runtime Capabilities)

- **Developer MCP tools** exist to help humans (and IDE assistants) author, review, and maintain the repository artifacts (specs, docs, source).
- **Runtime agents** never receive developer tool access. Runtime agents operate only through **governed Skills** with explicit contracts.
- **MCP in this document** refers only to developer-facing servers. It is intentionally separate from any runtime tool surface.

---

## MCP Servers (Developer-Only)

### filesystem-mcp
**Purpose:**  
- Read/write project files
- Generate and refine specifications inside the IDE

**Access Scope:**  
- Developer (human + IDE agent)
- No runtime agent access

---

### git-mcp
**Purpose:**  
- Commit, diff, and review changes
- Maintain traceability between specs and implementation

**Access Scope:**  
- Developer only
- Used to demonstrate structured workflows during the challenge

---

## Explicit Non-Goals

- Runtime agents do **not** access developer MCP servers
- MCP servers do **not** grant execution authority to agents
- This document does not define production deployment tooling

---

## Rationale

Separating developer MCP tooling from runtime agent skills ensures:
- Clear authority boundaries
- No accidental privilege escalation
- Auditable human-in-the-loop workflows
