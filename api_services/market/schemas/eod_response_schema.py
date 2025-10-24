from dataclasses import dataclass
from datetime import datetime
from marshmallow import Schema, fields, post_load, RAISE
from api_services.market.schemas.common_schemas import PaginationSchema, PaginationDTO


# Data Transfer Objects (DTOs)
@dataclass
class EodDataDTO:
    """DTO for individual EOD data records."""
    open: float
    high: float
    low: float
    close: float
    volume: float
    adj_high: float | None
    adj_low: float | None
    adj_close: float
    adj_open: float
    adj_volume: float | None
    split_factor: float
    dividend: float
    name: str | None
    exchange_code: str | None
    asset_type: str | None
    price_currency: str | None
    symbol: str
    exchange: str
    date: datetime


@dataclass
class EodResponseDTO:
    """DTO for the entire /eod endpoint response."""
    pagination: PaginationDTO
    data: list[EodDataDTO]


# Marshmallow Schemas for validation and deserialization
class EodDataSchema(Schema):
    """Schema for individual EOD data objects in the 'data' list."""
    class Meta:
        unknown = RAISE

    open = fields.Float(required=True)
    high = fields.Float(required=True)
    low = fields.Float(required=True)
    close = fields.Float(required=True)
    volume = fields.Float(required=True)
    adj_high = fields.Float(required=True, allow_none=True)
    adj_low = fields.Float(required=True, allow_none=True)
    adj_close = fields.Float(required=True)
    adj_open = fields.Float(required=True)
    adj_volume = fields.Float(required=True, allow_none=True)
    split_factor = fields.Float(required=True)
    dividend = fields.Float(required=True)
    name = fields.Str(required=True, allow_none=True)
    exchange_code = fields.Str(required=True, allow_none=True)
    asset_type = fields.Str(required=True, allow_none=True)
    price_currency = fields.Str(required=True, allow_none=True)
    symbol = fields.Str(required=True)
    exchange = fields.Str(required=True)
    date = fields.DateTime(required=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return EodDataDTO(**data)


class EodResponseSchema(Schema):
    """Schema for the entire /eod endpoint response."""
    class Meta:
        unknown = RAISE

    pagination = fields.Nested(PaginationSchema, required=True)
    data = fields.List(fields.Nested(EodDataSchema), required=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return EodResponseDTO(**data)
