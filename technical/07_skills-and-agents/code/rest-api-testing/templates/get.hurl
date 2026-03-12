# Test: {{test_name}}
# Suite: {{suite}}
# Endpoint: GET {{endpoint}}

GET {{base_url}}{{endpoint}}
HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
