import unittest

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestApp(unittest.TestCase):
    def test_get_info(self):
        # act
        response = client.get("/info")

        # assert
        self.assertEqual(200, response.status_code)
        self.assertEqual("running", response.json()["status"])

    def test_get_levels(self):
        # act
        response = client.get("/api/v1/levels?user_id=01&limit=5")

        # assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(5, len(response.json()))
