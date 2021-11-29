from brownie import *
from .settings import *
from .contracts import *
from .contract_addresses import *
import time


def main():
    load_accounts()

    treasury = web3.toChecksumAddress('0x66d7Dd55646100541F2B6ec15781b6d4C8372b1c')
    mona_token = CONTRACTS[network.show_active()]["mona_token"]

    # Deploy Contracts 
    access_control = CONTRACTS[network.show_active()]["access_control"]
    if access_control == '':
        access_control = deploy_access_control()
    if mona_token == '':
        mona_token = deploy_mona_token(access_control, MONA_SYMBOL, MONA_NAME, treasury, MONA_TREASURY_SUPPLY, MONA_TOKEN_CAP)
    
    weth_token = deploy_weth_token()

    # Deploy Uniswap Pool
    uniswap_pool = deploy_uniswap_pool(mona_token, weth_token)
    
    print(str(uniswap_pool))


