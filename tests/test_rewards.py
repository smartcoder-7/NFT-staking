from brownie import accounts, web3, Wei, reverts, chain
from brownie.network.transaction import TransactionReceipt
from brownie.convert import to_address
import pytest
from brownie import Contract
from settings import *

@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_get_current_reward_week(staking_rewards):

    chain.sleep(15)
    chain.mine()
    current_week = staking_rewards.getCurrentRewardWeek()
    assert current_week == 0 

def test_get_current_reward_week1(staking_rewards):
    days = 14
    chain.sleep(days*24*60*60)
    chain.mine()
    current_week = staking_rewards.getCurrentRewardWeek()
    assert current_week == 2 

def test_get_total_contributions(staking_rewards_mock, staking_genesis_mock, staking_nft_mock, staking_lp_mock):
    staking_genesis_mock.setStakedEthTotal(5.0*TENPOW18)
    staking_nft_mock.setStakedEthTotal(6.5*TENPOW18)
    # LP staking is 0 due to Uniswap
    # staking_lp_mock.setStakedEthTotal(0*TENPOW18)
    assert staking_rewards_mock.getTotalContributions() == (5.0 + 6.5)*TENPOW18

# def test_update_rewards(staking_rewards_mock):
#     staking_rewards_mock.updateRewards()
#     days = 6
#     chain.sleep(days*24*60*60)
#     chain.mine()
#     staking_rewards_mock.updateRewards()
#     days = 10
#     chain.sleep(days*24*60*60)
#     chain.mine()
#     staking_rewards_mock.updateRewards()
#     days = 50
#     chain.sleep(days*24*60*60)
#     chain.mine()
#     staking_rewards_mock.updateRewards()



def test_get_genesis_rewards(staking_rewards):
    current_week = staking_rewards.getCurrentWeek()
    print("CurrentWeek: ", staking_rewards.getCurrentWeek())

    print("lastRewardTime: ", staking_rewards.lastRewardTime())
    print("Total Rewards paid= ", staking_rewards.totalRewardsPaid())
    print("CurrentGenesisWtPoints: ", staking_rewards.getCurrentGenesisWtPoints())
    print("CurrentParentWtPoints: ", staking_rewards.getCurrentParentWtPoints())
    print("CurrentLpWeightPoints: ", staking_rewards.getCurrentLpWeightPoints())
    days = 2
    start_time = staking_rewards.startTime() 
    end_time = start_time + days*24*60*60
    chain.sleep(days*24*60*60)
    chain.mine()
    staking_rewards.updateRewards()
    genesis_rewards = staking_rewards.genesisRewards(start_time, end_time)/ TENPOW18
    print("Genesis Rewards for ", days, "days is = ", genesis_rewards)
    print("lastRewardTime: ", staking_rewards.lastRewardTime())
    print("CurrentWeek: ", staking_rewards.getCurrentWeek())

    print("CurrentGenesisWtPoints: ", staking_rewards.getCurrentGenesisWtPoints())
    print("CurrentParentWtPoints: ", staking_rewards.getCurrentParentWtPoints())
    print("CurrentLpWeightPoints: ", staking_rewards.getCurrentLpWeightPoints())
    print("Total Rewards paid= ", staking_rewards.totalRewardsPaid()/ TENPOW18)


    days = 15
    start_time = staking_rewards.startTime() 
    end_time = start_time + days*24*60*60
    chain.sleep(days*24*60*60)
    chain.mine()
    staking_rewards.updateRewards()
    genesis_rewards = staking_rewards.genesisRewards(start_time, end_time) / TENPOW18
    print("Genesis Rewards for ", days, "days is = ", genesis_rewards)
    print("CurrentWeek: ", staking_rewards.getCurrentWeek())
    print("lastRewardTime: ", staking_rewards.lastRewardTime())
    print("CurrentGenesisWtPoints: ", staking_rewards.getCurrentGenesisWtPoints())
    print("CurrentParentWtPoints: ", staking_rewards.getCurrentParentWtPoints())
    print("CurrentLpWeightPoints: ", staking_rewards.getCurrentLpWeightPoints())

    print("Total Rewards paid= ", staking_rewards.totalRewardsPaid()/ TENPOW18)

    days = 27
    start_time = staking_rewards.startTime() 
    end_time = start_time + days*24*60*60
    chain.sleep(days*24*60*60)
    chain.mine()
    staking_rewards.updateRewards()
    genesis_rewards = staking_rewards.genesisRewards(start_time, end_time) / TENPOW18
    chain.mine()
    print("Genesis Rewards for ", days, "days is = ", genesis_rewards)
    print("CurrentWeek: ", staking_rewards.getCurrentWeek())
    print("lastRewardTime: ", staking_rewards.lastRewardTime())
    print("CurrentGenesisWtPoints: ", staking_rewards.getCurrentGenesisWtPoints())
    print("CurrentParentWtPoints: ", staking_rewards.getCurrentParentWtPoints())
    print("CurrentLpWeightPoints: ", staking_rewards.getCurrentLpWeightPoints())
    genesis_rewards_paid =  staking_rewards.genesisRewardsPaid()
    print("Genesis Rewards paid= ", genesis_rewards_paid)
    print("Total Rewards paid= ", staking_rewards.totalRewardsPaid()/ TENPOW18)



