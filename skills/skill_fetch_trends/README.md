---
# `skill_fetch_trends`

## Purpose

Provide a bounded, read-only way for runtime agents to request a structured snapshot of current trends relevant to a platform and region.

## Input contract (JSON)

```json
{
  "platform": "string",
  "region": "string",
  "limit": "integer",
  "topic_hints": ["string"]
}
```

Field notes:
- `platform`: logical platform identifier (not a direct API endpoint).
- `region`: logical region identifier.
- `limit`: maximum number of trend items requested.
- `topic_hints`: optional strings to narrow relevance.

## Output contract (JSON)

```json
{
  "trends": [
    {
      "topic": "string",
      "score": "number",
      "timestamp": "ISO-8601"
    }
  ],
  "source": {
    "platform": "string",
    "region": "string"
  }
}
```

## Explicit constraints

- **No hidden state**: the skill retains no memory between calls.
- **No agent-to-external access**: runtime agents never access external systems directly; any external interaction occurs only inside this skill via governed tool bridges.
- **Deterministic contract**: given the same declared input, the skill returns the same structured output or an explicit failure.
