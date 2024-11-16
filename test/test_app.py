import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.dependencies.database import get_measurements_count
from app.main import app


class TestMain(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("app.main.create_db_and_tables")
    @patch("app.main.import_dataset")
    def test_startup_loads_dataset(self, mock_create_db, mock_import_dataset):
        # act
        with self.client:
            pass

        # assert
        mock_create_db.assert_called_once()
        mock_import_dataset.assert_called_once()

    def test_info_endpoint(self):
        # arrange
        app.dependency_overrides[get_measurements_count] = lambda: 10
        expected = {"status": "running", "dataset_size": 10}

        # act
        response = self.client.get("/info")

        # assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json(), expected)


if __name__ == "__main__":
    unittest.main()
