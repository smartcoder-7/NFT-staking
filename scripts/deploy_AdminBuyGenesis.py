from brownie import *
from .settings import *
from .contracts import *
from .contract_addresses import *
import time


def main():
    load_accounts()

    # User to get Genesis NFT
    ##user = web3.toChecksumAddress('0x2A40019ABd4A61d71aBB73968BaB068ab389a636')
    user = web3.toChecksumAddress('0x1F3389Fc75Bf55275b03347E4283f24916F402f7')
    ##user = web3.toChecksumAddress('0x2F55acCE6958d390dc32606230B6BdA2dfec2102')

    # Get Contracts 
    genesis_nft_address = CONTRACTS[network.show_active()]["genesis_nft"]
    genesis_nft = DigitalaxGenesisNFT.at(genesis_nft_address)

    # Mint NFTs
    genesis_nft.adminBuy(user, {'from':accounts[0]})
    genesis_nft.transferFrom(user, web3.toChecksumAddress('0x2F55acCE6958d390dc32606230B6BdA2dfec2102'),1,{'from':accounts[1]})

    genesis_nft.adminBuy(user, {'from':accounts[0]})
    genesis_nft.transferFrom(user, web3.toChecksumAddress('0x2F55acCE6958d390dc32606230B6BdA2dfec2102'),2,{'from':accounts[1]})

    genesis_nft.adminBuy(user, {'from':accounts[0]})
    genesis_nft.transferFrom(user, web3.toChecksumAddress('0x2F55acCE6958d390dc32606230B6BdA2dfec2102'),3,{'from':accounts[1]})


    genesis_nft.adminBuy(user, {'from':accounts[0]})
    genesis_nft.transferFrom(user, web3.toChecksumAddress('0x2F55acCE6958d390dc32606230B6BdA2dfec2102'),4,{'from':accounts[1]})

    genesis_nft.adminBuy(user, {'from':accounts[0]})
    genesis_nft.transferFrom(user, web3.toChecksumAddress('0xb0CD38895f459d835541bd12eCB09CE99f57d7f9'),5,{'from':accounts[1]})

    genesis_nft.adminBuy(user, {'from':accounts[0]})
    genesis_nft.transferFrom(user, web3.toChecksumAddress('0xb0CD38895f459d835541bd12eCB09CE99f57d7f9'),6,{'from':accounts[1]})

    genesis_nft.adminBuy(user, {'from':accounts[0]})
    genesis_nft.transferFrom(user, web3.toChecksumAddress('0xb0CD38895f459d835541bd12eCB09CE99f57d7f9'),7,{'from':accounts[1]})


    genesis_nft.adminBuy(user, {'from':accounts[0]})
    genesis_nft.transferFrom(user, web3.toChecksumAddress('0xb0CD38895f459d835541bd12eCB09CE99f57d7f9'),8,{'from':accounts[1]})

    genesis_nft.adminBuy(user, {'from':accounts[0]})
    genesis_nft.transferFrom(user, web3.toChecksumAddress('0xb0CD38895f459d835541bd12eCB09CE99f57d7f9'),9,{'from':accounts[1]})





