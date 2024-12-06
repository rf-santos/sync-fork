# .github/scripts/poll_workflow.py
import os
import sys
import time
from datetime import datetime, timedelta
from github import Github
from github.GithubException import GithubException

def poll_workflow(workflow_name, repo):
    try:
        gh = Github(os.environ['GITHUB_TOKEN'])
        repository = gh.get_repo(repo)
        
        # Initial delay to allow workflow to start
        time.sleep(15)
        
        start_time = datetime.now()
        max_duration = timedelta(minutes=5)
        
        while datetime.now() - start_time < max_duration:
            runs = repository.get_workflow_runs(
                event='repository_dispatch'
            )
            
            matching_runs = [
                run for run in runs
                if run.name == workflow_name
            ]
            
            if not matching_runs:
                print("No matching workflow runs found. Waiting...")
                time.sleep(10)
                continue
                
            latest_run = matching_runs[0]
            print(f"Latest run - Status: {latest_run.status}, Conclusion: {latest_run.conclusion}")
            
            if latest_run.status == 'completed':
                if latest_run.conclusion == 'success':
                    print("Workflow completed successfully")
                    return 0
                elif latest_run.conclusion:
                    print(f"Workflow failed with conclusion: {latest_run.conclusion}")
                    return 1
                    
            time.sleep(10)
            
        print("Timeout reached while waiting for workflow completion")
        return 1
        
    except GithubException as e:
        print(f"GitHub API error: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: poll_workflow.py WORKFLOW_NAME REPO")
        sys.exit(1)

    result = poll_workflow(sys.argv[1], sys.argv[2])
    print(f"Workflow result: {result}")
    if result != 0:
        print("Triggered workflow failed...")
        sys.exit(1)
