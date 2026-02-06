import pytest

# NOTE: These imports intentionally reference not-yet-implemented contract validators.
# Under TDD, tests should fail initially (ImportError / AttributeError) until the
# implementation is created in a spec-compliant way.
# Spec reference: specs/technical.md §2.1 (generic skill envelope) and §5 (boundaries).
from chimera.contracts.skills import (  # type: ignore[import-not-found]
    validate_skill_invocation_request,
    validate_skill_response,
)


def test_skill_invocation_request_minimal_valid_envelope():
    """
    A skill invocation request MUST include:
    - invocation_id (string)
    - agent_id (string)
    - skill_name (string)
    - intent (string)
    - input (object)
    - context.persona_id, context.objective_id, context.risk_profile, context.trace_id

    Spec: specs/technical.md §2.1 Agent → Skill Request.
    """
    request = {
        "invocation_id": "invocation-uuid",
        "agent_id": "agent-uuid",
        "skill_name": "skill_fetch_trends",
        "intent": "understand_current_trends_for_persona_context",
        "input": {"platform": "tiktok", "region": "US"},
        "context": {
            "persona_id": "persona-uuid",
            "objective_id": "objective-uuid",
            "risk_profile": "standard",
            "trace_id": "trace-uuid",
        },
    }

    validate_skill_invocation_request(request)


def test_skill_invocation_request_rejects_missing_required_fields():
    """
    A skill invocation request MUST be rejected when required fields are missing,
    e.g.:
    - no invocation_id
    - no context or missing persona_id / objective_id / risk_profile / trace_id

    Spec: specs/technical.md §2.1.
    """
    bad_request = {
        # "invocation_id" missing
        "agent_id": "agent-uuid",
        "skill_name": "skill_fetch_trends",
        "intent": "understand_current_trends_for_persona_context",
        "input": {"platform": "tiktok", "region": "US"},
        "context": {
            "persona_id": "persona-uuid",
            "objective_id": "objective-uuid",
            "risk_profile": "standard",
            "trace_id": "trace-uuid",
        },
    }

    with pytest.raises(ValueError):
        validate_skill_invocation_request(bad_request)


def test_skill_invocation_request_rejects_undeclared_top_level_parameters():
    """
    Skills MUST expose explicit, schema-defined inputs and outputs.
    Top-level parameters outside the defined envelope should be rejected,
    to avoid arbitrary, undeclared control or data channels.

    Spec: specs/technical.md §2.1 and §5.1/§5.2 (contract-first, no hidden channels).
    Ambiguity: The spec does not forbid additional optional fields explicitly; this
    test treats extra top-level fields as a schema violation to keep boundaries tight.
    """
    bad_request = {
        "invocation_id": "invocation-uuid",
        "agent_id": "agent-uuid",
        "skill_name": "skill_fetch_trends",
        "intent": "understand_current_trends_for_persona_context",
        "input": {"platform": "tiktok", "region": "US"},
        "context": {
            "persona_id": "persona-uuid",
            "objective_id": "objective-uuid",
            "risk_profile": "standard",
            "trace_id": "trace-uuid",
        },
        "extra": "should-not-be-here",  # undeclared parameter
    }

    with pytest.raises(ValueError):
        validate_skill_invocation_request(bad_request)


def test_skill_response_success_shape():
    """
    A successful skill response MUST:
    - Have status == "success"
    - Include output (object) with structured result
    - Include meta.duration_ms (number) and meta.trace_id (string)

    Spec: specs/technical.md §2.1 Skill → Agent Response.
    """
    response = {
        "invocation_id": "invocation-uuid",
        "skill_name": "skill_fetch_trends",
        "status": "success",
        "output": {
            "trends": [],
            "source": {"platform": "tiktok", "region": "US", "retrieved_at": "2025-01-10T12:00:00Z"},
        },
        "meta": {
            "duration_ms": 1234,
            "warnings": [],
            "trace_id": "trace-uuid",
        },
    }

    validate_skill_response(response)


def test_skill_response_failure_shape():
    """
    A failed skill response MUST:
    - Have status == \"failure\"
    - Include error.code (string), error.message (string), error.retryable (boolean)
    - Include meta.duration_ms and meta.trace_id

    Spec: specs/technical.md §2.1 (failure envelope).
    """
    response = {
        "invocation_id": "invocation-uuid",
        "skill_name": "skill_fetch_trends",
        "status": "failure",
        "error": {
            "code": "UPSTREAM_TIMEOUT",
            "message": "Trend service did not respond in time",
            "retryable": True,
        },
        "meta": {
            "duration_ms": 30010,
            "trace_id": "trace-uuid",
        },
    }

    validate_skill_response(response)


def test_skill_response_rejects_side_effect_only_behavior():
    """
    Skills MUST NOT be side-effect-only:
    - A response with status == "success" but no output object should be rejected,
      because all meaningful effects and decisions must be surfaced via JSON.

    Spec: specs/technical.md §5.1/§5.2 (must surface all meaningful effects, no hidden channels).
    """
    bad_response = {
        "invocation_id": "invocation-uuid",
        "skill_name": "skill_fetch_trends",
        "status": "success",
        # "output" missing -> would imply side-effects not captured in contract
        "meta": {
            "duration_ms": 100,
            "trace_id": "trace-uuid",
        },
    }

    with pytest.raises(ValueError):
        validate_skill_response(bad_response)


def test_skill_response_rejects_undeclared_top_level_parameters():
    """
    Skill responses MUST adhere to the defined envelope.
    Top-level fields outside {invocation_id, skill_name, status, output/error, meta}
    are treated as violations to avoid accidental side channels.

    Spec: specs/technical.md §2.1 and §5.1/§5.2.
    Ambiguity: The spec does not explicitly forbid extra metadata fields; this test
    intentionally constrains the envelope to keep authority boundaries clean.
    """
    bad_response = {
        "invocation_id": "invocation-uuid",
        "skill_name": "skill_fetch_trends",
        "status": "success",
        "output": {"example": "value"},
        "meta": {
            "duration_ms": 10,
            "trace_id": "trace-uuid",
        },
        "debug": {"raw": "leaky-internal-state"},  # undeclared channel
    }

    with pytest.raises(ValueError):
        validate_skill_response(bad_response)

