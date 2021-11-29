from brownie import *
from .settings import *
from .contracts import *
from .contract_addresses import *

def get_lp_token(tokenA, tokenB):
    load_accounts()

    uniswap_pool_address = CONTRACTS[network.show_active()]["lp_token"]
    if uniswap_pool_address == '':
        uniswap_factory = interface.IUniswapV2Factory(UNISWAP_FACTORY)
        tx = uniswap_factory.getPair(tokenA, tokenB, {'from': accounts[0]})
        return tx

def main():
    mona_token = CONTRACTS[network.show_active()]["mona_token"]

    # Deploy Contracts 
    access_control = CONTRACTS[network.show_active()]["access_control"]
    weth_token = deploy_weth_token()
    address = get_lp_token(mona_token,weth_token)
    print(address)