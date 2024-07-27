import constant as c
import math as Math
import decimal

UPPER_LIMIT=0.00060 #0.0006
LOWER_LIMIT=0.00035 #0.00035
MIN_AMOUNT=1000 

def getName():
	return "QFS"

def getContract(web3):
	return web3.eth.contract(address=web3.to_checksum_address(c.qfsAddress), abi=c.qfsAbi)

def getPath(web3):
	path=[] # path = QFS > BNB > BUSD
	path.append(web3.to_checksum_address(c.qfsAddress))
	path.append(web3.to_checksum_address(c.wbnbAddress))
	path.append(web3.to_checksum_address(c.busdAddress))
	return path

def getBalance(web3,address):
	contract = getContract(web3)
	balance=contract.functions.balanceOf(web3.to_checksum_address(address)).call()
	readableBalance=web3.from_wei(balance,'ether')
	return readableBalance

def getDecimals(web3):
	contract = getContract(web3)
	return contract.functions.decimals().call()

def multiplyToInt(web3,amount):
	return int(decimal.Decimal(amount)*decimal.Decimal(Math.pow(10,getDecimals(web3))))

def getDecimalsPow(web3):
	return int(1*Math.pow(10,getDecimals(web3)))
