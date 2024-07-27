import time

import constant as c
import common
import pancakeswap
import bnb
import qfs
import busd

web3 = common.connectBSC()
logger = common.getLogger()

def checkWalletInfo():
	logger.info("======= WALLET {} INFO =======".format(c.sender_address))
	logger.info("Done {} transactions".format(bnb.getNonce(web3,c.sender_address)))
	logger.info("Has {} BNB ( {} BUSD )".format(bnb.getBalance(web3,c.sender_address),calculateBUSD(bnb.getBalance(web3,c.sender_address), bnb)))
	logger.info("Has {} QFS".format(qfs.getBalance(web3,c.sender_address)))
	logger.info("Range trading {}: [{:.5f} - {:.5f}] ".format(qfs.getName(),qfs.LOWER_LIMIT,qfs.UPPER_LIMIT))
	logger.info("======================================================================\n")

# Calculate amount of BUSD from amount of specific token
def calculateBUSD(fromTokenAmount,tokenUtil):
	try:
		path=tokenUtil.getPath(web3)
		amountIn=tokenUtil.multiplyToInt(web3,fromTokenAmount) 
		amountOut=pancakeswap.getAmountsOut(web3,amountIn,path)
		amountBusd=amountOut[len(path)-1]/busd.getDecimalsPow(web3)
		return amountBusd	
	except Exception as e:
		logger.error("[{}] calculateBUSD: {}".format(tokenUtil.getName(), e))
		return 0
	
# Calculate amount of BNB from specific amount of BUSD
def calculateBNB(busdAmount):
	try:
		path=[] # path = BUSD > BNB
		path.append(web3.to_checksum_address(c.busdAddress))
		path.append(web3.to_checksum_address(c.wbnbAddress))
		amountIn=busd.multiplyToInt(web3,busdAmount) 
		amountOut=pancakeswap.getAmountsOut(web3,amountIn,path)
		amountBnb=amountOut[1]/bnb.getDecimalsPow(web3)
		return amountBnb	
	except Exception as e:
		logger.error("[{}] calculateBNB: {}".format(bnb.getName(), e))
		return 0

def buyQFS():
	bnbAmount=calculateBNB(c.BUY_AMOUNT) # Get BNB amount of [constans.BUY_AMOUNT] USD 
	# Spend: BNB, Buy: QFS
	tid = pancakeswap.buyTokens(web3,bnb.multiplyToInt(web3,bnbAmount),c.qfsAddress,c.sender_address)
	logger.info("----  Bought QFS from {} BNB : https://bscscan.com/tx/{}".format(bnbAmount, web3.to_hex(tid)))
	status=0
	while status==0:
		try:
			result=web3.eth.get_transaction_receipt(tid)
			status=int(result.status)
			logger.info("Success = {}".format(status))	
		except Exception as e :
			# logger.info("Let's wait! Got exception: {}".format(e))
			logger.info("...")
		finally:
			time.sleep(2)
	return tid

def sellQFS():
	qfsInWallet=qfs.getBalance(web3,c.sender_address)
	# Spend: QFS, Buy: BNB
	tid = pancakeswap.sellTokens(web3,qfs.multiplyToInt(web3,qfsInWallet),c.qfsAddress,qfs.getContract(web3),c.sender_address)
	logger.info("---- Sold {} QFS : https://bscscan.com/tx/{}".format(qfsInWallet, web3.to_hex(tid)))
	status=0
	while status==0:
		try:
			result=web3.eth.get_transaction_receipt(tid)
			status=int(result.status)
			logger.info("Success = {}".format(status))	
		except Exception as e :
			# logger.info("Let's wait! Got exception: {}".format(e))
			logger.info("...")
		finally:
			time.sleep(2)
	return tid

def watchQFS():
	logger.info("Start watching & trading: QFS")
	while True:
		qfsInWallet=qfs.getBalance(web3,c.sender_address)
		price=calculateBUSD(1, qfs)# check for 1 QFS
		logger.info("1 QFS = {:.18f} BUSD ||| QFS in Wallet: {}".format(price, qfsInWallet))

		if (price <= qfs.LOWER_LIMIT) and (qfsInWallet < qfs.MIN_AMOUNT):
			buyQFS()
			checkWalletInfo()
		elif (price >= qfs.UPPER_LIMIT) and (qfsInWallet >= qfs.MIN_AMOUNT):
			sellQFS() 
			checkWalletInfo()
		
		time.sleep(c.PRICE_CHECK_INTERVAL)
	

def main():
	checkWalletInfo()
	watchQFS()
	
if __name__ == "__main__":
    main()