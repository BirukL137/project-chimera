# Technical Specification — Project Chimera

## API Contracts

### Trend Fetch Contract

Input:
```json
{
  "platform": "string",
  "region": "string",
  "limit": "integer"
}

Output:
{
  "trends": [
    {
      "topic": "string",
      "score": "number",
      "timestamp": "ISO-8601"
    }
  ]
}

## Database Schema (High-Level)

erDiagram
  VIDEO ||--o{ METADATA : has
  VIDEO {
    uuid id
    string platform
    datetime created_at
  }
  METADATA {
    string topic
    number relevance_score
  }

## Tooling & MCP Governance

- All external tools (APIs, scrapers, platform SDKs) are accessed exclusively via MCP servers.
- Agents cannot bypass MCP or invoke tools directly.
- Tool enablement and scope are:
  - Defined at deploy-time
  - Approved by the Human Operator
- MCP enforces:
  - Allowlisted tools only
  - Read/write permission boundaries
  - Auditable request logs

## MCP Enforcement Boundary

- Agents (Planner, Worker, Judge) do not possess network or API credentials.
- All external I/O capabilities are available only to the MCP runtime layer.
- Skills are executed in a restricted execution environment with no direct outbound access.
- Any attempt to access external systems outside MCP is considered a hard violation and results in task termination.
