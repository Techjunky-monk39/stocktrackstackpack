import os
import unittest
from unittest.mock import patch, MagicMock
import health_checks

class TestHealthChecks(unittest.TestCase):

    @patch("requests.get")
    def test_check_openai_api_success(self, mock_get):
        """Test OpenAI API health check when the API is reachable."""
        os.environ["OPENAI_API_KEY"] = "test_key"
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = health_checks.check_openai_api()
        self.assertEqual(result, "OpenAI API is working correctly.")

    @patch("requests.get")
    def test_check_openai_api_failure(self, mock_get):
        """Test OpenAI API health check when the API is unreachable."""
        os.environ["OPENAI_API_KEY"] = "test_key"
        mock_get.side_effect = Exception("API unreachable")

        result = health_checks.check_openai_api()
        self.assertIn("Error checking OpenAI API", result)

    def test_check_openai_api_no_key(self):
        """Test OpenAI API health check when the API key is missing."""
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]

        result = health_checks.check_openai_api()
        self.assertEqual(result, "Warning: OPENAI_API_KEY environment variable not set.")

    @patch("requests.get")
    def test_check_codegpt_api_success(self, mock_get):
        """Test CodeGPT API health check when the API is reachable."""
        os.environ["CODEGPT_API_KEY"] = "test_key"
        os.environ["CODEGPT_HEALTH_CHECK_ENDPOINT"] = "https://example.com/health"
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = health_checks.check_codegpt_api()
        self.assertEqual(result, "CodeGPT API is working correctly.")

    @patch("requests.get")
    def test_check_codegpt_api_failure(self, mock_get):
        """Test CodeGPT API health check when the API is unreachable."""
        os.environ["CODEGPT_API_KEY"] = "test_key"
        os.environ["CODEGPT_HEALTH_CHECK_ENDPOINT"] = "https://example.com/health"
        mock_get.side_effect = Exception("API unreachable")

        result = health_checks.check_codegpt_api()
        self.assertIn("Error checking CodeGPT API", result)

    def test_check_codegpt_api_no_key(self):
        """Test CodeGPT API health check when the API key is missing."""
        if "CODEGPT_API_KEY" in os.environ:
            del os.environ["CODEGPT_API_KEY"]

        result = health_checks.check_codegpt_api()
        self.assertEqual(result, "Warning: CODEGPT_API_KEY environment variable not set.")

if __name__ == "__main__":
    unittest.main()
