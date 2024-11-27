import unittest

from fastapi.testclient import TestClient

from app.main import app


class TestApp(unittest.TestCase):
    def test_get_info(self):
        # act
        with TestClient(app) as client:
            response = client.get("/info")

        # assert
        self.assertEqual(200, response.status_code)
        self.assertEqual("running", response.json()["status"])

    def test_get_measurements(self):
        # act
        with TestClient(app) as client:
            response = client.get("/api/v1/measurements?user_id=01&limit=5")

        # assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(5, len(response.json()["measurements"]))
