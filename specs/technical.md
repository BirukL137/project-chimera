## Trend Fetch API Contract

Input:
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
