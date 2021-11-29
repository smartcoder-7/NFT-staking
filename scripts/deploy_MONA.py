from brownie import *
from .settings import *
from .contracts import *
from .contract_addresses import *
import time


def main():
    if network.show_active() == 'mainnet':
        # replace with your keys
        accounts.load("dream")
    # add accounts if active network is goerli
    if network.show_active() in ['goerli', 'ropsten','kovan','rinkeby']:
        # 0x2A40019ABd4A61d71aBB73968BaB068ab389a636
        accounts.add('4ca89ec18e37683efa18e0434cd9a28c82d461189c477f5622dae974b43baebf')
        # 0x1F3389Fc75Bf55275b03347E4283f24916F402f7
        accounts.add('fa3c06c67426b848e6cef377a2dbd2d832d3718999fbe377236676c9216d8ec0')

    access_control = CONTRACTS[network.show_active()]["access_control"]
    treasury = web3.toChecksumAddress('0x66d7Dd55646100541F2B6ec15781b6d4C8372b1c')

    if access_control == '':
        access_control = deploy_access_control()


    mona_token = deploy_mona_token(access_control, MONA_SYMBOL, MONA_NAME, treasury, MONA_TREASURY_SUPPLY, MONA_TOKEN_CAP)


