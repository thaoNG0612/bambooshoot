def getBalance(web3, address):
	return web3.from_wei(web3.eth.get_balance(address),'ether')
	

def getNonce(web3, address):
	return web3.eth.get_transaction_count(address)