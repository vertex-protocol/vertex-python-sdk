from copy import deepcopy
from types import FunctionType
from pydantic import BaseModel


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
