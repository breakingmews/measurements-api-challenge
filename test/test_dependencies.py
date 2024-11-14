import unittest

import pandas as pd

from app.dependencies import prepare_dataset


class TestCase(unittest.TestCase):
    def test_prepare_dataset(self):
        # arrange
        data1 = pd.DataFrame(
            {
                "Seriennummer": ["123", "456"],
                "Gerätezeitstempel": ["2023-01-01 00:00:00", "2023-01-01 01:00:00"],
                "Glukosewert-Verlauf mg/dL": [100, 110],
                "OtherColumn": [1, 2],
            },
        )

        data2 = pd.DataFrame(
            {
                "Seriennummer": ["789", "012"],
                "Gerätezeitstempel": ["2023-01-01 02:00:00", "2023-01-01 03:00:00"],
                "Glukosewert-Verlauf mg/dL": [120, 130],
                "OtherColumn": [3, 4],
            }
        )

        dataset = [data1, data2]

        # act
        result = prepare_dataset(dataset)

        # assert
        expected = pd.DataFrame(
            {
                "serial_number": ["123", "456", "789", "012"],
                "device_timestamp": [
                    "2023-01-01 00:00:00",
                    "2023-01-01 01:00:00",
                    "2023-01-01 02:00:00",
                    "2023-01-01 03:00:00",
                ],
                "glucose_value_mgdl": [100, 110, 120, 130],
            },
            index=[0, 1, 0, 1],
        )

        pd.testing.assert_frame_equal(result, expected)
