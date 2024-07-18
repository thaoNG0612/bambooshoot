from time import strftime,localtime
import time
import constant as c

import common
import pancakeswap
import bnb
import qfs

web3 = common.connectBSC()
print("Test-wallet has {} BNB, done {} transactions".format(bnb.getBalance(web3,c.sender_address), bnb.getNonce(web3,c.sender_address)))
print("Test-wallet has {} QFS ".format(qfs.getBalance(web3,c.sender_address)))


# Swap buy-spend pair
#tx_token = pancakeswap.swap(web3,c.qfsAddress,c.wbnbAddress,c.sender_address)
#print("Transaction submitted: https://bscscan.com/tx/{}".format(web3.to_hex(tx_token)))
