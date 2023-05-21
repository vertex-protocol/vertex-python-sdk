from eth_account import Account
from eth_account.signers.local import LocalAccount
from typing import Optional
from pydantic import BaseModel, AnyUrl, validator, root_validator

PrivateKey = str
Signer = LocalAccount | PrivateKey


class EngineClientOpts(BaseModel):
    """
    Model representing the options for Engine Client
    """

    url: AnyUrl
    signer: Optional[Signer] = None
    linked_signer: Optional[Signer] = None
    chain_id: Optional[int] = None
    endpoint_addr: Optional[str] = None
    book_addrs: Optional[list[str]] = None

    class Config:
        arbitrary_types_allowed = True

    @root_validator
    def check_linked_signer(cls, values: dict):
        signer, linked_signer = values.get("signer"), values.get("linked_signer")
        if linked_signer and not signer:
            raise ValueError("linked_signer cannot be set if signer is not set")
        return values

    @validator("signer")
    def signer_to_local_account(cls, v: Optional[Signer]) -> Optional[LocalAccount]:
        if v is None or isinstance(v, LocalAccount):
            return v
        return Account.from_key(v)

    @validator("linked_signer")
    def linked_signer_to_local_account(
        cls, v: Optional[Signer]
    ) -> Optional[LocalAccount]:
        if v is None or isinstance(v, LocalAccount):
            return v
        return Account.from_key(v)
