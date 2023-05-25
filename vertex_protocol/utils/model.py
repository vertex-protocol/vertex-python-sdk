from pydantic import BaseModel


class VertexBaseModel(BaseModel):
    def dict(self, **kwargs):
        kwargs.setdefault("exclude_none", True)
        return super().dict(**kwargs)

    def json(self, **kwargs):
        kwargs.setdefault("exclude_none", True)
        return super().json(**kwargs)
