---
# `skill_transcribe_audio`

## Purpose

Provide a bounded capability to generate a structured transcript from an audio (or audio-bearing) artifact for use in governed reasoning and review.

## Input contract (JSON)

```json
{
  "artifact": {
    "artifact_id": "string",
    "language_hint": "string"
  },
  "output_preferences": {
    "include_timestamps": "boolean"
  }
}
```

Field notes:
- `artifact.artifact_id`: opaque reference to an existing audio-bearing artifact.
- `artifact.language_hint`: optional hint to constrain expected language (may be empty).
- `output_preferences.include_timestamps`: whether the transcript should include timing metadata.

## Output contract (JSON)

```json
{
  "transcript": {
    "text": "string",
    "language": "string"
  },
  "segments": [
    {
      "start_ms": "integer",
      "end_ms": "integer",
      "text": "string"
    }
  ]
}
```

## Explicit constraints

- **No hidden state**: the skill retains no memory between calls.
- **No agent-to-external access**: runtime agents never access external systems directly; any model/tool access occurs only inside this skill via governed tool bridges.
- **Contract-first**: output must conform to this schema; failures must be explicit.
- **Deterministic contract**: given the same declared input, the skill returns the same structured output or an explicit failure.
