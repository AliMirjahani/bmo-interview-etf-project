# ETF Price Monitor

A full-stack application for analyzing ETF (Exchange-Traded Fund) portfolio compositions and historical price data.

## Tech Stack

### Backend (Python/Flask)

- Flask + Flask-CORS for API
- Pandas for data processing (vectorized operations)
- Pydantic for request/response validation
- Prometheus for metrics
- Multi-level logging with rotation

### Frontend (React)

- React 19 + Redux Toolkit
- AG Grid for tables
- Plotly.js for charts
- Axios for HTTP

---

## Quick Start

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py  # Runs on http://localhost:5000
```

### Frontend

```bash
cd frontend
npm install
npm start  # Runs on http://localhost:3000
```

### Tests

```bash
# Backend (27 tests)
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
pytest test/ -v
```

---



## API

### POST /api/etf/upload

**Request:**

```bash
POST /api/etf/upload?top_holdings_count=5
Content-Type: multipart/form-data

# CSV with columns: name, weight
```

**Response (200):**

```json
{
  "constituents": [
    {
      "name": "AAPL",
      "weight": 0.25,
      "price": 150.50
    }
  ],
  "top_holdings": [
    {
      "name": "AAPL",
      "holding_size": 37.625
    }
  ],
  "etf_prices": [
    {
      "date": "2024-01-15",
      "price": 125.75
    }
  ]
}
```

**Response (400/500):**

```json
{
  "error": "Invalid file format",
  "error_code": 1004,
  "error_detail": "The file is not a valid CSV format"
}
```

---
