import constant as c
from web3 import Web3
from web3.middleware import geth_poa_middleware
import logging

# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=c.LOG_FILE,
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger().addHandler(console)

# Now, we can log to the root logger, or any other logger. First the root...
logging.info('Logger is initiated.')

def connectBSC():
    web3 = Web3(Web3.HTTPProvider(c.bsc))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    logging.info("Connected to BSC blockchain: {}\n".format(web3.is_connected()))
    return web3

def getLogger():
    return logging