def test_get_mock_genesis_rewards(staking_rewards_mock):
    print("CurrentWeek: ", staking_rewards_mock.getCurrentWeek())
    print("lastRewardTime: ", staking_rewards_mock.lastRewardTime())
    print("Total Rewards paid= ", staking_rewards_mock.totalRewardsPaid())
    print("CurrentGenesisWtPoints: ", staking_rewards_mock.getCurrentGenesisWtPoints())
    print("CurrentParentWtPoints: ", staking_rewards_mock.getCurrentParentWtPoints())
    print("CurrentLpWeightPoints: ", staking_rewards_mock.getCurrentLpWeightPoints())

    days = 2
    start_time = staking_rewards_mock.startTime() 
    end_time = start_time + days*24*60*60
    chain.sleep(days*24*60*60)
    chain.mine()
    staking_rewards_mock.updateRewards()
    genesis_rewards = staking_rewards_mock.genesisRewards(start_time, end_time)/ TENPOW18
    print("Mock Genesis Rewards for ", days, "days is = ", genesis_rewards)
    print("lastRewardTime: ", staking_rewards_mock.lastRewardTime())
    print("CurrentGenesisWtPoints: ", staking_rewards_mock.getCurrentGenesisWtPoints())
    print("CurrentParentWtPoints: ", staking_rewards_mock.getCurrentParentWtPoints())
    print("CurrentLpWeightPoints: ", staking_rewards_mock.getCurrentLpWeightPoints())
    print("Total Rewards paid= ", staking_rewards_mock.totalRewardsPaid()/ TENPOW18)
    print("CurrentWeek: ", staking_rewards_mock.getCurrentWeek())

    days = 15
    start_time = staking_rewards_mock.startTime() 
    end_time = start_time + days*24*60*60
    chain.sleep(days*24*60*60)
    chain.mine()
    staking_rewards_mock.updateRewards()
    genesis_rewards = staking_rewards_mock.genesisRewards(start_time, end_time)/ TENPOW18
    print("Mock Genesis Rewards for ", days, "days is = ", genesis_rewards)
    print("lastRewardTime: ", staking_rewards_mock.lastRewardTime())
    print("CurrentGenesisWtPoints: ", staking_rewards_mock.getCurrentGenesisWtPoints())
    print("CurrentParentWtPoints: ", staking_rewards_mock.getCurrentParentWtPoints())
    print("CurrentLpWeightPoints: ", staking_rewards_mock.getCurrentLpWeightPoints())    
    print("Total Rewards paid= ", staking_rewards_mock.totalRewardsPaid()/ TENPOW18)
    print("CurrentWeek: ", staking_rewards_mock.getCurrentWeek())

    days = 27
    start_time = staking_rewards_mock.startTime() 
    end_time = start_time + days*24*60*60
    chain.sleep(days*24*60*60)
    chain.mine()
    staking_rewards_mock.updateRewards()
    genesis_rewards = staking_rewards_mock.genesisRewards(start_time, end_time)/ TENPOW18
    genesis_rewards_paid =  staking_rewards_mock.genesisRewardsPaid()
    chain.mine()
    print("Mock Genesis Rewards for ", days, "days is = ", genesis_rewards)
    print("lastRewardTime: ", staking_rewards_mock.lastRewardTime())
    print("CurrentGenesisWtPoints: ", staking_rewards_mock.getCurrentGenesisWtPoints())
    print("CurrentParentWtPoints: ", staking_rewards_mock.getCurrentParentWtPoints())
    print("CurrentLpWeightPoints: ", staking_rewards_mock.getCurrentLpWeightPoints())
    print("CurrentWeek: ", staking_rewards_mock.getCurrentWeek())
   
    print("Mock Genesis Rewards paid= ", genesis_rewards_paid)
    print("Total Rewards paid= ", staking_rewards_mock.totalRewardsPaid()/ TENPOW18)
    

