from enum import Enum
from types import FunctionType
from pydantic import BaseModel


class VertexBaseModel(BaseModel):
    """
    This base model extends Pydantic's BaseModel and excludes fields with None
    values by default when serializing via .dict() or .json()
    """

    def dict(self, **kwargs):
        """
        Convert model to dictionary, excluding None fields by default.

        Args:
            kwargs: Arbitrary keyword arguments.

        Returns:
            dict: The model as a dictionary.
        """
        kwargs.setdefault("exclude_none", True)
        return super().dict(**kwargs)

    def json(self, **kwargs):
        """
        Convert model to JSON, excluding None fields by default.

        Args:
            kwargs: Arbitrary keyword arguments.

        Returns:
            str: The model as a JSON string.
        """
        kwargs.setdefault("exclude_none", True)
        return super().json(**kwargs)

    def serialize_dict(self, fields: list[str], func: FunctionType):
        """
        Apply a function to specified fields in the model's dictionary.

        Args:
            fields (list[str]): Fields to be modified.
            func (FunctionType): Function to apply to each field.
        """
        for field in fields:
            self.__dict__[field] = func(self.__dict__[field])


def to_enum(value: str | Enum) -> Enum:
    """
    Utility function that ensures value is an Enum.

    Args:
        value (str | Enum): Value to be converted into an Enum.

    Returns:
        Enum: The converted Enum value.
    """
    if isinstance(value, Enum):
        return value.value
    else:
        return value
