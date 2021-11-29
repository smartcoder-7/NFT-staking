from brownie import accounts, web3, Wei, reverts, chain
from brownie.network.transaction import TransactionReceipt
from brownie.convert import to_address
import pytest
from brownie import Contract
from settings import *

@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

def staked_nft_all(staking_genesis, staked_nft):
    chain.sleep(GENESIS_AUCTION_TIME)

    for tokenId in range(1,7):
        staked_nft.setApprovalForAll(staking_genesis, True, {'from':accounts[tokenId]})
        txn = staking_genesis.stake(tokenId,{'from':accounts[tokenId]})
    
    totalEth =  (1.5 +0.1 +0.2 +1 +1 +1.7)*TENPOW18
   
    #Ask why there is 200 more wei
    assert staking_genesis.stakedEthTotal() == totalEth
    assert 'Staked' in txn.events
    return staked_nft


def test_stake_genesis_nft(staking_genesis, staked_nft):
    balance_of_staking_user = staking_genesis.stakers(accounts[2])[0]
    tokenId = 2
    
    assert balance_of_staking_user == 0.1*TENPOW18
    assert staked_nft.ownerOf(tokenId) == staking_genesis

    balance_of_staking_user = staking_genesis.stakers(accounts[3])[0]
    tokenId = 3
    
    assert balance_of_staking_user == 0.2*TENPOW18
    assert staked_nft.ownerOf(tokenId) == staking_genesis
    


 # Fail when trying to deposit something that is not mine
def test_fail_stake_not_owner(staking_genesis, staked_nft):
   
    staked_nft.setApprovalForAll(staking_genesis, True, {'from':accounts[2]})
    tokenId = 2
    with reverts():
        staking_genesis.stake(tokenId,{'from':accounts[3]})
        

    
def test_unstake_genesis_nft(staking_genesis, staked_nft):
    ## First staking tokens that will be unstaked
    
    
    chain.sleep(2000)
    chain.mine()
    ## see if reward generation is correct.

    ## For account 2 staking is 0.2 ##
    balance_of_user_after_staking = staking_genesis.stakers(accounts[3])[0]
    assert balance_of_user_after_staking == 0.2*TENPOW18
   
    token_id_to_unstake = 3
   
    
    txn = staking_genesis.unstake(token_id_to_unstake, {'from': accounts[3]})
    balance_of_user_after_unstaking = staking_genesis.stakers(accounts[3])[0]

    net_balance_of_user = balance_of_user_after_staking - balance_of_user_after_unstaking

    assert net_balance_of_user == 0.2 * TENPOW18
    assert balance_of_user_after_unstaking == 0
    
    assert staking_genesis.stakedEthTotal() == 5.3 * TENPOW18
    assert staked_nft.ownerOf(token_id_to_unstake) == accounts[3]
    assert 'Unstaked' in txn.events 

    

def test_rewards_genesis_staking(staked_nft,staking_genesis):

    chain.sleep(10000)
    
    print("stakers struct[balance]=",staking_genesis.stakers(accounts[2])[0])
    print("stakers struct[lastRewardPoints]=",staking_genesis.stakers(accounts[2])[1])
    print("stakers struct[lastRewardEarned]=",staking_genesis.stakers(accounts[2])[2])
    print("stakers struct[rewardsReleased]=",staking_genesis.stakers(accounts[2])[3])
    rewardsOwing = staking_genesis.rewardsOwing(accounts[2])
   
    print("rewardsOwing--->",rewardsOwing)
    print("total reward points -->",staking_genesis.rewardsPerTokenPoints())
    

