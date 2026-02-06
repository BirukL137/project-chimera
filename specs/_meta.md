# Project Chimera — Master Meta Specification

> This document defines the **intent, boundaries, and hard constraints** for Project Chimera.
> It is **spec-only** and intentionally avoids implementation details.  
> (Assumption: Detailed functional and technical specs will live in separate files and reference this document.)

---

## 1. Vision

Chimera is an **Autonomous Influencer System** composed of **sovereign, persona-bound agents** that can operate at internet scale while remaining **governable, auditable, and safe**.

A small human team should be able to:

- Orchestrate **large fleets of agents** across platforms.
- Delegate complex, long-running objectives to agents.
- Rely on **formal governance and explicit constraints**, not manual babysitting.

(Assumption: “Influencer” includes any outward-facing persona producing or curating public content, not only commercial brand influencers.)

---

## 2. Non-Goals

Chimera is **not** intended to provide:

- **Real-time human chat or companionship** as a primary product surface.
- **Unconstrained autonomous finance**; all meaningful financial actions remain gated by explicit governance.
- **Direct platform automation for arbitrary tasks** outside the influencer / content domain.
- **A general-purpose agent runtime** for any arbitrary user-defined behavior.
- **Low-level infrastructure decisions** (e.g., database engine, CI/CD stack) within this document.

(Assumption: The product is focused on autonomous influencer behavior and campaign-like workflows, not on being a generic “do anything” agent platform.)

---

## 3. Core Constraints

These are **non-negotiable** and apply to all future specifications and implementations.

### 3.1 Spec-First, Architecture-Driven

- No production implementation may proceed **without ratified specifications** for the relevant scope.
- Specifications (SRS, persona SOUL documents, governance rules) are treated as **first-class system inputs**.
- Architecture is derived from **system intent and constraints**, not from implementation convenience.

(Assumption: A lightweight spec ratification process exists, even if informal at first, and is required before any production code is merged.)

### 3.2 Agent-Centric, Hub-and-Spoke Orchestration

- The system is modeled as a **distributed ecosystem of agents**, not a single monolithic app.
- A **central orchestrator (Hub)** is responsible for global strategy, resource allocation, and policy enforcement.
- **Manager / Planner / Worker / Judge** roles form the **spokes**, executing and evaluating work under orchestrator constraints.

(Assumption: This high-level orchestration pattern is stable, even if specific agent roles evolve.)

### 3.3 MCP-Only External Interactions

- **All interactions with external systems** (APIs, data stores, platforms) **MUST** flow through **Model Context Protocol (MCP)** servers.
- Runtime agents **MUST NOT** call external APIs or infrastructure directly.
- Skills are the **only** agent-facing abstraction that may internally use MCP.

(Assumption: Any exceptions—for example, logging infrastructure—must still preserve the same observability and governance guarantees as MCP.)

### 3.4 Skills: Stateless, Deterministic Capability Layer

- Skills represent **what an agent can do**, not how it reasons.
- Skills are **stateless between invocations**: no hidden cross-call memory.
- Skills are **deterministic** with respect to their declared inputs: same input → same output (or explicit, structured failure).
- All skill inputs and outputs must conform to **contract-first schemas**.

(Assumption: When skills depend on time-varying or external data, that variability is made explicit in the input/contract, to preserve auditability and replay.)

### 3.5 Strict Agent Isolation

- Each agent’s **memory**, **goals**, and **financial state** are logically isolated from other agents.
- Cross-agent coordination must occur through **explicit, governed channels** (e.g., orchestrator-managed workflows), not ad hoc shared state.

(Assumption: Isolation is logical rather than necessarily physical; multiple agents may co-reside in the same process or database while respecting these boundaries.)

---

## 4. Governance Principles

### 4.1 Rules and Personas as Data

- Governance rules, persona definitions (SOUL), budgets, and safety policies are treated as **data**, not hard-coded logic.
- Changes to governance data must be:
  - **Controlled** (only authorized human actors may approve),
  - **Audited** (who changed what, when, and why),
  - **Versioned** (allowing rollbacks and historical inspection).

(Assumption: The governance store is considered part of the trusted control plane and is not writable by runtime agents.)

### 4.2 Human-in-the-Loop as Guardrail, Not Crutch

- Humans are involved when:
  - Confidence or safety thresholds are breached,
  - Content is sensitive, regulated, or high-impact,
  - Financial or reputational risk exceeds predefined limits.
- When HITL is triggered for a high-risk action, the **default posture is to block** until a human or designated Judge agent explicitly approves, modifies, or rejects the action.

(Assumption: For low-risk actions, policies may allow fully autonomous behavior, but this autonomy is always traceable back to explicit governance settings.)

### 4.3 Default Fail-Closed Posture

- On uncertainty (policy ambiguity, tool failure, incomplete context), the system should **fail closed**, not silently proceed.
- Escalation to Judge and/or human review is preferred over implicit “best-effort” behavior for safety-critical decisions.

(Assumption: “Fail-closed” may still allow read-only exploration or simulation, but not side-effecting actions.)

### 4.4 Transparency and Auditability

- Every materially impactful action (e.g., publishing content, spending funds, changing long-term memory or personas) should be:
  - **Attributable** to a specific agent, governance policy, and triggering context.
  - **Reconstructable** from logs and specifications (within reasonable limits).
- Observability is a **core requirement**, not an afterthought.

---

## 5. Explicit Prohibitions

This section lists behaviors that are **architecturally disallowed**, regardless of implementation details.

1. **Direct external access by agents**
   - Agents may **not**:
     - Call external APIs, databases, or platforms directly.
     - Bypass MCP or skills to reach infrastructure.

2. **Hidden persistent state in skills**
   - Skills may **not**:
     - Maintain undocumented cross-call state via globals, caches, or side-effecting writes.
     - Persist data outside of what is declared in their contracts and governed data models.

3. **Undocumented non-determinism**
   - Skills and governance components may **not**:
     - Use unlogged randomness or time-based behavior that changes outputs for the same declared inputs without making those factors explicit.
     - Depend on external mutable state in ways that break the “same input → same output (or explicit failure)” expectation.

4. **Self-modifying governance by agents**
   - Runtime agents may **not**:
     - Directly alter governance rules, budgets, or persona DNA.
     - Grant themselves new capabilities, skills, or MCP access outside a controlled human-governed process.

5. **Unbounded autonomous financial actions**
   - Agents and skills may **not**:
     - Execute financial transfers or commitments that exceed configured policy limits.
     - Bypass Judge/human approval for transactions above defined thresholds.

(Assumption: “Financial” includes direct money movement and any commitments that can generate real-world financial liability, such as paid campaigns or ad spend.)

6. **Opaque cross-agent coupling**
   - Agents may **not**:
     - Share mutable internal state directly.
     - Coordinate via channels that are not observable and governed by the orchestrator or governance layer.

---

## 6. Relationship to Other Specs

- **Functional specifications** define *what* Chimera must do for users and stakeholders while respecting all constraints in this document.
- **Technical specifications** define *how* APIs, schemas, and protocols behave, as long as they do not violate these meta-level constraints.
- This meta specification is **authoritative**: in case of conflict, other specs must be updated to comply with it.

(Assumption: The spec set is living; this file is updated via the same governed process as other critical artifacts, but with extra scrutiny due to its cross-cutting impact.)