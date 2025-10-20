import os
import tempfile

from flask import Flask, jsonify, request
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics

from config import DEFAULT_TOP_HOLDINGS_COUNT
from exceptions import (
    ETFValidationError,
    UnexpectedError,
    NoFileProvidedError,
    NoFileSelectedError,
    InvalidFileTypeError
)
from logger import app_logger
from schemas import ETFUploadResponseSchema, ErrorResponseSchema
from services.etf_service import calculate_etf_data
from validator import validate_and_read_etf_csv

app = Flask(__name__)

# Initialize Prometheus metrics before CORS
metrics = PrometheusMetrics(app)
# Add custom info metric
metrics.info('app_info', 'Application info', version='1.0.0', app_name='BMO ETF Backend')

CORS(app)


@app.route('/test')
def test():
    return jsonify({"message": "Welcome to the API"})


@app.route('/api/etf/upload', methods=['POST'])
def upload_etf_csv():
    tmp_file_path = None
    try:
        top_holdings_count = request.args.get('top_holdings_count', DEFAULT_TOP_HOLDINGS_COUNT, type=int)
        app_logger.info("ETF CSV upload request received")

        if 'file' not in request.files:
            raise NoFileProvidedError()

        file = request.files['file']

        if file.filename == '':
            raise NoFileSelectedError()

        if not file.filename.endswith('.csv'):
            raise InvalidFileTypeError(file.filename)

        app_logger.info(f"Processing file: {file.filename}")

        with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as tmp_file:
            file.save(tmp_file.name)
            tmp_file_path = tmp_file.name

        etf = validate_and_read_etf_csv(tmp_file_path)
        app_logger.info(f"CSV validation successful for {file.filename}")
        constituents, top_holdings, etf_prices = calculate_etf_data(etf, top_holdings_count)

        response_schema = ETFUploadResponseSchema(
            constituents=constituents,
            top_holdings=top_holdings,
            etf_prices=etf_prices
        )

        app_logger.info(f"Successfully processed ETF CSV: {file.filename}")
        return jsonify(response_schema.model_dump()), 200

    except ETFValidationError as e:
        # Log the validation error based on status code
        # this could be an interceptor in larger applications to apply on all APIs
        # in the interceptor there can be implementation for email alerts for critical errors or general error monitoring system integration
        if e.status_code >= 500:
            app_logger.error(e.get_log_message(), exc_info=True)
        elif e.status_code >= 400:
            app_logger.warning(e.get_log_message())
        else:
            app_logger.info(e.get_log_message())

        # Serialize error response using Pydantic
        error_schema = ErrorResponseSchema(
            error=e.message,
            error_code=e.error_code,
            error_detail=e.error_detail
        )
        return jsonify(error_schema.model_dump(exclude_none=True)), e.status_code

    except Exception as e:
        unexpected_error = UnexpectedError(str(e))
        app_logger.error(unexpected_error.get_log_message(), exc_info=True)

        # Serialize error response using Pydantic
        error_schema = ErrorResponseSchema(
            error=unexpected_error.message,
            error_code=unexpected_error.error_code,
            error_detail=unexpected_error.error_detail
        )
        return jsonify(error_schema.model_dump(exclude_none=True)), unexpected_error.status_code

    finally:
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)  # Clean up temporary file
            app_logger.debug(f"Cleaned up temporary file: {tmp_file_path}")


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    # Disable reloader to ensure Prometheus metrics endpoint works correctly
    app.run(debug=True, port=port, use_reloader=False)
