# Fork Synchronization Workflow
Automatically sync your fork with upstream releases while preserving your customizations.

## Features
- Daily automatic sync checks
- Custom patch preservation
- Automated PR creation and merging
- Built-in test workflow

## Setup
1. Repository Configuration

```
# Required repository secrets
UPSTREAM_REPO_URL=https://github.com/original/repo.git

# Enable workflow permissions
Settings → Actions → General → "Read and write permissions"
```

2. Directory Structure

```
.github/
├── workflows/
│   ├── sync-fork.yml      
│   └── test_sync-fork.yml 
├── patches/
│   ├── customizations.patch
│   └── test-customizaitons.patch
├── scripts/
│   └── poll_workflow.py
└── test/
    └── test-patch.md
```

## Workflow Steps
1. Schedule: Daily or manual trigger
2. Check: Monitor upstream releases
3. Branch: Create sync branch
4. Sync: Merge latest release
5. Customize: Apply patches
6. Review: Create PR
7. Merge: Auto-merge if checks pass

## Testing

```
# Via GitHub UI
Actions → Test Sync Workflow → Run workflow

# Test workflow will:
- Create mock tags
- Trigger sync
- Apply test patches
- Cleanup
```

## Error Handling
- Merge conflicts: Manual resolution required
- Failed patches: Reported in PR
- Status updates: Actions tab

## Troubleshooting
- Check Actions logs
- Verify UPSTREAM_REPO_URL
- Validate patch format
- Review permissions

## License
GNU GPL v3