import pytest
import git
from pathlib import Path
from unittest.mock import Mock, patch

class TestSyncWorkflow:
    def test_new_release_detection(self, test_repos):
        """Test if new releases are correctly detected."""
        fork = test_repos["fork"]
        upstream = test_repos["upstream"]
        
        # Fetch tags from upstream
        fork.remotes.upstream.fetch("--tags")
        
        # Get latest tag
        latest_tag = sorted(upstream.tags, key=lambda t: t.name)[-1]
        
        assert latest_tag.name == "v1.1.0"
        
        # Test branch creation
        new_branch = fork.create_head(f"sync/{latest_tag.name}")
        new_branch.checkout()
        
        assert fork.active_branch.name == f"sync/{latest_tag.name}"
    
    def test_patch_application(self, test_repos):
        """Test if patches are correctly applied."""
        fork = test_repos["fork"]
        patch_file = Path(".github/patches/customizations.patch")
        
        # Try to apply patch
        result = fork.git.apply("--check", str(patch_file))
        
        assert result is None  # No exception means patch can be applied
        
        # Actually apply patch
        fork.git.apply(str(patch_file))
        custom_file = Path(fork.working_dir) / "custom.txt"
        
        assert custom_file.exists()
        assert custom_file.read_text() == "Custom feature"
    
    def test_conflict_handling(self, test_repos):
        """Test handling of merge conflicts."""
        upstream = test_repos["upstream"]
        fork = test_repos["fork"]
        
        # Create conflicting change in upstream
        conflict_file = Path(upstream.working_dir) / "custom.txt"
        conflict_file.write_text("Conflicting change")
        upstream.index.add(["custom.txt"])
        upstream.index.commit("Add conflicting change")
        upstream.create_tag("v1.2.0")
        
        # Try to merge in fork
        fork.remotes.upstream.fetch("--tags")
        with pytest.raises(git.GitCommandError):
            fork.git.merge("v1.2.0")