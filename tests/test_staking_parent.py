from brownie import accounts, web3, Wei, reverts, chain
from brownie.network.transaction import TransactionReceipt
from brownie.convert import to_address
import pytest
from brownie import Contract
from settings import *

@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

# def staked_nft_all(staking_nft, parent_nft):
#     chain.sleep(GENESIS_AUCTION_TIME)

#     for tokenId in range(1,7):
#         parent_nft.setApprovalForAll(staking_nft, True, {'from':accounts[tokenId]})
#         txn = staking_nft.stake(tokenId,{'from':accounts[tokenId]})
    
#     # totalEth =  1.5*TENPOW18+0.1*TENPOW18+0.2*TENPOW18+1*TENPOW18+1*TENPOW18+1.7*TENPOW18
#        # assert staking_nft.stakedEthTotal() == totalEth
#     assert 'Staked' in txn.events
#     return parent_nft


# def test_stake_genesis_nft(staking_nft, parent_nft):
#     balance_of_staking_user = staking_nft.stakers(accounts[2])[0]
#     tokenId = 2
    
#     assert balance_of_staking_user == 0.1*TENPOW18
#     assert parent_nft.ownerOf(tokenId) == staking_nft

#     balance_of_staking_user = staking_nft.stakers(accounts[3])[0]
#     tokenId = 3
    
#     assert balance_of_staking_user == 0.2*TENPOW18
#     assert parent_nft.ownerOf(tokenId) == staking_nft
    
    


#  # Fail when trying to deposit something that is not mine
# def test_fail_stake_not_owner(staking_nft, parent_nft):
   
#     parent_nft.setApprovalForAll(staking_nft, True, {'from':accounts[2]})
#     tokenId = 2
#     with reverts():
#         staking_nft.stake(tokenId,{'from':accounts[3]})
        


    

# So the genesis contracts did not have any way to check how much was contributed
# So instead we put in the amounts using setContributions()
# The conftest.py should have the contributions set
# We will eventually need to add a setContributions script, later


# # Things the genesisis staking contract should check
# Deposit genesis token into staking contract
# Get the amount of staked ETH contributed for a user
# Withdraw token from staking contract


# Claim reward, not finished, but do it for now and we'll finish it 