class ETFValidationError(Exception):

    def __init__(self, message, error_code=None, status_code=None, error_detail=None):
        self.message = message
        self.error_code = error_code or 1004
        self.error_detail = error_detail
        self.status_code = status_code or 400
        super().__init__(self.message)

    def to_dict(self):
        result = {
            "error": self.message,
            "error_code": self.error_code
        }
        if self.error_detail:
            result["error_detail"] = self.error_detail
        return result

    def get_log_message(self):
        log_message = f"[{self.error_code}] {self.message}"
        if self.error_detail:
            log_message += f" | Details: {self.error_detail}"
        return log_message

    def __str__(self):
        return self.message


class FileProcessingError(ETFValidationError):

    def __init__(self, details):
        message = f"There was a problem processing the file."
        super().__init__(message, status_code=400, error_code=1004, error_detail=details)


class ETFFileNotFoundError(ETFValidationError):

    def __init__(self, file_path):
        message = "There was a problem. Please inform the service maintainer"
        super().__init__(message, status_code=400, error_code=2001, error_detail="ETF file not found")


class FileEncodingError(FileProcessingError):

    def __init__(self):
        message = "The file cannot be read. Please ensure it's a valid text file encoded in UTF-8."
        super().__init__(message)


class InvalidCSVFormatError(FileProcessingError):

    def __init__(self, details):
        message = f"The file is not a valid CSV format. Please check that it has proper comma-separated values. Details: {details}"
        super().__init__(message)


class EmptyFileError(FileProcessingError):

    def __init__(self):
        message = "The CSV file appears to be empty. Please provide a file with ETF constituent data."
        super().__init__(message)


class MissingColumnsError(FileProcessingError):

    def __init__(self, missing_columns, available_columns):
        available_cols = ', '.join(available_columns)
        message = f"Your CSV is missing required columns: {', '.join(missing_columns)}. Found columns: {available_cols}. Please ensure your CSV has 'name' and 'weight' columns."
        super().__init__(message)


class NoDataRowsError(FileProcessingError):

    def __init__(self):
        message = "The CSV file has headers but no data rows. Please add ETF constituent information."
        super().__init__(message)


class MissingStockNamesError(FileProcessingError):

    def __init__(self, empty_rows):
        row_nums = ', '.join([str(i + 2) for i in empty_rows[:5]])
        message = f"Some stock names are missing. Please check rows: {row_nums}. Every ETF constituent must have a name."
        super().__init__(message)


class InvalidStockNamesError(FileProcessingError):

    def __init__(self):
        message = "All stock names must be text values (e.g., 'A', 'AAPL', 'MSFT'). Please check your 'name' column."
        super().__init__(message)


class MissingWeightsError(FileProcessingError):

    def __init__(self, empty_rows):
        row_nums = ', '.join([str(i + 2) for i in empty_rows[:5]])
        message = f"Some weights are missing. Please check rows: {row_nums}. Every constituent must have a weight value."
        super().__init__(message)


class NonNumericWeightsError(FileProcessingError):

    def __init__(self, non_numeric_values):
        message = f"Weight values must be numbers (e.g., 0.15, 0.25). Found invalid values: {', '.join(map(str, non_numeric_values))}. Please use decimal format."
        super().__init__(message)


class NegativeWeightsError(FileProcessingError):

    def __init__(self, negative_weight_stocks):
        message = f"Weight values cannot be negative. Found negative weights for: {', '.join(negative_weight_stocks)}. Weights must be between 0 and 1."
        super().__init__(message)


class WeightsExceedOneError(FileProcessingError):

    def __init__(self, over_weight_stocks):
        message = f"Weight values cannot exceed 1.0. Found weights greater than 1 for: {', '.join(over_weight_stocks)}. Please use decimal format (e.g., 0.25 for 25%)."
        super().__init__(message)


class IncorrectWeightSumError(FileProcessingError):

    def __init__(self, weight_sum):
        percentage = weight_sum * 100
        message = f"The total weights sum to {weight_sum:.4f} ({percentage:.2f}%), but should sum to approximately 1.0 (100%). Please verify your weight allocations."
        super().__init__(message)


class UnexpectedError(ETFValidationError):

    def __init__(self, details):
        message = f"An unexpected error occurred while processing your file. Please try again or contact support. Details: {details}"
        super().__init__(message, error_code=5000, status_code=500)


class NoFileProvidedError(ETFValidationError):

    def __init__(self):
        message = "No file provided. Please select a file to upload."
        super().__init__(message, error_code=1001, status_code=400)


class NoFileSelectedError(ETFValidationError):

    def __init__(self):
        message = "No file selected. Please choose a CSV file to upload."
        super().__init__(message, error_code=1002, status_code=400)


class InvalidFileTypeError(ETFValidationError):

    def __init__(self, filename):
        message = f"Invalid file type. Expected a CSV file but received '{filename}'. Please upload a .csv file."
        super().__init__(message, error_code=1003, status_code=400)


class StockPriceNotFoundError(ETFValidationError):

    def __init__(self, stock):
        message = f"Price data for stock '{stock}' not found."
        super().__init__(message, status_code=400, error_code=3001)
