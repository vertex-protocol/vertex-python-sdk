import os
from typing import Optional
from pydantic import BaseModel
from web3 import Web3
from web3.types import TxParams
from web3.contract import Contract
from web3.contract.contract import ContractFunction
from eth_account.signers.local import LocalAccount
from vertex_protocol.contracts.loader import load_abi
from vertex_protocol.contracts.types import DepositCollateralParams, VertexAbiName
from vertex_protocol.utils.bytes32 import (
    hex_to_bytes32,
    str_to_hex,
    subaccount_name_to_bytes12,
    zero_address,
)
from vertex_protocol.utils.exceptions import InvalidProductId
from vertex_protocol.contracts.types import *


class VertexContractsContext(BaseModel):
    """
    Holds the context for various Vertex contracts.

    Attributes:
        endpoint_addr (str): The endpoint address.

        querier_addr (str): The querier address.

        spot_engine_addr (Optional[str]): The spot engine address. This may be None.

        perp_engine_addr (Optional[str]): The perp engine address. This may be None.

        clearinghouse_addr (Optional[str]): The clearinghouse address. This may be None.
    """

    endpoint_addr: str
    querier_addr: str
    spot_engine_addr: Optional[str]
    perp_engine_addr: Optional[str]
    clearinghouse_addr: Optional[str]


class VertexContracts:
    """
    Encapsulates the set of Vertex contracts required for querying and executing.
    """

    w3: Web3
    contracts_context: VertexContractsContext
    querier: Contract
    endpoint: Contract
    clearinghouse: Optional[Contract]
    spot_engine: Optional[Contract]
    perp_engine: Optional[Contract]

    def __init__(self, node_url: str, contracts_context: VertexContractsContext):
        """
        Initialize a VertexContracts instance.

        This will set up the Web3 instance and contract addresses for querying and executing the Vertex contracts.
        It will also load and parse the ABI for the given contracts.

        Args:
            node_url (str): The Ethereum node URL.

            contracts_context (VertexContractsContext): The Vertex contracts context, holding the relevant addresses.
        """
        self.w3 = Web3(Web3.HTTPProvider(node_url))

        self.contracts_context = VertexContractsContext.parse_obj(contracts_context)
        self.querier: Contract = self.w3.eth.contract(
            address=contracts_context.querier_addr, abi=load_abi(VertexAbiName.FQUERIER)  # type: ignore
        )
        self.endpoint: Contract = self.w3.eth.contract(
            address=self.contracts_context.endpoint_addr,
            abi=load_abi(VertexAbiName.ENDPOINT),  # type: ignore
        )
        self.clearinghouse = None
        self.spot_engine = None
        self.perp_engine = None

        if self.contracts_context.clearinghouse_addr:
            self.clearinghouse: Contract = self.w3.eth.contract(
                address=self.contracts_context.clearinghouse_addr,
                abi=load_abi(VertexAbiName.ICLEARINGHOUSE),  # type: ignore
            )

        if self.contracts_context.spot_engine_addr:
            self.spot_engine: Contract = self.w3.eth.contract(
                address=self.contracts_context.spot_engine_addr,
                abi=load_abi(VertexAbiName.ISPOT_ENGINE),  # type: ignore
            )

        if self.contracts_context.perp_engine_addr:
            self.perp_engine: Contract = self.w3.eth.contract(
                address=self.contracts_context.perp_engine_addr,
                abi=load_abi(VertexAbiName.IPERP_ENGINE),  # type: ignore
            )

    def deposit_collateral(
        self, params: DepositCollateralParams, signer: LocalAccount
    ) -> str:
        """
        Deposits a specified amount of collateral into a spot product.

        Args:
            params (DepositCollateralParams): The parameters for depositing collateral.

            signer (LocalAccount): The account that will sign the deposit transaction.

        Returns:
            str: The transaction hash of the deposit operation.
        """
        params = DepositCollateralParams.parse_obj(params)
        if params.referral_code is not None and params.referral_code.strip():
            return self.execute(
                self.endpoint.functions.depositCollateralWithReferral(
                    subaccount_name_to_bytes12(params.subaccount_name),
                    params.product_id,
                    params.amount,
                    params.referral_code,
                ),
                signer,
            )
        else:
            return self.execute(
                self.endpoint.functions.depositCollateral(
                    subaccount_name_to_bytes12(params.subaccount_name),
                    params.product_id,
                    params.amount,
                ),
                signer,
            )

    def approve_allowance(self, erc20: Contract, amount: int, signer: LocalAccount):
        """
        Approves a specified amount of allowance for the ERC20 token contract.

        Args:
            erc20 (Contract): The ERC20 token contract.

            amount (int): The amount of the ERC20 token to be approved.

            signer (LocalAccount): The account that will sign the approval transaction.

        Returns:
            str: The transaction hash of the approval operation.
        """
        return self.execute(
            erc20.functions.approve(self.endpoint.address, amount), signer
        )

    def _mint_mock_erc20(
        self, erc20: Contract, amount: int, signer: LocalAccount
    ) -> str:
        """
        Mints a specified amount of mock ERC20 tokens for testing purposes.

        Args:
            erc20 (Contract): The contract instance of the ERC20 token to be minted.

            amount (int): The amount of tokens to mint.

            signer (LocalAccount): The account that will sign the minting transaction.

        Returns:
            str: The transaction hash of the mint operation.
        """
        return self.execute(erc20.functions.mint(signer.address, amount), signer)

    def get_token_contract_for_product(self, product_id: int) -> Contract:
        """
        Returns the ERC20 token contract for a given product.

        Args:
            product_id (int): The ID of the product for which to get the ERC20 token contract.

        Returns:
            Contract: The ERC20 token contract for the specified product.

        Raises:
            InvalidProductId: If the provided product ID is not valid.
        """
        if self.spot_engine is None:
            raise Exception("SpotEngine contract not initialized")
        product_config = self.spot_engine.functions.getConfig(product_id).call()
        token = product_config[0]
        if token == f"0x{zero_address().hex()}":
            raise InvalidProductId(f"Invalid product id provided: {product_id}")
        return self.w3.eth.contract(
            address=token,
            abi=load_abi(VertexAbiName.MOCK_ERC20),
        )

    def execute(self, func: ContractFunction, signer: LocalAccount) -> str:
        """
        Executes a smart contract function.

        This method builds a transaction for a given contract function, signs the transaction with the provided signer's private key,
        sends the raw signed transaction to the network, and waits for the transaction to be mined.

        Args:
            func (ContractFunction): The contract function to be executed.

            signer (LocalAccount): The local account object that will sign the transaction. It should contain the private key.

        Returns:
            str: The hexadecimal representation of the transaction hash.

        Raises:
            ValueError: If the transaction is invalid, the method will not catch the error.
            TimeExhausted: If the transaction receipt isn't available within the timeout limit set by the Web3 provider.
        """
        tx = func.build_transaction(self._build_tx_params(signer))
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=signer.key)
        signed_tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(signed_tx_hash)
        return signed_tx_hash.hex()

    def _build_tx_params(self, signer: LocalAccount) -> TxParams:
        tx_params: TxParams = {
            "from": signer.address,
            "nonce": self.w3.eth.get_transaction_count(signer.address),
        }
        if os.getenv("CLIENT_MODE") == "devnet":
            tx_params["gasPrice"] = self.w3.eth.gas_price
        return tx_params


__all__ = [
    "VertexContractsContext",
    "VertexContracts",
    "DepositCollateralParams",
    "VertexExecuteType",
    "VertexNetwork",
    "VertexAbiName",
    "VertexDeployment",
]
