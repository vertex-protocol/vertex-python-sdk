from types import FunctionType
from typing import Type, Any, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound="VertexBaseModel")


class VertexBaseModel(BaseModel):
    def dict(self, **kwargs):
        kwargs.setdefault("exclude_none", True)
        return super().dict(**kwargs)

    def json(self, **kwargs):
        kwargs.setdefault("exclude_none", True)
        return super().json(**kwargs)

    def serialize_dict(self, fields: list[str], func: FunctionType):
        for field in fields:
            self.__dict__[field] = func(self.__dict__[field])

    @classmethod
    def to_model(cls: Type[T], obj: Any) -> T:
        if isinstance(obj, cls):
            return obj
        else:
            return cls.parse_obj(obj)
