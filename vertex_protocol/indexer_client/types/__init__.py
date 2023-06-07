from pydantic import BaseModel, AnyUrl, validator


class IndexerClientOpts(BaseModel):
    """
    Model representing the options for the Indexer Client
    """

    url: AnyUrl

    @validator("url")
    def clean_url(cls, v: AnyUrl) -> str:
        return v.rstrip("/")
