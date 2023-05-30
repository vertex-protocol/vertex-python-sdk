from web3 import Web3

rpc_node = "https://goerli-rollup.arbitrum.io/rpc"


def run():
    print("setting up contracts client...")
    w3 = Web3(Web3.HTTPProvider(rpc_node))

    print("hi", w3.eth.chain_id)
