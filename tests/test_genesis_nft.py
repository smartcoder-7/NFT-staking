from brownie import accounts, web3, Wei, reverts, chain
from brownie.network.transaction import TransactionReceipt
from brownie.convert import to_address
import pytest
from brownie import Contract
from settings import *

@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

# def test_buy_NFT_during_genesis(genesis_nft):
#     #genesis start timestamp slept
#     chain.sleep(15)
#     chain.mine()
#     txn = genesis_nft.buy({'from':accounts[2],'value':'1 ethers'})
#     assert 'GenesisPurchased' in txn.events
    
# def test_buy_NFT_during_genesis_and_end(genesis_nft):
#     #genesis start timestamp slept
#     chain.sleep(15)
#     chain.mine()
#     txn = genesis_nft.buy({'from':accounts[2],'value':'1 ethers'})
#     assert 'GenesisPurchased' in txn.events
#     txn = genesis_nft.buyOrIncreaseContribution({'from':accounts[2],'value':'0.5 ethers'})
#     assert 'ContributionIncreased' in txn.events
#     chain.sleep(GENESIS_AUCTION_TIME)

# def test_staked_nft_to_transfer(staked_nft):
#     chain.sleep(GENESIS_AUCTION_TIME)
#     chain.mine()
#     tokenId = 1
#     ######### token id and from_address (accounts[id]) have same ids
#     from_address = accounts[1]
#     to_address = accounts[9]
#     staked_nft.transferFrom(from_address,to_address,tokenId,{'from':from_address})
#     assert staked_nft.ownerOf(tokenId) == to_address
#     tokenId = 6
#     from_address = accounts[6]
    
#     staked_nft.transferFrom(from_address,to_address,tokenId,{'from':from_address})
#     assert staked_nft.ownerOf(tokenId) == to_address
#     assert staked_nft.balanceOf(to_address) == 2

