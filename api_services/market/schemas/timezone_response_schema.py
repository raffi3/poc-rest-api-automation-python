from dataclasses import dataclass
from marshmallow import Schema, fields, post_load
from api_services.market.schemas.common_schemas import PaginationSchema, PaginationDTO


# DTOs
@dataclass
class TimezoneDataDTO:
    timezone: str
    abbr: str
    abbr_dst: str


@dataclass
class TimezonesResponseDTO:
    pagination: PaginationDTO
    data: list[TimezoneDataDTO]


# Schemas
class TimezoneDataSchema(Schema):
    timezone = fields.Str(required=True)
    abbr = fields.Str(required=True)
    abbr_dst = fields.Str(required=True)

    @post_load
    def deserialize(self, data, **kwargs):
        return TimezoneDataDTO(**data)


class TimezonesResponseSchema(Schema):
    pagination = fields.Nested(PaginationSchema, required=True)
    data = fields.List(fields.Nested(TimezoneDataSchema), required=True)

    @post_load
    def deserialize(self, data, **kwargs):
        return TimezonesResponseDTO(**data)
