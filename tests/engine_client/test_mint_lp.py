from vertex_protocol.engine_client.types.execute import (
    MintLpParams,
    MintLpRequest,
    to_execute_request,
)
from vertex_protocol.utils.bytes32 import hex_to_bytes32


def test_mint_lp_params(senders: list[str], owners: list[str], mint_lp_params: dict):
    sender = senders[0]
    product_id = mint_lp_params["productId"]
    amount_base = mint_lp_params["amountBase"]
    quote_amount_low = mint_lp_params["quoteAmountLow"]
    quote_amount_high = mint_lp_params["quoteAmountHigh"]
    params_from_dict = MintLpParams(
        **{
            "sender": sender,
            "productId": product_id,
            "amountBase": amount_base,
            "quoteAmountLow": quote_amount_low,
            "quoteAmountHigh": quote_amount_high,
        }
    )
    params_from_obj = MintLpParams(
        sender=sender,
        productId=mint_lp_params["productId"],
        amountBase=amount_base,
        quoteAmountLow=quote_amount_low,
        quoteAmountHigh=quote_amount_high,
    )
    bytes32_sender = MintLpParams(
        sender=hex_to_bytes32(sender),
        productId=product_id,
        amountBase=amount_base,
        quoteAmountLow=quote_amount_low,
        quoteAmountHigh=quote_amount_high,
    )
    subaccount_params_sender = MintLpParams(
        sender={"subaccount_owner": owners[0], "subaccount_name": "default"},
        productId=product_id,
        amountBase=amount_base,
        quoteAmountLow=quote_amount_low,
        quoteAmountHigh=quote_amount_high,
    )

    assert (
        params_from_dict
        == params_from_obj
        == bytes32_sender
        == subaccount_params_sender
    )
    params_from_dict.signature = (
        "0x51ba8762bc5f77957a4e896dba34e17b553b872c618ffb83dba54878796f2821"
    )
    params_from_dict.nonce = 100000
    req_from_params = MintLpRequest(mint_lp=params_from_dict)
    assert req_from_params == to_execute_request(params_from_dict)
    assert req_from_params.dict() == {
        "mint_lp": {
            "tx": {
                "sender": sender.lower(),
                "productId": product_id,
                "amountBase": str(amount_base),
                "quoteAmountLow": str(quote_amount_low),
                "quoteAmountHigh": str(quote_amount_high),
                "nonce": str(params_from_dict.nonce),
            },
            "signature": params_from_dict.signature,
        }
    }
