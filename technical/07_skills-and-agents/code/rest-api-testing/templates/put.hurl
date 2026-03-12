# Test: {{test_name}}
# Suite: {{suite}}
# Endpoint: PUT {{endpoint}}

PUT {{base_url}}{{endpoint}}
Content-Type: application/json
{
  "id": 1,
  "title": "updated",
  "body": "updated body",
  "userId": 1
}
HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
