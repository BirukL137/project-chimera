---
# `skill_download_video`

## Purpose

Provide a bounded capability to acquire a single video artifact for downstream processing (e.g., transcription), without granting runtime agents direct external access.

## Input contract (JSON)

```json
{
  "source": {
    "kind": "string",
    "reference": "string"
  },
  "constraints": {
    "max_bytes": "integer"
  }
}
```

Field notes:
- `source.kind`: logical identifier for the source type (e.g., "url", "platform_id"); not an API selection.
- `source.reference`: opaque identifier the system can resolve under governance.
- `constraints.max_bytes`: upper bound on artifact size.

## Output contract (JSON)

```json
{
  "artifact": {
    "artifact_id": "string",
    "media_type": "string",
    "bytes": "integer"
  }
}
```

## Explicit constraints

- **No hidden state**: the skill retains no memory between calls.
- **No agent-to-external access**: runtime agents never access external systems directly; any retrieval occurs only inside this skill via governed tool bridges.
- **Contract-first and bounded**: the skill returns exactly one acquired artifact reference or an explicit failure.
- **Deterministic contract**: given the same declared input, the skill returns the same structured output or an explicit failure.
