from .query import *
from .execute import *
from eth_account.signers.local import LocalAccount
from typing import Optional
from pydantic import BaseModel


class EngineClientOpts(BaseModel):
    """
    Model representing the options for Engine Client
    """

    url: str
    signer: Optional[LocalAccount] = None
    linked_signer: Optional[LocalAccount] = None
    chain_id: Optional[str] = None
    endpoint_addr: Optional[str] = None
    book_addrs: Optional[list[str]] = None

    class Config:
        arbitrary_types_allowed = True
