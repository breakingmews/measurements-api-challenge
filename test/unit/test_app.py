import unittest
from datetime import datetime
from typing import Sequence
from unittest.mock import patch

from fastapi.testclient import TestClient

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

    @patch("app.dependencies.service.MeasurementService.get_measurements_count")
    def test_info_endpoint(self, get_measurements_count_mock):
        # arrange
        get_measurements_count_mock.return_value = 10
        expected = {"status": "running", "dataset_size": 10}

        # act
        response = self.client.get("/info")

        # assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json(), expected)

    @patch("app.dependencies.service.MeasurementService.get_measurements")
    def test_get_measurements(self, get_measurements_mock):
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
            "/api/v1/measurements",
            params={
                "user_id": "test_user",
                "offset": 0,
                "limit": 10,
                "device_timestamp_from": "2021-02-13T00:06:00",
            },
        )

        # assert
        expected = {
            "measurements": [
                {
                    "device_id": "test_device",
                    "user_id": "test_user",
                    "device_timestamp": "2021-02-13T00:06:00",
                    "value": 5.5,
                }
            ]
        }
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.json())
        self.assertNotIn("id", response.json())

    @patch("app.dependencies.service.MeasurementService.get_measurement")
    def test_get_measurement(self, mock_get_measurement):
        # arrange
        mock_measurement: Measurement = Measurement(
            id="1",
            user_id="test_user",
            device_id="test_device",
            device_timestamp=datetime(2021, 2, 13, 0, 6, 0),
            value=5.5,
        )

        mock_get_measurement.return_value = mock_measurement

        # act
        response = self.client.get("/api/v1/measurements/1")

        # assert
        expected = {
            "device_id": "test_device",
            "user_id": "test_user",
            "device_timestamp": "2021-02-13T00:06:00",
            "value": 5.5,
        }

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.json())
        self.assertNotIn("id", response.json())

    @patch("app.dependencies.service.MeasurementService.get_measurement")
    def test_get_measurement_not_found(self, mock_get_measurement):
        # arrange
        mock_get_measurement.return_value = None

        # act
        response = self.client.get("/api/v1/measurements/1")

        # assert
        self.assertEqual(404, response.status_code)
        self.assertEqual(response.json()["message"], "Not found")

    @patch("app.dependencies.service.MeasurementService.get_measurements")
    def test_get_measurements_not_found(self, get_measurements_mock):
        # arrange
        get_measurements_mock.return_value = []

        # act
        response = self.client.get(
            "/api/v1/measurements",
            params={
                "user_id": "test_user",
                "offset": 0,
                "limit": 10,
                "device_timestamp_from": "2021-02-13T00:06:00",
            },
        )

        # assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json()["measurements"], [])


if __name__ == "__main__":
    unittest.main()
