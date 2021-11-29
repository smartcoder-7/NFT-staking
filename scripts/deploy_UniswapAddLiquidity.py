from brownie import *
from .settings import *
from .contracts import *
from .contract_addresses import *
import time


def main():
    load_accounts()

    treasury = web3.toChecksumAddress('0x66d7Dd55646100541F2B6ec15781b6d4C8372b1c')

    # Deploy Contracts 
    weth_token = deploy_weth_token()
    mona_token = get_mona_token()

    # Deploy Uniswap Pool
    uniswap_pool = deploy_uniswap_pool(mona_token, weth_token)

    weth_token.deposit({'from': accounts[0], 'value': 0.11*10**18})
    mona_token.transfer(uniswap_pool, 20 * 10**18, {'from':accounts[0]})
    weth_token.transfer( uniswap_pool,0.1 * 10**18,{'from':accounts[0]})
    uniswap_pool.mint(treasury,{'from':accounts[0]})
    print(str(uniswap_pool))


