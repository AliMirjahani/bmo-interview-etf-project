from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List
from datetime import date


class ConstituentSchema(BaseModel):
    name: str = Field(..., description="Stock symbol/name")
    weight: float = Field(..., ge=0, le=1, description="Weight in ETF portfolio (0-1)")
    price: float = Field(..., gt=0, description="Latest stock price")


class TopHoldingSchema(BaseModel):
    name: str = Field(..., description="Stock symbol/name")
    holding_size: float = Field(..., gt=0, description="Total holding value (weight * price)")


class ETFPriceSchema(BaseModel):
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    price: float = Field(..., gt=0, description="ETF price on this date")


class ETFUploadResponseSchema(BaseModel):
    constituents: List[ConstituentSchema] = Field(..., description="List of all ETF constituents")
    top_holdings: List[TopHoldingSchema] = Field(..., description="Top N holdings by value")
    etf_prices: List[ETFPriceSchema] = Field(..., description="Historical ETF prices")


class ErrorResponseSchema(BaseModel):
    error: str = Field(..., description="Error message")
    error_code: int = Field(..., description="Application-specific error code")
    error_detail: str | None = Field(None, description="Additional error details")
