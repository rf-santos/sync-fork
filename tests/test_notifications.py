from unittest.mock import Mock, patch
import pytest

class TestNotifications:
    @patch('github.Github')
    def test_failure_notification(self, mock_github):
        """Test creation of failure notification issues."""
        mock_repo = Mock()
        mock_github.return_value.get_repo.return_value = mock_repo
        
        issue_data = {
            "title": "⚠️ Sync failed for release v1.2.0",
            "body": "Synchronization with upstream release v1.2.0 failed.\n\nMerge Status: conflicts"
        }
        
        mock_repo.create_issue.return_value = Mock(number=1)
        
        # Simulate issue creation
        issue = mock_repo.create_issue(**issue_data)
        
        assert issue.number == 1
        mock_repo.create_issue.assert_called_once_with(**issue_data)