# Test: {{test_name}}
# Suite: {{suite}}
# Endpoint: POST {{endpoint}}

POST {{base_url}}{{endpoint}}
Content-Type: application/json
{
  "title": "test",
  "body": "test body",
  "userId": 1
}
HTTP 201
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$.id" exists