def test_get_genesis_staked_eth(staking_rewards_mock):
    genesis_staked_eth_total = staking_rewards_mock.getGenesisStakedEthTotal()
    print("getGenesisStakedEthTotal= ", genesis_staked_eth_total)

def test_get_mock_genesis_staked_eth(staking_rewards):
    genesis_staked_eth_total = staking_rewards.getGenesisStakedEthTotal()
    print("getGenesisStakedEthTotal= ", genesis_staked_eth_total)


# def test_get_mock_genesis_rewards(staking_rewards):
#     genesis_staked_eth_total = staking_rewards.getGenesisStakedEthTotal()
#     print("getGenesisStakedEthTotal= ", genesis_staked_eth_total)



def test_stake_genesis(staking_rewards, staking_genesis,staked_nft,mona_token):
    print_mona_balances(mona_token, staking_genesis, staking_rewards)
    chain.sleep(GENESIS_AUCTION_TIME +20)
    print_mona_balances(mona_token, staking_genesis, staking_rewards)
    
    for tokenId in range(7,10):
        staked_nft.setApprovalForAll(staking_genesis, True, {'from':accounts[tokenId]})
        staking_genesis.stake(tokenId,{'from':accounts[tokenId]})
    
    totalEth = (0.1 + 0.3 + 0.5) * TENPOW18
    print_mona_balances(mona_token, staking_genesis, staking_rewards)

    days = 14

    chain.sleep(days * 24 * 60 * 60)
    tokenId = 7
    print_mona_balances(mona_token, staking_genesis, staking_rewards)
    txn = staking_genesis.unstake(tokenId, {'from': accounts[tokenId]})
    start_time = staking_rewards.startTime() 
    end_time = start_time + days*24*60*60
    genesis_rewards = staking_rewards.genesisRewards(start_time, end_time)
    
    print("Genesis Rewards for ", days, "days is = ", genesis_rewards/TENPOW18)
    
    balanceOfAccount = mona_token.balanceOf(accounts[tokenId])
    balanceOfStakingGenesisContract = mona_token.balanceOf(staking_genesis)
   
    print("balance of the mona token of accounts[",tokenId,"]=",balanceOfAccount/TENPOW18)
    print('balance of mona token in the contract staking genesis after unstaking token[',tokenId,"]=",balanceOfStakingGenesisContract/TENPOW18)
    tokenId = 9
    txn = staking_genesis.unstake(tokenId, {'from': accounts[tokenId]})
    
    balanceOfAccount = mona_token.balanceOf(accounts[tokenId])
    balanceOfStakingGenesisContract = mona_token.balanceOf(staking_genesis)
   
    print("balance of the mona token of accounts[",tokenId,"]=",balanceOfAccount/TENPOW18)
    print('balance of mona token in the contract staking genesis after unstaking token[',tokenId,"]=",balanceOfStakingGenesisContract/TENPOW18)
 

    tokenId = 8
    txn = staking_genesis.unstake(tokenId, {'from': accounts[tokenId]})
    
    
    
    balanceOfAccount = mona_token.balanceOf(accounts[tokenId])
    balanceOfStakingGenesisContract = mona_token.balanceOf(staking_genesis)

    print("balance of the mona token of accounts[",tokenId,"]=",balanceOfAccount/TENPOW18)
    print('balance of mona token in the contract staking genesis after unstaking token[',tokenId,"]=",balanceOfStakingGenesisContract/TENPOW18)
    

    
    print_mona_balances(mona_token, staking_genesis, staking_rewards)

   # print('added: ', balanceOfStakingGenesisContract+balanceOfAccount)
    print('------------------------------- after 28 days')
    days = 28
    

    chain.sleep(14 * 24 * 60 * 60)
    tokenId = 6
    
    txn = staking_genesis.unstake(tokenId, {'from': accounts[tokenId]})
    start_time = staking_rewards.startTime() 
    end_time = start_time + days*24*60*60
    genesis_rewards = staking_rewards.genesisRewards(start_time, end_time)
    
    print("Genesis Rewards for ", days, "days is = ", genesis_rewards/TENPOW18)
    
    balanceOfAccount = mona_token.balanceOf(accounts[tokenId])
    balanceOfStakingGenesisContract = mona_token.balanceOf(staking_genesis)
   
    print("balance of the mona token of accounts[",tokenId,"]=",balanceOfAccount/TENPOW18)
    print('balance of mona token in the contract staking genesis after unstaking token[',tokenId,"]=",balanceOfStakingGenesisContract/TENPOW18)
    print_mona_balances(mona_token, staking_genesis, staking_rewards)           
    print('staking ------------------------------- after 28 days')
    tokenId = 7
    days = 8
    chain.sleep(days * 24 * 60 * 60)
    txn = staking_genesis.stake(tokenId, {'from':accounts[tokenId]})
    days = 8
    chain.sleep(days * 24 * 60 * 60)
    txn = staking_genesis.unstake(tokenId, {'from': accounts[tokenId]})

    # for tokenId in range(1,5):
    #     txn = staking_genesis.unstake(tokenId, {'from': accounts[tokenId]})
    unstake_staked_tokens(staking_genesis)

    balanceOfAccount = mona_token.balanceOf(accounts[tokenId])
    balanceOfStakingGenesisContract = mona_token.balanceOf(staking_genesis)
    balanceOfRewardContract = mona_token.balanceOf(staking_rewards)
   
    print("balance of the mona token of accounts[",tokenId,"]=",balanceOfAccount/TENPOW18)
    print('balance of mona token in the contract staking genesis after staking token [',tokenId,"]=",balanceOfStakingGenesisContract/TENPOW18)
    print_mona_balances(mona_token, staking_genesis, staking_rewards)

