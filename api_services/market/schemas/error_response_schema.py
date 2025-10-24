from dataclasses import dataclass
from marshmallow import Schema, fields, post_load


# DTOs
@dataclass
class ErrorDetailsDTO:
    code: str
    message: str


@dataclass
class ErrorResponseDTO:
    error: ErrorDetailsDTO


# Schemas
class ErrorDetailsSchema(Schema):
    code = fields.Str(required=True)
    message = fields.Str(required=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return ErrorDetailsDTO(**data)


class ErrorResponseSchema(Schema):
    error = fields.Nested(ErrorDetailsSchema, required=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return ErrorResponseDTO(**data)
