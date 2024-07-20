from time import strftime,localtime
import time
import math as Math
import decimal
import constant as c
import schedule

import common
import pancakeswap
import bnb
import qfs
import busd

web3 = common.connectBSC()


def checkWalletInfo():
	print("====================================================================")
	print("============================ Wallet info ===========================\n")
	print("Test-wallet has {} BNB, done {} transactions".format(bnb.getBalance(web3,c.sender_address), bnb.getNonce(web3,c.sender_address)))
	print("Test-wallet has {} QFS ".format(qfs.getBalance(web3,c.sender_address)))
	print("\n\n\n\n")


def checkPrice():
	start=strftime('%Y-%m-%d %H:%M:%S', localtime(time.time()))
	print("--------- {} -----------".format(start))
	# Check price: QFS <=> BNB
	amountIn=qfs.multiplyToInt(web3,1) # check for 1 QFS
	amountOut=pancakeswap.getAmountOut(web3, amountIn, c.qfsAddress, c.wbnbAddress)
	amountBnb=amountOut[1]/bnb.getDecimalsPow(web3)
	# Check price: BNB <=> BUSD
	amountIn=bnb.multiplyToInt(web3,amountBnb)
	amountOut=pancakeswap.getAmountOut(web3,amountIn, c.wbnbAddress, c.busdAddress)
	amountBusd=amountOut[1]/busd.getDecimalsPow(web3)
	print("1QFS = {0:.18f} BNB = {1:.18f} BUSD\n".format(amountBnb, amountBusd))

def swapTokens():
	# Swap buy-spend pair
	tx_token = pancakeswap.swap(web3,c.qfsAddress,c.wbnbAddress,c.sender_address)
	print("Transaction submitted: https://bscscan.com/tx/{}".format(web3.to_hex(tx_token)))


def job():
    checkPrice()


def startObserving():
	print("====================================================================")
	print("============================== Prices ==============================\n")
	# Start schedule for checking price, running every 2 second
	schedule.every(2).seconds.do(job)
	while True:
	    schedule.run_pending()
	    time.sleep(1)



startObserving()