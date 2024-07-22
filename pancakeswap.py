import config #locally store on your machine only, DO NOT COMMIT THIS FILE TO GIT   !!!!!

import time
import constant as c

def getRouterContract(web3):
	return web3.eth.contract(address=c.panRouterContractAddress, abi=c.panAbi)

def buildTxn(web3,nonce,routerContract,tokenToBuy,tokenToSpend,senderAddress):
	# Build Pancakeswap transaction
	return routerContract.functions.swapExactETHForTokens(
		0, # set to 0, or specify minimum amount of tokens you want to receive - consider decimals!!!
		[tokenToSpend,tokenToBuy],
		senderAddress,
		(int(time.time()) + 10000) # transaction expires in 10s (10000ms)
		).build_transaction({
		'from': senderAddress,
		'value': web3.to_wei(0.00001,'ether'),#This is the Token(BNB) amount you want to Swap from
		'gas': 250000,
		'gasPrice': web3.to_wei('1','gwei'),
		'nonce': nonce,
	})

def swap(web3,tokenToBuyAddress,tokenToSpendAddress,senderAddress):
	router = getRouterContract(web3)
	nonce=web3.eth.get_transaction_count(senderAddress)
	# Buy & spend tokens
	tokenToBuy = web3.to_checksum_address(tokenToBuyAddress)
	tokenToSpend = web3.to_checksum_address(tokenToSpendAddress)
	#Build + Sign txn
	pancakeswap2_txn=buildTxn(web3,router,tokenToBuy,tokenToSpend,senderAddress)
	signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=config.private_key)
	# Submit txn
	return web3.eth.send_raw_transaction(signed_txn.rawTransaction)
	


def getAmountOut(web3,tokenToSpendAmount, tokenToSpendAddress, tokenToBuyAddress):
	router = getRouterContract(web3)
	tokenToBuy = web3.to_checksum_address(tokenToBuyAddress)
	tokenToSpend = web3.to_checksum_address(tokenToSpendAddress)
	return router.functions.getAmountsOut(tokenToSpendAmount, [tokenToSpend, tokenToBuy]).call()

def getAmountsOut(web3,tokenToSpendAmount, path) :
	router = getRouterContract(web3)
	return router.functions.getAmountsOut(tokenToSpendAmount, path).call()