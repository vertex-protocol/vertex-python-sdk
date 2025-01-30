from vertex_protocol.utils.enum import StrEnum
from eth_account import Account
from eth_account.signers.local import LocalAccount
from typing import Optional, Union
from pydantic import BaseModel, AnyUrl, validator, root_validator


class VertexBackendURL(StrEnum):
    """Enum representing different Vertex backend URLs."""

    # mainnet
    MAINNET_GATEWAY = "https://gateway.prod.vertexprotocol.com/v1"
    MAINNET_INDEXER = "https://archive.prod.vertexprotocol.com/v1"
    MAINNET_TRIGGER = "https://trigger.prod.vertexprotocol.com/v1"

    BLAST_MAINNET_GATEWAY = "https://gateway.blast-prod.vertexprotocol.com/v1"
    BLAST_MAINNET_INDEXER = "https://archive.blast-prod.vertexprotocol.com/v1"
    BLAST_MAINNET_TRIGGER = "https://trigger.blast-prod.vertexprotocol.com/v1"

    MANTLE_MAINNET_GATEWAY = "https://gateway.mantle-prod.vertexprotocol.com/v1"
    MANTLE_MAINNET_INDEXER = "https://archive.mantle-prod.vertexprotocol.com/v1"
    MANTLE_MAINNET_TRIGGER = "https://trigger.mantle-prod.vertexprotocol.com/v1"

    SEI_MAINNET_GATEWAY = "https://gateway.sei-prod.vertexprotocol.com/v1"
    SEI_MAINNET_INDEXER = "https://archive.sei-prod.vertexprotocol.com/v1"
    SEI_MAINNET_TRIGGER = "https://trigger.sei-prod.vertexprotocol.com/v1"

    BASE_MAINNET_GATEWAY = "https://gateway.base-prod.vertexprotocol.com/v1"
    BASE_MAINNET_INDEXER = "https://archive.base-prod.vertexprotocol.com/v1"
    BASE_MAINNET_TRIGGER = "https://trigger.base-prod.vertexprotocol.com/v1"

    SONIC_MAINNET_GATEWAY = "https://gateway.sonic-prod.vertexprotocol.com/v1"
    SONIC_MAINNET_INDEXER = "https://archive.sonic-prod.vertexprotocol.com/v1"
    SONIC_MAINNET_TRIGGER = "https://trigger.sonic-prod.vertexprotocol.com/v1"

    ABSTRACT_MAINNET_GATEWAY = "https://gateway.abstract-prod.vertexprotocol.com/v1"
    ABSTRACT_MAINNET_INDEXER = "https://archive.abstract-prod.vertexprotocol.com/v1"
    ABSTRACT_MAINNET_TRIGGER = "https://trigger.abstract-prod.vertexprotocol.com/v1"

    # testnet
    SEPOLIA_TESTNET_GATEWAY = "https://gateway.sepolia-test.vertexprotocol.com/v1"
    SEPOLIA_TESTNET_INDEXER = "https://archive.sepolia-test.vertexprotocol.com/v1"
    SEPOLIA_TESTNET_TRIGGER = "https://trigger.sepolia-test.vertexprotocol.com/v1"

    BLAST_TESTNET_GATEWAY = "https://gateway.blast-test.vertexprotocol.com/v1"
    BLAST_TESTNET_INDEXER = "https://archive.blast-test.vertexprotocol.com/v1"
    BLAST_TESTNET_TRIGGER = "https://trigger.blast-test.vertexprotocol.com/v1"

    MANTLE_TESTNET_GATEWAY = "https://gateway.mantle-test.vertexprotocol.com/v1"
    MANTLE_TESTNET_INDEXER = "https://archive.mantle-test.vertexprotocol.com/v1"
    MANTLE_TESTNET_TRIGGER = "https://trigger.mantle-test.vertexprotocol.com/v1"

    SEI_TESTNET_GATEWAY = "https://gateway.sei-test.vertexprotocol.com/v1"
    SEI_TESTNET_INDEXER = "https://archive.sei-test.vertexprotocol.com/v1"
    SEI_TESTNET_TRIGGER = "https://trigger.sei-test.vertexprotocol.com/v1"

    BASE_TESTNET_GATEWAY = "https://gateway.base-test.vertexprotocol.com/v1"
    BASE_TESTNET_INDEXER = "https://archive.base-test.vertexprotocol.com/v1"
    BASE_TESTNET_TRIGGER = "https://trigger.base-test.vertexprotocol.com/v1"

    SONIC_TESTNET_GATEWAY = "https://gateway.sonic-test.vertexprotocol.com/v1"
    SONIC_TESTNET_INDEXER = "https://archive.sonic-test.vertexprotocol.com/v1"
    SONIC_TESTNET_TRIGGER = "https://trigger.sonic-test.vertexprotocol.com/v1"

    ABSTRACT_TESTNET_GATEWAY = "https://gateway.abstract-test.vertexprotocol.com/v1"
    ABSTRACT_TESTNET_INDEXER = "https://archive.abstract-test.vertexprotocol.com/v1"
    ABSTRACT_TESTNET_TRIGGER = "https://trigger.abstract-test.vertexprotocol.com/v1"

    # dev
    DEVNET_GATEWAY = "http://localhost:80"
    DEVNET_INDEXER = "http://localhost:8000"
    DEVNET_TRIGGER = "http://localhost:8080"


