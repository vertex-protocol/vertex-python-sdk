from eth_account import Account
from eth_account.signers.local import LocalAccount
from typing import Optional
from pydantic import BaseModel, AnyUrl, validator


class IndexerClientOpts(BaseModel):
    """
    Model representing the options for the Indexer Client
    """

    url: AnyUrl

    @validator("url")
    def clean_url(cls, v: AnyUrl) -> AnyUrl:
        return v.rstrip("/")
