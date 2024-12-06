# .github/scripts/poll_workflow.py
import os
import sys
import time
import requests
from datetime import datetime, timedelta

def poll_workflow(workflow_name, tag_name, repo):
    token = os.environ['GITHUB_TOKEN']
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}'
    }
    
    # Initial delay
    time.sleep(15)
    
    start_time = datetime.now()
    max_duration = timedelta(minutes=5)
    
    while datetime.now() - start_time < max_duration:
        url = f'https://api.github.com/repos/{repo}/actions/runs'
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"API request failed: {response.status_code}")
            print(response.text)
            sys.exit(1)
            
        data = response.json()
        
        # Find relevant workflow runs
        runs = [
            run for run in data['workflow_runs']
            if run['name'] == workflow_name 
            and run['event'] == 'repository_dispatch'
        ]
        
        if not runs:
            print("No matching workflow runs found. Waiting...")
            time.sleep(10)
            continue
            
        latest_run = runs[0]
        print(f"Latest run - Status: {latest_run['status']}, Conclusion: {latest_run['conclusion']}")
        
        if latest_run['status'] == 'completed':
            if latest_run['conclusion'] == 'success':
                print("Workflow completed successfully")
                sys.exit(0)
            elif latest_run['conclusion']:
                print(f"Workflow failed with conclusion: {latest_run['conclusion']}")
                sys.exit(1)
                
        time.sleep(10)
    
    print("Timeout reached while waiting for workflow completion")
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: poll_workflow.py WORKFLOW_NAME TAG_NAME REPO")
        sys.exit(1)
        
    poll_workflow(sys.argv[1], sys.argv[2], sys.argv[3])