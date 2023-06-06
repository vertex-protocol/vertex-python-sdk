from pydantic import BaseModel


class EIP712Domain(BaseModel):
    """
    Model that represents the EIP-712 Domain data structure.

    Attributes:
        name (str): The user-readable name of the signing domain, i.e., the name of the DApp or the protocol.
        version (str): The current major version of the signing domain. Signatures from different versions are not compatible.
        chainId (int): The chain ID of the originating network.
        verifyingContract (str): The address of the contract that will verify the signature.
    """

    name: str
    version: str
    chainId: int
    verifyingContract: str


class EIP712Types(BaseModel):
    """
    Util to encapsulate the EIP-712 type data structure.

    Attributes:
        EIP712Domain (list[dict]): A list of dictionaries representing EIP-712 Domain data.
    """

    EIP712Domain: list[dict]

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"


class EIP712TypedData(BaseModel):
    """
    Util to represent the EIP-712 Typed Data structure.

    Attributes:
        types (EIP712Types): EIP-712 type data.
        primaryType (str): The primary type for EIP-712 message signing.
        domain (EIP712Domain): The domain data of the EIP-712 typed message.
        message (dict): The actual data to sign.
    """

    types: EIP712Types
    primaryType: str
    domain: EIP712Domain
    message: dict
