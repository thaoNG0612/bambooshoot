import constant as c
from web3 import Web3
from web3.middleware import geth_poa_middleware

def connectBSC():
    web3 = Web3(Web3.HTTPProvider(c.bsc))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    print("Connected to BSC blockchain: {}".format(web3.is_connected()))
    return web3