import constant as c
import math as Math
import decimal

def getName():
	return "BUSD"

def getContract(web3):
	return web3.eth.contract(address=web3.to_checksum_address(c.busdAddress), abi=c.busdAbi)

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