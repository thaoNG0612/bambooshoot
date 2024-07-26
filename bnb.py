import math as Math
import decimal
import constant as c

def getName():
	return "BNB"

def getPath(web3):
	path=[] # path = BNB > BUSD
	path.append(web3.to_checksum_address(c.wbnbAddress))
	path.append(web3.to_checksum_address(c.busdAddress))
	return path

def getBalance(web3, address):
	return web3.from_wei(web3.eth.get_balance(address),'ether')
	
def getNonce(web3, address):
	return web3.eth.get_transaction_count(address)

def getDecimals(web3):
	return 18 #BNB has 18 decimal places.

def multiplyToInt(web3,amount):
	return int(decimal.Decimal(amount)*decimal.Decimal(Math.pow(10,getDecimals(web3))))

def getDecimalsPow(web3):
	return int(1*Math.pow(10,getDecimals(web3)))
