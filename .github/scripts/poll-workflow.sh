#!/bin/bash

WORKFLOW_NAME="$1"
TAG_NAME="$2"
GITHUB_REPOSITORY="$3"
MAX_ATTEMPTS=30

ATTEMPT=0
while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
  RUNS=$(gh api -H "Accept: application/vnd.github+json" \
    /repos/${GITHUB_REPOSITORY}/actions/runs \
    -q ".workflow_runs[] | select(.name == \"$WORKFLOW_NAME\" and .event == \"repository_dispatch\" and .head_branch == \"sync/$TAG_NAME\") | [.id, .status, .conclusion] | @csv" | head -n 1)
  
  if [[ -z "$RUNS" ]]; then
    echo "No workflow run found. Attempt $ATTEMPT of $MAX_ATTEMPTS"
    ATTEMPT=$((ATTEMPT + 1))
    sleep 10
    continue
  fi

  IFS=',' read -r -a RUN_DATA <<< "$RUNS"
  STATUS=${RUN_DATA[1]//\"/}
  CONCLUSION=${RUN_DATA[2]//\"/}

  echo "Current status: $STATUS, conclusion: $CONCLUSION"

  if [[ "$STATUS" == "completed" ]]; then
    if [[ "$CONCLUSION" != "success" ]]; then
      echo "Workflow failed with conclusion: $CONCLUSION"
      exit 1
    fi
    exit 0
  fi

  ATTEMPT=$((ATTEMPT + 1))
  sleep 10
done

echo "Timeout reached while waiting for workflow completion"
exit 1