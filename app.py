from time import strftime,localtime
import time
import constant as c
from eth_defi.event_reader.block_time import measure_block_time


import common
import pancakeswap
import bnb
import qfs
import busd

web3 = common.connectBSC()
logger = common.setupLogging('qfs.log')

def checkWalletInfo():
	logger.info("Test-wallet has {} BNB, done {} transactions".format(bnb.getBalance(web3,c.sender_address), bnb.getNonce(web3,c.sender_address)))
	logger.info("Test-wallet has {} QFS".format(qfs.getBalance(web3,c.sender_address)))

def checkQFSPrice():
	start=strftime('%Y-%m-%d %H:%M:%S', localtime(time.time()))
	path=[] # path = QFS > BNB > BUSD
	path.append(web3.to_checksum_address(c.qfsAddress))
	path.append(web3.to_checksum_address(c.wbnbAddress))
	path.append(web3.to_checksum_address(c.busdAddress))
	amountIn=qfs.multiplyToInt(web3,1) # check for 1 QFS
	amountOut=pancakeswap.getAmountsOut(web3,amountIn,path)
	amountBusd=amountOut[2]/busd.getDecimalsPow(web3)
	logger.info("{0:}	1 QFS = {1:.18f} BUSD".format(start, amountBusd))

def swapTokens():
	# Swap buy-spend pair
	tx_token = pancakeswap.swap(web3,c.qfsAddress,c.wbnbAddress,c.sender_address)
	print("Transaction submitted: https://bscscan.com/tx/{}".format(web3.to_hex(tx_token)))


def main():
	checkWalletInfo()
	logger.info("Start watching & trading: QFS.....")
	while True:
		# Start schedule for checking price, running every 2 second
		checkQFSPrice()
		block_time = measure_block_time(web3)
		time.sleep(block_time)
	
if __name__ == "__main__":
    main()