def unstake_staked_tokens(staking_genesis):
    for tokenId in range(0,10):
        if (accounts[tokenId] == staking_genesis.tokenOwner(tokenId)):
            txn = staking_genesis.unstake(tokenId, {'from': accounts[tokenId]})
            print("unstaked accounts[",tokenId,"]=",accounts[tokenId])



def print_mona_balances(mona_token, staking_genesis, staking_rewards):
    total_balance = 0
    print('TIME: ',chain.time())

    for tokenId in range(0,10):
        balance = mona_token.balanceOf(accounts[tokenId])
        total_balance = total_balance + balance
        print("MONA Balance accounts[",tokenId,"]=",mona_token.balanceOf(accounts[tokenId])/TENPOW18)

    print('MONA in staking genesis: ',mona_token.balanceOf(staking_genesis)/TENPOW18)
    print('MONA in staking rewards: ',mona_token.balanceOf(staking_rewards)/TENPOW18)
    print('MONA in total balance: ',(total_balance+ mona_token.balanceOf(staking_genesis) + mona_token.balanceOf(staking_rewards))/TENPOW18)
    print('MONA in total supply: ',mona_token.totalSupply()/TENPOW18)

# def test_get_return_weights(staking_rewards):
#     assert staking_rewards.startTime() > 0
#     assert staking_rewards.startTime() <= chain.time() 
#     assert staking_rewards.lastRewardTime() == staking_rewards.startTime()
#     days = 140
#     chain.sleep(days*24*60*60)
#     chain.mine()
#     tx = staking_rewards.genesisRewards(staking_rewards.startTime(), chain.time()  )



# Private function 
# def test_check_normaliser_weights(staking_rewards):
#     _g = 1 * TENPOW18
#     _p = 100.00 * TENPOW18
#     _m =  10.00 * TENPOW18

#     (gw, pw, mw) = staking_rewards._getReturnWeights(_g,_p,_m)
#     assert gw ==  20266344914718466
#     assert pw == 777070205938096872
#     assert mw == 202663449147184661
