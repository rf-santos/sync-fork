import pytest
from pathlib import Path
import git
import shutil
import os

@pytest.fixture(scope="session")
def test_repos(request):
    """Create test repositories for the test session."""
    base_dir = Path(".github/test/repos")
    repos = {}

    def cleanup():
        # Close any open repos
        for repo in repos.values():
            if repo.is_valid():
                repo.close()
        
        # Clean up test directory
        if base_dir.exists():
            # Use git.rmtree() for Git repos
            for repo_path in ['upstream', 'fork']:
                full_path = base_dir / repo_path
                if full_path.exists():
                    git.rmtree(str(full_path))
            # Remove base directory
            if base_dir.exists():
                shutil.rmtree(base_dir, ignore_errors=True)

    # Register cleanup 
    request.addfinalizer(cleanup)

    # Clean up any existing test repos
    cleanup()
    
    # Create test directory
    base_dir.mkdir(parents=True)
    
    # Create upstream repo
    upstream_path = base_dir / "upstream"
    upstream = git.Repo.init(upstream_path)
    repos['upstream'] = upstream
    
    # Initial commit in upstream
    readme = upstream_path / "README.md"
    readme.write_text("# Test Upstream")
    upstream.index.add(["README.md"])
    upstream.index.commit("Initial commit")
    upstream.create_tag("v1.0.0")
    
    # Add new feature
    feature = upstream_path / "feature.txt"
    feature.write_text("New feature")
    upstream.index.add(["feature.txt"])
    upstream.index.commit("Add new feature")
    upstream.create_tag("v1.1.0")
    
    # Add another tag to simulate a new release
    new_feature = upstream_path / "new_feature.txt"
    new_feature.write_text("Another new feature")
    upstream.index.add(["new_feature.txt"])
    upstream.index.commit("Add another new feature")
    upstream.create_tag("v1.2.0")
    
    # Create fork
    fork_path = base_dir / "fork"
    fork = git.Repo.clone_from(str(upstream_path), fork_path)
    repos['fork'] = fork
    fork.create_remote("upstream", str(upstream_path))
    
    # Add custom feature to fork
    custom = fork_path / "custom.txt"
    custom.write_text("Custom feature")
    fork.index.add(["custom.txt"])
    fork.index.commit("Add custom feature")

    return repos