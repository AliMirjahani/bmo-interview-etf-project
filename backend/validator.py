import pandas as pd

from exceptions import (
    ETFFileNotFoundError,
    FileEncodingError,
    InvalidCSVFormatError,
    EmptyFileError,
    MissingColumnsError,
    NoDataRowsError,
    MissingStockNamesError,
    InvalidStockNamesError,
    MissingWeightsError,
    NonNumericWeightsError,
    NegativeWeightsError,
    WeightsExceedOneError,
    IncorrectWeightSumError
)


def validate_and_read_etf_csv(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise ETFFileNotFoundError(file_path)
    except UnicodeDecodeError:
        raise FileEncodingError()
    except pd.errors.ParserError as e:
        raise InvalidCSVFormatError(str(e))
    except Exception as e:
        raise InvalidCSVFormatError(str(e))

    # Check if DataFrame is empty
    if df.empty:
        raise EmptyFileError()

    # Check for required columns
    required_columns = ['name', 'weight']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise MissingColumnsError(missing_columns, df.columns.tolist())

    # Check if there are any rows
    if len(df) == 0:
        raise NoDataRowsError()

    # Validate 'name' column - should contain valid stock symbols
    if df['name'].isna().any():
        empty_rows = df[df['name'].isna()].index.tolist()
        raise MissingStockNamesError(empty_rows)

    # Check if all names are strings
    if not all(isinstance(name, str) for name in df['name']):
        raise InvalidStockNamesError()

    # Validate 'weight' column - should be numeric
    if df['weight'].isna().any():
        empty_rows = df[df['weight'].isna()].index.tolist()
        raise MissingWeightsError(empty_rows)

    # Try to convert weight to numeric
    try:
        weights = pd.to_numeric(df['weight'])
    except (ValueError, TypeError):
        non_numeric = df[pd.to_numeric(df['weight'], errors='coerce').isna()]['weight'].tolist()[:3]
        raise NonNumericWeightsError(non_numeric)

    # Check if weights are in valid range (0-1)
    if (weights < 0).any():
        negative_weights = df[weights < 0]['name'].tolist()[:3]
        raise NegativeWeightsError(negative_weights)

    # we can also normalize the weight so the sum be 1, but we are not doing that for now
    if (weights > 1).any():
        over_weights = df[weights > 1]['name'].tolist()[:3]
        raise WeightsExceedOneError(over_weights)

    # Check if weights sum to approximately 1.0 (allowing some tolerance)
    weight_sum = weights.sum()
    if not (0.95 <= weight_sum <= 1.05):
        raise IncorrectWeightSumError(weight_sum)

    return df
