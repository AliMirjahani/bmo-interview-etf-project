import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from validator import validate_and_read_etf_csv
from exceptions import ETFValidationError


def validate_etf_csv_wrapper(file_path):
    try:
        df = validate_and_read_etf_csv(file_path)
        return True, None, 200, df
    except ETFValidationError as e:
        error_message = e.error_detail if e.error_detail else e.message
        return False, error_message, e.status_code, None
    except Exception as e:
        return False, str(e), None, None


class TestValidateETFCSV:
    @pytest.fixture
    def test_data_dir(self):
        return os.path.join(os.path.dirname(__file__), 'test_data')

    def test_valid_csv(self, test_data_dir):
        file_path = os.path.join(test_data_dir, 'valid.csv')
        is_valid, error_message, status_code, df = validate_etf_csv_wrapper(file_path)

        assert is_valid is True
        assert error_message is None
        assert status_code is 200
        assert df is not None
        assert len(df) == 3
        assert list(df.columns) == ['name', 'weight']

    def test_empty_csv(self, test_data_dir):
        file_path = os.path.join(test_data_dir, 'empty.csv')
        is_valid, error_message, status_code, df = validate_etf_csv_wrapper(file_path)

        assert is_valid is False
        assert "not a valid csv format" in error_message.lower() or "no columns to parse" in error_message.lower()
        assert status_code == 400
        assert df is None

    def test_missing_columns(self, test_data_dir):
        file_path = os.path.join(test_data_dir, 'missing_columns.csv')
        is_valid, error_message, status_code, df = validate_etf_csv_wrapper(file_path)

        assert is_valid is False
        assert "missing required columns" in error_message.lower()
        assert "weight" in error_message
        assert status_code == 400
        assert df is None

    def test_missing_name_column(self, test_data_dir):
        file_path = os.path.join(test_data_dir, 'missing_name_column.csv')
        is_valid, error_message, status_code, df = validate_etf_csv_wrapper(file_path)

        assert is_valid is False
        assert "missing required columns" in error_message.lower()
        assert "name" in error_message
        assert status_code == 400
        assert df is None

    def test_no_data_rows(self, test_data_dir):
        file_path = os.path.join(test_data_dir, 'no_data_rows.csv')
        is_valid, error_message, status_code, df = validate_etf_csv_wrapper(file_path)

        assert is_valid is False
        assert "empty" in error_message.lower() or "no data" in error_message.lower()
        assert status_code == 400
        assert df is None

    def test_missing_stock_names(self, test_data_dir):
        file_path = os.path.join(test_data_dir, 'missing_stock_names.csv')
        is_valid, error_message, status_code, df = validate_etf_csv_wrapper(file_path)

        assert is_valid is False
        assert "stock names are missing" in error_message.lower()
        assert status_code == 400
        assert df is None

    def test_missing_weights(self, test_data_dir):
        file_path = os.path.join(test_data_dir, 'missing_weights.csv')
        is_valid, error_message, status_code, df = validate_etf_csv_wrapper(file_path)

        assert is_valid is False
        assert "weights are missing" in error_message.lower()
        assert status_code == 400
        assert df is None

    def test_non_numeric_weights(self, test_data_dir):
        file_path = os.path.join(test_data_dir, 'non_numeric_weights.csv')
        is_valid, error_message, status_code, df = validate_etf_csv_wrapper(file_path)

        assert is_valid is False
        assert "weight values must be numbers" in error_message.lower()
        assert status_code == 400
        assert df is None

    def test_negative_weights(self, test_data_dir):
        file_path = os.path.join(test_data_dir, 'negative_weights.csv')
        is_valid, error_message, status_code, df = validate_etf_csv_wrapper(file_path)

        assert is_valid is False
        assert "cannot be negative" in error_message.lower()
        assert status_code == 400
        assert df is None

    def test_weights_over_one(self, test_data_dir):
        file_path = os.path.join(test_data_dir, 'weights_over_one.csv')
        is_valid, error_message, status_code, df = validate_etf_csv_wrapper(file_path)

        assert is_valid is False
        assert "cannot exceed 1.0" in error_message.lower()
        assert status_code == 400
        assert df is None

    def test_weights_sum_incorrect(self, test_data_dir):
        file_path = os.path.join(test_data_dir, 'weights_sum_incorrect.csv')
        is_valid, error_message, status_code, df = validate_etf_csv_wrapper(file_path)

        assert is_valid is False
        assert "should sum to approximately 1.0" in error_message.lower()
        assert status_code == 400
        assert df is None

    def test_file_not_found(self):
        file_path = 'non_existent_file.csv'
        is_valid, error_message, status_code, df = validate_etf_csv_wrapper(file_path)

        assert is_valid is False
        assert "file not found" in error_message.lower() or "not found" in error_message.lower()
        assert status_code == 400
        assert df is None

    def test_invalid_csv_format(self, test_data_dir):
        file_path = os.path.join(test_data_dir, 'not_a_csv.txt')
        is_valid, error_message, status_code, df = validate_etf_csv_wrapper(file_path)

        assert is_valid is False
        assert status_code == 400
        assert df is None
