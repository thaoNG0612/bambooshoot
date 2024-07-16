import config #locally store on your machine only, DO NOT COMMIT THIS FILE TO GIT   !!!!!

from web3 import Web3
from time import strftime,localtime
import time
import json
import constant as c

#Test BSC blockchain connection
web3 = Web3(Web3.HTTPProvider(c.bsc))
print("Connected to BSC blockchain: {}".format(web3.is_connected()))

#Check BNB balance
balance = web3.eth.get_balance(c.sender_address)
humanReadable = web3.from_wei(balance,'ether')
nonce = web3.eth.get_transaction_count(c.sender_address)
print("Test-wallet has {} BNB, done {} transactions".format(humanReadable, nonce))

#Setup the PancakeSwap contract, buy & spend tokens
contract = web3.eth.contract(address=c.panRouterContractAddress, abi=c.panAbi)
tokenToBuy = web3.to_checksum_address(c.tokenToBuyAddress)
spend = web3.to_checksum_address(c.tokenToSpendAddress)

# Timestamp of start
start=strftime('%Y-%m-%d %H:%M:%S', localtime(time.time()))
print("Started build and send transaction at {}".format(start))

# Build Pancakeswap transaction
pancakeswap2_txn = contract.functions.swapExactETHForTokens(
	0, # set to 0, or specify minimum amount of tokens you want to receive - consider decimals!!!
	[spend,tokenToBuy],
	c.sender_address,
	(int(time.time()) + 10000) # transaction expires in 10s (10000ms)
	).build_transaction({
	'from': c.sender_address,
	'value': web3.to_wei(0.00001,'ether'),#This is the Token(BNB) amount you want to Swap from
	'gas': 250000,
	'gasPrice': web3.to_wei('1','gwei'),
	'nonce': nonce,
})

# Sign the trasaction using wallet's private key => Send transaction
signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=config.mm_pk)
tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("Transaction submitted: https://bscscan.com/tx/{}".format(web3.to_hex(tx_token)))