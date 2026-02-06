import pytest

# NOTE: These imports intentionally reference not-yet-implemented contract validators.
# Under TDD, tests should fail initially (ImportError / AttributeError) until the
# implementation is created in a spec-compliant way.
# Spec reference: specs/technical.md §3.1 (MCP trend_fetch_api) and §2.2 (skill_fetch_trends).
from chimera.contracts.trends import (  # type: ignore[import-not-found]
    validate_mcp_trend_response,
    validate_skill_fetch_trends_output,
)


def test_mcp_trend_response_happy_path_structure():
    """
    A successful MCP trend_fetch_api response MUST:
    - Have ok == True
    - Contain result.trends as a list
    - Each trend item has topic (string), score (number), timestamp (ISO-8601 string)

    Spec: specs/technical.md §3.1 Generic MCP Tool Request/Response.
    """
    response = {
        "ok": True,
        "result": {
            "trends": [
                {
                    "topic": "home workout challenges",
                    "score": 0.87,
                    "timestamp": "2025-01-10T11:58:00Z",
                }
            ]
        },
    }

    # Expected: does NOT raise; returns a truthy/None sentinel indicating validity.
    validate_mcp_trend_response(response)


def test_mcp_trend_response_rejects_missing_required_fields():
    """
    An MCP trend_fetch_api response MUST be rejected when:
    - ok is True but result.trends[*].topic / score / timestamp is missing.

    Spec: specs/technical.md §3.1 (trend structure under result.trends).
    """
    bad_response = {
        "ok": True,
        "result": {
            "trends": [
                {
                    # "topic" missing
                    "score": 0.87,
                    "timestamp": "2025-01-10T11:58:00Z",
                }
            ]
        },
    }

    with pytest.raises(ValueError):
        validate_mcp_trend_response(bad_response)


def test_mcp_trend_response_rejects_wrong_types():
    """
    A trend item MUST have correct types:
    - topic: string
    - score: number
    - timestamp: string (ISO-8601)

    Spec: specs/technical.md §3.1.
    Ambiguity: ISO-8601 validation strictness is not defined; these tests only
    assert type-level contracts, leaving formatting specifics to later refinement.
    """
    bad_response = {
        "ok": True,
        "result": {
            "trends": [
                {
                    "topic": 123,  # wrong type
                    "score": "0.87",  # wrong type
                    "timestamp": 1704882000,  # wrong type
                }
            ]
        },
    }

    with pytest.raises(ValueError):
        validate_mcp_trend_response(bad_response)


def test_skill_fetch_trends_output_happy_path_structure():
    """
    skill_fetch_trends output MUST:
    - Provide trends[] with topic, score, timestamp, optional examples[]
    - Provide source with platform, region, retrieved_at

    Spec: specs/technical.md §2.2 skill_fetch_trends Contract.
    """
    output = {
        "trends": [
            {
                "topic": "home workout challenges",
                "score": 0.87,
                "timestamp": "2025-01-10T11:58:00Z",
                "examples": [
                    {
                        "content_id": "external-content-id-1",
                        "title": "7-day core challenge",
                        "url": "https://platform.example/trend/123",
                    }
                ],
            }
        ],
        "source": {
            "platform": "tiktok",
            "region": "US",
            "retrieved_at": "2025-01-10T12:00:00Z",
        },
    }

    validate_skill_fetch_trends_output(output)


def test_skill_fetch_trends_output_rejects_missing_source():
    """
    skill_fetch_trends output MUST include source.platform, source.region,
    and source.retrieved_at.

    Spec: specs/technical.md §2.2 (source object).
    """
    bad_output = {
        "trends": [
            {
                "topic": "home workout challenges",
                "score": 0.87,
                "timestamp": "2025-01-10T11:58:00Z",
            }
        ],
        # "source" missing
    }

    with pytest.raises(ValueError):
        validate_skill_fetch_trends_output(bad_output)


def test_skill_fetch_trends_output_rejects_malformed_trend_items():
    """
    skill_fetch_trends MUST reject malformed trend entries inside trends[]:
    - Missing topic / score / timestamp
    - Wrong types for those fields

    Spec: specs/technical.md §2.2.
    """
    bad_output = {
        "trends": [
            {
                "topic": "home workout challenges",
                "score": "0.87",  # wrong type
                "timestamp": "2025-01-10T11:58:00Z",
            }
        ],
        "source": {
            "platform": "tiktok",
            "region": "US",
            "retrieved_at": "2025-01-10T12:00:00Z",
        },
    }

    with pytest.raises(ValueError):
        validate_skill_fetch_trends_output(bad_output)

