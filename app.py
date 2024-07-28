import time

import constant as c
from defilib import *
from tokenslib import *

web3 = common.connectBSC()
logger = common.setupLogger(__name__, c.LOG_FILE)

def checkWalletInfo():
	logger.info("======= WALLET {} INFO =======".format(c.sender_address))
	logger.info("Done {} transactions".format(bnb.getNonce(web3,c.sender_address)))
	logger.info("Has {} BNB ( {} BUSD )".format(bnb.getBalance(web3,c.sender_address),calculateBUSD(bnb.getBalance(web3,c.sender_address), bnb)))
	for token in c.TRADING_LIST:
		logger.info("Has {} {} || Range trading: [{:.9f} - {:.9f}] ".format(token.getBalance(web3,c.sender_address), token.getName(), token.LOWER_LIMIT,token.UPPER_LIMIT))
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
		path.append(web3.to_checksum_address(busd.ADDRESS))
		path.append(web3.to_checksum_address(bnb.ADDRESS))
		amountIn=busd.multiplyToInt(web3,busdAmount) 
		amountOut=pancakeswap.getAmountsOut(web3,amountIn,path)
		amountBnb=amountOut[1]/bnb.getDecimalsPow(web3)
		return amountBnb	
	except Exception as e:
		logger.error("[{}] calculateBNB: {}".format(bnb.getName(), e))
		return 0

def buy(token):
	bnbAmount=calculateBNB(c.BUY_AMOUNT) # Get BNB amount of [constans.BUY_AMOUNT] USD 
	# Spend: BNB, Buy: Token
	tid = pancakeswap.buyTokens(web3,bnb.multiplyToInt(web3,bnbAmount),token.ADDRESS,c.sender_address)
	logger.info("----  Bought {} from {} BNB : https://bscscan.com/tx/{}".format(token.getName(), bnbAmount, web3.to_hex(tid)))
	status=0
	while status==0:
		try:
			result=web3.eth.get_transaction_receipt(tid)
			status=int(result.status)
			logger.info("Success = {}".format(status))
			if status==0:
				logger.info("Status = {} | Failed txn!".format(status))	
				status=-1 #failed txn, get out of loop
		except Exception as e :
			# logger.info("Let's wait! Got exception: {}".format(e))
			logger.info("...")
		finally:
			time.sleep(2)
	return tid

def sell(token):
	tokenInWallet=token.getBalance(web3,c.sender_address)
	# Spend: Token, Buy: BNB
	tid = pancakeswap.sellTokens(web3,token.multiplyToInt(web3,tokenInWallet),token.ADDRESS,token.getContract(web3),c.sender_address)
	logger.info("---- Sold {} {} : https://bscscan.com/tx/{}".format(tokenInWallet, token.getName(), web3.to_hex(tid)))
	status=0
	while status==0:
		try:
			result=web3.eth.get_transaction_receipt(tid)
			status=int(result.status)
			if status==0:
				logger.info("Status = {} | Failed txn!".format(status))	
				status=-1 #failed txn, get out of loop
		except Exception as e :
			# logger.info("Let's wait! Got exception: {}".format(e))
			logger.info("...")
		finally:
			time.sleep(2)
	return tid

def watch(token):
	logger.info("Start watching & trading: {}".format(token.getName()))
	counter = 0
	while True:
		tokenInWallet=token.getBalance(web3,c.sender_address)
		price=calculateBUSD(1, token)# check for 1 token
		# Only log price to console after 20 checks
		counter+=1
		if counter == 20:
			logger.info("1 {} = {:.18f} BUSD ||| Token in Wallet: {}".format(token.getName(), price, tokenInWallet))
			counter = 0
			
		if (price <= token.LOWER_LIMIT) and (tokenInWallet < token.MIN_AMOUNT):
			buy(token)
			checkWalletInfo()
		elif (price >= token.UPPER_LIMIT) and (tokenInWallet >= token.MIN_AMOUNT):
			sell(token) 
			checkWalletInfo()
		
		time.sleep(c.PRICE_CHECK_INTERVAL)
	

def main(token):
	global logger
	logger = common.setupLogger(token.getName(), c.LOG_FILE)
	watch(token)
	
if __name__ == "__main__":
	checkWalletInfo()
	token = str.lower(input('What token to run [QFS,SHIB]?\n'))
	match token:
		case "qfs":
			main(qfs)
		case "shib":
			main(shib)
		case _:
			"Token not found."

    