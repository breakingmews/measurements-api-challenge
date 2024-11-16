import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from app.dependencies.database import (
    import_dataset,
)


class TestDatabase(unittest.TestCase):
    @patch("app.dependencies.database.load_dataset")
    @patch("app.dependencies.database.get_session")
    @patch("app.dependencies.database.get_measurements_count")
    def test_import_dataset_new_data(
        self, mock_get_measurements_count, mock_get_session, mock_load_dataset
    ):
        # arrange
        mock_session = MagicMock()
        mock_get_session.return_value = iter([mock_session])
        mock_get_measurements_count.return_value = 0

        mock_data = pd.DataFrame([{"id": 1, "value": "test"}])
        mock_load_dataset.return_value = mock_data

        # act
        import_dataset()

        # assert
        mock_load_dataset.assert_called_once()
        self.assertEqual(mock_session.add.call_count, len(mock_data))
        self.assertEqual(mock_session.commit.call_count, len(mock_data))

    @patch("app.dependencies.database.load_dataset")
    @patch("app.dependencies.database.get_session")
    @patch("app.dependencies.database.get_measurements_count")
    def test_import_dataset_existing_data(
        self, mock_get_measurements_count, mock_get_session, mock_load_dataset
    ):
        # arrange
        mock_session = MagicMock()
        mock_get_session.return_value = iter([mock_session])
        mock_get_measurements_count.return_value = 10

        # act
        import_dataset()

        # assert
        mock_load_dataset.assert_not_called()
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()


if __name__ == "__main__":
    unittest.main()
