import unittest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app


class TestMain(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("app.main.load_dataset")
    def test_startup_loads_dataset(self, mock_load):
        mock_load.return_value = AsyncMock(return_value=[])()

        with self.client:
            mock_load.assert_called_once()

    @patch("app.main.load_dataset", new_callable=AsyncMock)
    def test_startup_loads_dataset_exception(self, mock_load):
        mock_load.side_effect = Exception("Test exception")

        with self.assertRaises(Exception) as context:
            with self.client:
                pass

        self.assertEqual(str(context.exception), "Test exception")

    @patch("app.main.app.state")
    def test_info_endpoint_returns_correct_response(self, mock_app_state):
        # Arrange
        mock_dataset = [1, 2, 3]
        mock_app_state.dataset = mock_dataset
        expected_response = {"status": "running", "dataset_size": 3}

        # Act
        response = self.client.get("/info")

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response)


if __name__ == "__main__":
    unittest.main()
