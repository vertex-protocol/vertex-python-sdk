from vertex_protocol.engine_client.types.execute import (
    BurnLpParams,
    BurnLpRequest,
    to_execute_request,
)
from vertex_protocol.utils.bytes32 import hex_to_bytes32


def test_burn_lp_params(senders: list[str], owners: list[str], burn_lp_params: dict):
    sender = senders[0]
    product_id = burn_lp_params["productId"]
    amount = burn_lp_params["amount"]
    params_from_dict = BurnLpParams(
        **{"sender": sender, "productId": product_id, "amount": amount}
    )
    params_from_obj = BurnLpParams(
        sender=sender,
        productId=product_id,
        amount=amount,
    )
    bytes32_sender = BurnLpParams(
        sender=hex_to_bytes32(sender), productId=product_id, amount=amount
    )
    subaccount_params_sender = BurnLpParams(
        sender={"subaccount_owner": owners[0], "subaccount_name": "default"},
        productId=product_id,
        amount=amount,
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
    req_from_params = BurnLpRequest(burn_lp=params_from_dict)
    assert req_from_params == to_execute_request(params_from_dict)
    assert req_from_params.dict() == {
        "burn_lp": {
            "tx": {
                "sender": sender.lower(),
                "productId": product_id,
                "amount": str(amount),
                "nonce": str(params_from_dict.nonce),
            },
            "signature": params_from_dict.signature,
        }
    }
