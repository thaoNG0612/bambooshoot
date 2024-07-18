import constant as c
from web3 import Web3

def connectBSC():
	web3 = Web3(Web3.HTTPProvider(c.bsc))
	print("Connected to BSC blockchain: {}".format(web3.is_connected()))
	return web3