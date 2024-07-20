import math as Math

def getBalance(web3, address):
	return web3.from_wei(web3.eth.get_balance(address),'ether')
	
def getNonce(web3, address):
	return web3.eth.get_transaction_count(address)

def getDecimals(web3):
	return 18 #BNB has 18 decimal places.

def multiplyToInt(web3,amount):
	return int(amount*Math.pow(10,getDecimals(web3)))

def getDecimalsPow(web3):
	return int(1*Math.pow(10,getDecimals(web3)))
