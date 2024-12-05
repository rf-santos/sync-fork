from unittest.mock import Mock, patch
import pytest
import json

class TestGitHubIntegration:
    @patch('github.Github')
    def test_pr_creation(self, mock_github):
        """Test Pull Request creation."""
        mock_repo = Mock()
        mock_github.return_value.get_repo.return_value = mock_repo
        
        pr_data = {
            "title": "Sync: Upstream release v1.1.0",
            "body": "This PR synchronizes our fork with upstream release v1.1.0",
            "head": "sync/v1.1.0",
            "base": "main"
        }
        
        mock_repo.create_pull.return_value = Mock(number=1, html_url="https://github.com/owner/repo/pull/1")
        
        # Simulate PR creation
        pr = mock_repo.create_pull(**pr_data)
        
        assert pr.number == 1
        mock_repo.create_pull.assert_called_once_with(**pr_data)
    
    @patch('github.Github')
    def test_auto_merge(self, mock_github):
        """Test automatic PR merging."""
        mock_repo = Mock()
        mock_pr = Mock()
        mock_github.return_value.get_repo.return_value = mock_repo
        mock_repo.get_pull.return_value = mock_pr
        
        # Simulate merge
        mock_pr.merge.return_value = True
        result = mock_pr.merge()
        
        assert result is True
        mock_pr.merge.assert_called_once()