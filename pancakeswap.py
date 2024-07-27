import config #locally store on your machine only, DO NOT COMMIT THIS FILE TO GIT   !!!!!
import time
import constant as c
import common

logger = common.getLogger()

def getRouterContract(web3):
	return web3.eth.contract(address=c.panRouterContractAddress, abi=c.panAbi)

# Get gas-price with x times speeded up
def getEstimatedGas(web3, senderAddress, nonce,isSpeedUp):
	estimatedGas = web3.eth.estimate_gas({
		"from"      : senderAddress,       
		"nonce"     : nonce
	})
	speededUpGas=estimatedGas*c.TXN_SPEED_UP_TIMES if isSpeedUp==True else estimatedGas
	logger.info("Estimated gas: {} | Speed-up gas: {}".format(estimatedGas,speededUpGas)) 
	return int(speededUpGas)


# Approve spender to swap token in wallet
def approve(web3, tokenAmount, token, spender_address, wallet_address, private_key):
  spender = spender_address
  #max_amount = web3.to_wei(2**64-1,'ether')
  tx = token.functions.approve(spender, tokenAmount).build_transaction({
      'from': wallet_address, 
      'nonce': web3.eth.get_transaction_count(wallet_address),
	#   'gas': getEstimatedGas(web3,wallet_address,web3.eth.get_transaction_count(wallet_address), False),
	  'gasPrice': web3.to_wei('1','gwei'),  # =  1.000.000.000 wei
      }) 
  signed_tx = web3.eth.account.sign_transaction(tx, private_key)
  tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
  return web3.to_hex(tx_hash)

# Swap from BNB for specific tokens| Spend=BNB, Buy=Token
def buyTokens(web3,bnbAmount,tokenAddress,senderAddress):
	try:
		nonce=web3.eth.get_transaction_count(senderAddress)
		router = getRouterContract(web3)
		# Buy & spend tokens
		tokenToBuy = web3.to_checksum_address(tokenAddress)
		tokenToSpend = web3.to_checksum_address(c.wbnbAddress)
		#Build txn
		pancakeswap2_txn=router.functions.swapExactETHForTokens(
			0, # set to 0, or specify minimum amount of tokens you want to receive - consider decimals!!!
			[tokenToSpend,tokenToBuy],
			senderAddress,
			(int(time.time()) + 10000) # transaction expires in 10s (10000ms)
			).build_transaction({
			'from': senderAddress,
			'value': bnbAmount, #This is the amount you want to Swap from
			# 'gas': getEstimatedGas(web3,senderAddress,nonce, True),
			'gasPrice': web3.to_wei('2','gwei'), 
			'nonce': nonce,
		})
		# Sign txn
		signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=config.private_key)
		# Submit txn
		return web3.eth.send_raw_transaction(signed_txn.rawTransaction)
	except ValueError as e:
		if e.args[0].get('message') in 'intrinsic gas too low':
			result = f"ERROR: {e.args[0].get('message')}"
		else:
			result = f"ERROR: {e.args[0].get('message')} : {e.args[0].get('code')}"
		return result


# Swap from specific token for BNB | Spend=Token, Buy=BNB
def sellTokens(web3,tokenAmount,tokenAddress,tokenContract,senderAddress):
	try:
		router = getRouterContract(web3)
		# Buy & spend tokens
		tokenToBuy = web3.to_checksum_address(c.wbnbAddress)
		tokenToSpend = web3.to_checksum_address(tokenAddress)

		# Approve Pancakeswap to spend token from wallet
		tid=approve(web3,tokenAmount,tokenContract,c.panRouterContractAddress,c.sender_address, config.private_key)
		logger.info("Approved to spend: https://bscscan.com/tx/{}".format(tid))
		status=0
		while status==0:
			try:
				result=web3.eth.get_transaction_receipt(tid)
				status=int(result.status)
				logger.info("Success = {}".format(status))
			except Exception as e :
				logger.info("...")
				# logger.info("Let's wait! Got exception: {}".format(e))
			finally:
				time.sleep(2)

		#Build txn
		pancakeswap2_txn=router.functions.swapExactTokensForETH(
			tokenAmount,
			0, # set to 0, or specify minimum amount of tokens you want to receive - consider decimals!!!
			[tokenToSpend,tokenToBuy],
			senderAddress,
			(int(time.time()) + 10000) # transaction expires in 10s (10000ms)
			).build_transaction({
			'from':senderAddress,
			# 'gas': getEstimatedGas(web3,senderAddress,web3.eth.get_transaction_count(senderAddress), True),
			'gasPrice': web3.to_wei('2','gwei'), 
			'nonce': web3.eth.get_transaction_count(senderAddress),
		})
		
		# Sign txn
		signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=config.private_key)
		# Submit txn
		return web3.eth.send_raw_transaction(signed_txn.rawTransaction)
	except ValueError as e:
		if e.args[0].get('message') in 'intrinsic gas too low':
			result = f"ERROR: {e.args[0].get('message')}"
		else:
			result = f"ERROR: {e.args[0].get('message')} : {e.args[0].get('code')}"
		return result

def getAmountsOut(web3,tokenToSpendAmount, path) :
	router = getRouterContract(web3)
	return router.functions.getAmountsOut(tokenToSpendAmount, path).call()