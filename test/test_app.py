import unittest
from datetime import datetime
from typing import Sequence
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.dependencies.database import (
    get_measurements_count,
)
from app.main import app
from app.model import Measurement


class TestApp(unittest.TestCase):
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

    @patch("app.router.get_measurements")
    def test_levels(self, get_measurements_mock):
        # arrange
        mock_measurements: Sequence[Measurement] = [
            Measurement(
                id="1",
                user_id="test_user",
                device_id="test_device",
                device_timestamp=datetime(2021, 2, 13, 0, 6, 0),
                value=5.5,
            )
        ]

        get_measurements_mock.return_value = mock_measurements

        # act
        response = self.client.get(
            "/api/v1/levels",
            params={
                "user_id": "test_user",
                "offset": 0,
                "limit": 10,
                "device_timestamp_from": "2021-02-13T00:06:00",
            },
        )

        # assert
        expected = [
            {
                "device_id": "test_device",
                "user_id": "test_user",
                "device_timestamp": "2021-02-13T00:06:00",
                "value": 5.5,
            }
        ]
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.json())
        self.assertNotIn("id", response.json())


if __name__ == "__main__":
    unittest.main()