PrivateKey = str
Signer = Union[LocalAccount, PrivateKey]


class VertexClientOpts(BaseModel):
    """
    Model defining the configuration options for execute Vertex Clients (e.g: Engine, Trigger). It includes various parameters such as the URL,
    the signer, the linked signer, the chain ID, and others.

    Attributes:
        url (AnyUrl): The URL of the server.
        signer (Optional[Signer]): The signer for the client, if any. It can either be a `LocalAccount` or a private key.
        linked_signer (Optional[Signer]): An optional signer linked the main subaccount to perform executes on it's behalf.
        chain_id (Optional[int]): An optional network chain ID.
        endpoint_addr (Optional[str]): Vertex's endpoint address used for verifying executes.
        book_addrs (Optional[list[str]]): Vertex's book addresses used for verifying order placement.

    Notes:
        - The class also includes several methods for validating and sanitizing the input values.
        - "linked_signer" cannot be set if "signer" is not set.
    """

    url: AnyUrl
    signer: Optional[Union[LocalAccount, PrivateKey]] = None
    linked_signer: Optional[Signer] = None
    chain_id: Optional[int] = None
    endpoint_addr: Optional[str] = None
    book_addrs: Optional[list[str]] = None

    class Config:
        arbitrary_types_allowed = True

    @root_validator
    def check_linked_signer(cls, values: dict):
        """
        Validates that if a linked_signer is set, a signer must also be set.

        Args:
            values (dict): The input values to be validated.

        Raises:
            ValueError: If linked_signer is set but signer is not.

        Returns:
            dict: The validated values.
        """
        signer, linked_signer = values.get("signer"), values.get("linked_signer")
        if linked_signer and not signer:
            raise ValueError("linked_signer cannot be set if signer is not set")
        return values

    @validator("url")
    def clean_url(cls, v: AnyUrl) -> str:
        """
        Cleans the URL input by removing trailing slashes.

        Args:
            v (AnyUrl): The input URL.

        Returns:
            str: The cleaned URL.
        """
        return v.rstrip("/")

    @validator("signer")
    def signer_to_local_account(cls, v: Optional[Signer]) -> Optional[LocalAccount]:
        """
        Validates and converts the signer to a LocalAccount instance.

        Args:
            v (Optional[Signer]): The signer instance or None.

        Returns:
            Optional[LocalAccount]: The LocalAccount instance or None.
        """
        if v is None or isinstance(v, LocalAccount):
            return v
        return Account.from_key(v)

    @validator("linked_signer")
    def linked_signer_to_local_account(
        cls, v: Optional[Signer]
    ) -> Optional[LocalAccount]:
        """
        Validates and converts the linked_signer to a LocalAccount instance.

        Args:
            v (Optional[Signer]): The linked_signer instance or None.

        Returns:
            Optional[LocalAccount]: The LocalAccount instance or None.
        """
        if v is None or isinstance(v, LocalAccount):
            return v
        return Account.from_key(v)
