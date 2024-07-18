import constant as c

def getBalance(web3,address):
	contract = web3.eth.contract(address=web3.to_checksum_address(c.qfsAddress), abi=c.qfsAbi)
	balance=contract.functions.balanceOf(web3.to_checksum_address(address)).call()
	readableBalance=web3.from_wei(balance,'ether')
	return readableBalance

