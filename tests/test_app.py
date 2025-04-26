import unittest
from unittest.mock import patch, MagicMock
import streamlit as st

# Mock dependencies before importing app
with patch("auth.login_form"), patch("database.get_favorite_stocks"), patch("user_data.record_search"):
    import app

class TestApp(unittest.TestCase):

    def setUp(self):
        """Set up the Streamlit session state for testing."""
        st.session_state.clear()
        st.session_state.ticker = ""
        st.session_state.last_update_time = None
        st.session_state.auto_refresh = False
        st.session_state.refresh_interval = 60
        st.session_state.data = None
        st.session_state.history = None
        st.session_state.ai_insights = None
        st.session_state.error = None
        st.session_state.is_loading_data = False
        st.session_state.is_loading_insights = False
        st.session_state.is_favorite = False

    @patch("stock_analysis.get_stock_data")
    def test_update_data_success(self, mock_get_stock_data):
        """Test the update_data function when stock data is successfully fetched."""
        mock_get_stock_data.return_value = (
            {"currentPrice": 150.0, "previousClose": 145.0},
            MagicMock()  # Mocked stock history data
        )
        app.update_data("AAPL")
        self.assertEqual(st.session_state.ticker, "AAPL")
        self.assertIsNotNone(st.session_state.data)
        self.assertIsNotNone(st.session_state.history)
        self.assertIsNone(st.session_state.error)

    @patch("stock_analysis.get_stock_data")
    def test_update_data_failure(self, mock_get_stock_data):
        """Test the update_data function when stock data fetch fails."""
        mock_get_stock_data.side_effect = Exception("API error")
        app.update_data("INVALID")
        self.assertEqual(st.session_state.ticker, "INVALID")
        self.assertIsNone(st.session_state.data)
        self.assertIsNone(st.session_state.history)
        self.assertIn("Error fetching data", st.session_state.error)

    def test_session_state_initialization(self):
        """Test that session state variables are initialized correctly."""
        self.assertEqual(st.session_state.ticker, "")
        self.assertIsNone(st.session_state.last_update_time)
        self.assertFalse(st.session_state.auto_refresh)
        self.assertEqual(st.session_state.refresh_interval, 60)
        self.assertIsNone(st.session_state.data)
        self.assertIsNone(st.session_state.history)
        self.assertIsNone(st.session_state.ai_insights)
        self.assertIsNone(st.session_state.error)
        self.assertFalse(st.session_state.is_loading_data)
        self.assertFalse(st.session_state.is_loading_insights)
        self.assertFalse(st.session_state.is_favorite)

if __name__ == "__main__":
    unittest.main()
