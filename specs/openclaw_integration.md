```markdown
# Project Chimera — OpenClaw Integration Specification

> This document defines how Chimera publishes its **Availability** / **Status** to the **OpenClaw** network.
> It focuses on intent, data contracts, and orchestration flow, not concrete implementation details.  
> (Assumption: OpenClaw is an external coordination / discovery network where autonomous systems advertise presence and capabilities.)

---

## 1. Purpose

Chimera should expose a **controlled, governance-respecting status signal** to the OpenClaw network so that:

- External systems can discover whether Chimera is **online, healthy, and accepting work**.
- Chimera can participate in **coordinated campaigns or cross-system workflows** without exposing internal details or control surfaces.
- Status publication remains **spec-first, auditable, and reversible**.

(Assumption: OpenClaw does not require Chimera to accept arbitrary remote commands; the initial integration is **publish-only**.)

---

## 2. Scope and Non-Goals

### 2.1 In Scope

- Defining **status payloads** that Chimera publishes to OpenClaw.
- Defining **when** and **how** Chimera updates its status.
- Clarifying **which Chimera components** are allowed to influence status publication.
- Defining **governance and safety rules** around what can be shared.

### 2.2 Out of Scope

- Accepting **tasks, commands, or job assignments** directly from OpenClaw.
- Defining OpenClaw’s **internal protocol** or persistence model.
- Implementing cross-network **payment, reputation, or SLAs**.
- Exposing **per-agent or per-persona private data** beyond what is explicitly defined here.

(Assumption: Future phases may add richer interaction with OpenClaw, but this document covers **status broadcast only**.)

---

## 3. Conceptual Model

### 3.1 Chimera Presence in OpenClaw

Chimera appears to OpenClaw as a **single logical participant** (a “Chimera Node”) with:

- A unique **Node ID**.
- A set of **capabilities descriptors** (e.g., “autonomous influencer agents”, “content campaigns”).
- A current **Availability / Status** record.

(Assumption: If multiple Chimera deployments exist (e.g., staging, production), each has its own OpenClaw Node ID.)

### 3.2 Status vs Internal Health

- **Internal health**: Detailed per-agent metrics, incidents, and subsystem states (kept inside Chimera).
- **Published status**: A **redacted, aggregated view** suitable for external coordination (e.g., “accepting new campaigns”, “degraded”, “maintenance”).

Chimera must **never leak** sensitive internal information (e.g., specific incidents, PII, proprietary strategies) through OpenClaw status.

---

## 4. Status Data Model

> Status is expressed as a JSON payload published to OpenClaw via an MCP tool.  
> (Assumption: OpenClaw expects JSON documents keyed by a logical node identifier.)

### 4.1 Status Payload Schema (Conceptual)

```json
{
  "node_id": "chimera-prod-001",
  "version": "1.0.0",
  "timestamp": "2025-01-10T12:00:00Z",
  "lifecycle_state": "online",
  "availability": {
    "accepting_new_objectives": true,
    "max_concurrent_objectives": 50,
    "current_objectives": 37
  },
  "health": {
    "status": "degraded",
    "reason_codes": ["ELEVATED_INCIDENT_RATE"],
    "since": "2025-01-10T10:30:00Z"
  },
  "capabilities": {
    "influencer_domains": ["fitness", "lifestyle"],
    "supported_regions": ["US", "CA", "UK"],
    "content_surfaces": ["short_video", "image", "text_post"]
  },
  "governance": {
    "policy_version": 4,
    "requires_manual_approval_for_high_risk": true
  },
  "constraints": {
    "max_daily_spend_global": 5000.0,
    "status_visibility": "public"
  }
}
```

Field notes:

- `node_id`: Logical identifier configured at deployment time.
- `version`: High-level Chimera deployment version (for compatibility and debugging).
- `lifecycle_state`:
  - `online` | `degraded` | `maintenance` | `offline_soon` | `offline`.
- `availability`: High-level capacity and willingness to accept new work.
- `health`: Abstracted health indicators, no internal stack traces or private metrics.
- `capabilities`: Coarse-grained domain descriptors, not per-agent secrets.
- `governance`: Limited metadata indicating **governance posture**, not policies themselves.
- `constraints`: Boundaries relevant to coordination (e.g., global spend caps).

(Assumption: OpenClaw consumers do not require fine-grained metrics; they use this status to decide whether to route work toward or away from Chimera.)

---

## 5. Publishing Flow within Chimera

> Publication is **initiated and controlled by the Orchestrator**, implemented via a **dedicated Skill** that calls an OpenClaw MCP tool.

### 5.1 Components

- **Orchestrator**
  - Aggregates internal state (objectives, incidents, capacity).
  - Decides **what status to publish** and **when**.
- **Status Skill** (e.g., `skill_publish_openclaw_status`)
  - A stateless, deterministic Skill that accepts a **normalized status description** and pushes it to OpenClaw via MCP.
- **OpenClaw MCP Server**
  - Exposes an MCP tool (e.g., `openclaw.publish_status`) that writes the status to OpenClaw.

(Assumption: This status Skill is **read-only** from the perspective of internal Chimera state; it only reads Orchestrator-provided data and writes to OpenClaw.)

### 5.2 End-to-End Sequence

1. **Orchestrator computes status snapshot**
   - Periodically (e.g., every N minutes) or on significant events, the Orchestrator:
     - Summarizes current objectives, capacity, and internal incidents.
     - Maps those to `lifecycle_state`, `availability`, and `health` concepts.

2. **Orchestrator invokes Status Skill**
   - Orchestrator calls `skill_publish_openclaw_status` with a JSON payload:

   ```json
   {
     "node_id": "chimera-prod-001",
     "lifecycle_state": "online",
     "availability": {
       "accepting_new_objectives": true,
       "max_concurrent_objectives": 50,
       "current_objectives": 37
     },
     "health": {
       "status": "degraded",
       "reason_codes": ["ELEVATED_INCIDENT_RATE"]
     },
     "capabilities": {
       "influencer_domains": ["fitness", "lifestyle"],
       "supported_regions": ["US", "CA", "UK"],
       "content_surfaces": ["short_video", "image", "text_post"]
     },
     "governance": {
       "policy_version": 4,
       "requires_manual_approval_for_high_risk": true
     },
     "constraints": {
       "max_daily_spend_global": 5000.0,
       "status_visibility": "public"
     }
   }
   ```

3. **Status Skill calls OpenClaw via MCP**
   - Skill transforms this payload into an MCP tool request:

   ```json
   {
     "tool_name": "openclaw.publish_status",
     "arguments": {
       "node_id": "chimera-prod-001",
       "status_payload": { /* same as above */ }
     }
   }
   ```

4. **OpenClaw MCP Server publishes to network**
   - MCP server:
     - Authenticates as the Chimera Node.
     - Stores/broadcasts the status on OpenClaw.
     - Returns success/failure to the Skill.

5. **Skill returns result to Orchestrator**
   - Success: Orchestrator logs timestamp and payload used.
   - Failure: Orchestrator may:
     - Retry with backoff,
     - Mark OpenClaw integration as temporarily unavailable,
     - Optionally raise an internal, low-priority incident.

(Assumption: Agents themselves **never** invoke `skill_publish_openclaw_status`; only Orchestrator or governance components do.)

---

## 6. Triggers for Status Updates

Chimera publishes or updates its OpenClaw status under the following conditions:

1. **Periodic Heartbeat**
   - At a configurable interval (e.g., every 5–15 minutes).
   - Ensures OpenClaw has a relatively fresh view of Chimera’s availability.

2. **Lifecycle Transitions**
   - When moving between:
     - `online` ↔ `degraded`
     - `online` ↔ `maintenance`
     - `online` / `degraded` ↔ `offline_soon` / `offline`
   - Example triggers:
     - Planned maintenance windows.
     - Significant infrastructure issues.

3. **Governance or Policy Changes**
   - When global policies or major constraints change in ways that affect coordination:
     - New `max_daily_spend_global`.
     - Changes in supported regions or content surfaces.

4. **Incident Thresholds**
   - When incident rates or severities cross defined thresholds that materially change risk posture.
   - Example: “If severe incidents per hour exceed threshold T, set `health.status = "degraded"` and publish.”

(Assumption: Thresholds and intervals are defined in governance/configuration, not hard-coded.)

---

## 7. Governance and Safety Rules

### 7.1 Who Controls Status Publication

- Only **Orchestrator and governance services** may:
  - Decide when to publish.
  - Assemble the status payload.
- **Agents**:
  - Cannot directly publish or modify OpenClaw status.
  - May only indirectly influence aggregate metrics (e.g., by creating more objectives).

(Assumption: Any manual override (e.g., “force offline”) is done via governance tools that drive the Orchestrator, not by editing OpenClaw directly.)

### 7.2 Information Allowed vs Prohibited

- **Allowed**:
  - High-level lifecycle state and capacity.
  - Aggregate, non-sensitive capability descriptors.
  - Coarse-grained health states (healthy / degraded / maintenance).
  - Governance posture at a macro level (e.g., “requires_manual_approval_for_high_risk: true”).

- **Prohibited**:
  - Per-agent or per-user identifiable details.
  - Specific incident descriptions or stack traces.
  - Exact budget or revenue amounts tied to specific clients or campaigns.
  - Any policy rules that could be exploited to game the system.

(Assumption: If in doubt, fields are **redacted or omitted** rather than over-disclosed.)

### 7.3 Fail-Closed Behavior

- If OpenClaw MCP calls fail repeatedly:
  - Chimera should **not** escalate its external status to a misleading state (e.g., “offline”) unless it truly is.
  - Instead, it records an internal incident: “OpenClaw status publishing degraded.”
- If status computation is ambiguous (e.g., conflicting signals about health):
  - Chimera prefers a **more conservative state** (e.g., `degraded` instead of `online`) or **no change** until clarity is restored.

(Assumption: External status should err on the side of caution without destabilizing dependent systems unnecessarily.)

---

## 8. Observability and Audit

Chimera must be able to answer, after the fact:

- **What status** did we last publish to OpenClaw?
- **When** did we publish it?
- **Why** (which internal conditions / governance decisions led to that state)?

To support this:

- Every successful publish is logged as an internal **ACTION** (per ERD-style modeling) with:
  - `kind = "OPENCLAW_STATUS_PUBLISH"`
  - Input snapshot (status payload).
  - Result snapshot (OpenClaw MCP response).
- Governance tools can query the history of OpenClaw status publications to:
  - Validate that external claims matched internal conditions.
  - Diagnose misconfigurations or misaligned thresholds.

(Assumption: This reuse of the existing ACTION / INCIDENT model is sufficient and avoids introducing a parallel logging subsystem.)

---

## 9. Future Extensions (Non-Binding)

> The following are explicitly non-binding ideas for later versions and **do not** affect current commitments.

- Allow Chimera to subscribe to **OpenClaw-wide signals** (e.g., “network-wide maintenance”).
- Integrate **reputation or reliability scores** derived from OpenClaw into governance decisions.
- Coordinate **multi-system campaigns** where OpenClaw orchestrates workflows across multiple autonomous participants.

(Assumption: Any evolution beyond publish-only would require a new spec and governance review.)
```