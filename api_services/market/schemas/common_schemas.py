from dataclasses import dataclass
from marshmallow import Schema, fields, post_load

# DTO (Data Transfer Object)
@dataclass
class PaginationDTO:
    """A dataclass to hold deserialized pagination data."""
    limit: int
    offset: int
    count: int
    total: int

# Schema
class PaginationSchema(Schema):
    """Marshmallow schema to validate and deserialize pagination data."""
    limit = fields.Int(required=True)
    offset = fields.Int(required=True)
    count = fields.Int(required=True)
    total = fields.Int(required=True)

    @post_load
    def make_dto(self, data, **kwargs):
        """Converts the deserialized data dictionary into a PaginationDTO."""
        return PaginationDTO(**data)
