from brownie import *
from .settings import *
from .contracts import *
from .contract_addresses import *
import time


def main():
    load_accounts()

    # User to get Genesis NFT
    ##user = web3.toChecksumAddress('0x2A40019ABd4A61d71aBB73968BaB068ab389a636')
    ##user = web3.toChecksumAddress('0x1F3389Fc75Bf55275b03347E4283f24916F402f7')
    
    ## Replace with beneficiary address
    user = web3.toChecksumAddress('0x2F55acCE6958d390dc32606230B6BdA2dfec2102')

    # Get Contracts 
    parent_nft_address = CONTRACTS[network.show_active()]["parent_nft"]
    parent_nft = DreamClothingNFT.at(parent_nft_address)

    # Mint NFTs
    parent_nft.mint(user, 'https://gateway.pinata.cloud/ipfs/QmbTVX9J3vS5tiwhJzuh8XPRfthQK6BDb57462cRoh7RgM', user, {'from':accounts[0]});
    parent_nft.mint(user, 'https://gateway.pinata.cloud/ipfs/Qmf6Y22UbEim8gnrgbYhF2PiPB25TwqskzbGLJVeaaqcR1', user, {'from':accounts[0]});
    parent_nft.mint(user, 'https://gateway.pinata.cloud/ipfs/QmbTVX9J3vS5tiwhJzuh8XPRfthQK6BDb57462cRoh7RgM', user, {'from':accounts[0]});
    parent_nft.mint(user, 'https://gateway.pinata.cloud/ipfs/Qmf6Y22UbEim8gnrgbYhF2PiPB25TwqskzbGLJVeaaqcR1', user, {'from':accounts[0]});

    parent_nft.setPrimarySalePrice(1, 100, {'from':accounts[0]});
    parent_nft.setPrimarySalePrice(2, 200, {'from':accounts[0]});
    parent_nft.setPrimarySalePrice(3, 300, {'from':accounts[0]});
    parent_nft.setPrimarySalePrice(4, 400, {'from':accounts[0]});




