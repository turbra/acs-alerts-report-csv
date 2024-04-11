# This script reports on all policy violations across all namespaces and creates alerts.csv
# Requires ROX_ENDPOINT and ROX_API_TOKEN environment variables
# Requires analyst access or more in ACS

import requests
import json
import subprocess
import os

def get_alerts(api_endpoint, bearer_token):
    api_url = f'https://{api_endpoint}/v1/alerts?status=ACTIVE&namespace=*'
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Accept': 'application/json'
    }
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        data = json.loads(response.text)
        alerts = data.get('alerts')
        if alerts:
            with open('alerts.txt', 'w') as f:
                for alert in alerts:
                    alert_data = {'id': alert['id'], 'time': alert['time']}
                    alert_data.update(alert)
                    f.write(json.dumps(alert_data) + '\n')
            jq_command = "jq -r '[.id, .time, .lifecycleStage, .policy.name, .policy.severity, .policy.description, .state, .enforcementAction, .commonEntityInfo.clusterName, .commonEntityInfo.namespace, .deployment.name] | @csv' alerts.txt > alerts.csv"
            subprocess.run(jq_command, shell=True, check=True)
        else:
            print("No alerts found.")
    else:
        print(response.text)

# Use environment variables
bearer_token = os.environ.get('ROX_API_TOKEN')
api_endpoint = os.environ.get('ROX_ENDPOINT')

if bearer_token and api_endpoint:
    get_alerts(api_endpoint, bearer_token)
else:
    print("Environment variables ROX_API_TOKEN and ROX_ENDPOINT are required.")
