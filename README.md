# Fork synchronization workflow
Boilerplate CI/CD to sync an upstream fork.

# Setup

## Initial Setup

1. Fork the repository on GitHub
2. Create a `.github/workflows` directory in your fork
3. Save the workflow file as `.github/workflows/sync-fork.yml`
4. Create a `.github/patches` directory to store your customizations
5. Add the upstream repository URL as a repository variable named `UPSTREAM_REPO_URL`
6. Make sure your repository has the necessary permissions enabled:
   1. Go to Settings → Actions → General
   2. Under "Workflow permissions", enable "Read and write permissions"


## Managing Customizations

1. Create a patch file of your customizations:
```bash
git diff main...your-customization-branch > .github/patches/customizations.patch
```

2. Store this patch file in your repository. The workflow will automatically attempt to apply these customizations after each sync


# How it Works:

The workflow runs daily and can also be triggered manually
It checks for new releases in the upstream repository
When a new release is detected, it:

- Creates a new branch
- Merges the release
- Applies your customizations
- Creates a pull request for review
- Automatically merge the PR if all checks pass

# Repository Strucutre

```

.github/
├── workflows/
│   └── sync-fork.yml
└── patches/
    └── customizations.patch
tests/
├── __init__.py
├── conftest.py
├── test_sync_workflow.py
├── test_github_integration.py
└── test_notifications.py
```