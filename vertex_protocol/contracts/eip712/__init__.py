from pydantic import BaseModel


class EIP712Domain(BaseModel):
    name: str
    version: str
    chainId: int
    verifyingContract: str


class EIP712Types(BaseModel):
    EIP712Domain: list[dict]

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"


class EIP712TypedData(BaseModel):
    types: EIP712Types
    primaryType: str
    domain: EIP712Domain
    message: dict
