#!/bin/bash
# This script reports on all policy violations across all namespaces and creates alerts.csv
# Requires ROX_ENDPOINT and ROX_API_TOKEN environment variables
# Requires analyst access or more in ACS

# Environment variables
bearer_token="$ROX_API_TOKEN"
api_endpoint="$ROX_ENDPOINT"
api_url="https://${api_endpoint}/v1/alerts?status=ACTIVE&namespace=*"

# Check if environment variables are set
if [[ -z "$bearer_token" || -z "$api_endpoint" ]]; then
    echo "Environment variables ROX_API_TOKEN and ROX_ENDPOINT are required."
    exit 1
fi

# Make the API request and write the output to alerts.txt
curl -s -k -H "Authorization: Bearer ${bearer_token}" -H "Accept: application/json" "$api_url" | \
jq -c '.alerts[]' > alerts.txt

# Check if alerts were found
if [[ ! -s alerts.txt ]]; then
    echo "No alerts found."
    exit 1
fi

# Convert JSON in alerts.txt to CSV and save as alerts.csv
jq -r '[.id, .time, .lifecycleStage, .policy.name, .policy.severity, .policy.description, .state, .enforcementAction, .commonEntityInfo.clusterName, .commonEntityInfo.namespace, .deployment.name] | @csv' alerts.txt > alerts.csv

echo "Alerts have been successfully fetched and saved to alerts.csv."
