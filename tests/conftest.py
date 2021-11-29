
from brownie import accounts, web3, Wei, chain
from brownie.network.transaction import TransactionReceipt
from brownie.convert import to_address
import pytest
from brownie import Contract
from settings import *


##############################################
# Access Controls
##############################################

@pytest.fixture(scope='module', autouse=True)
def access_controls(DigitalaxAccessControls):
    access_controls = DigitalaxAccessControls.deploy({'from': accounts[0]})
    return access_controls

##############################################
# MONA Token
##############################################

@pytest.fixture(scope='module', autouse=True)
def mona_token(MONA, access_controls):
    tokenOwner = accounts[2]
    initialSupply = 1000
    mona_token = MONA.deploy( 
                        MONA_SYMBOL
                        , MONA_NAME
                        , 18
                        , access_controls
                        , tokenOwner
                        , initialSupply
         , {'from': accounts[0]})
    return mona_token

@pytest.fixture(scope='module', autouse=True)
def weth_token(WETH9):
    weth_token = WETH9.deploy({'from': accounts[0]})
    return weth_token

#####################################
#LP TOKEN USE - Replace with LP contract
######################################
@pytest.fixture(scope='module', autouse=True)
def lp_token(MONA,weth_token, access_controls):
    tokenOwner = accounts[2]
    initialSupply = 1000
    lp_token = MONA.deploy( 
                        'LP'
                        ,'MONALP'
                        , 18
                        , access_controls
                        , tokenOwner
                        , initialSupply
         , {'from': accounts[0]})
    return lp_token

##############################################
# NFT Tokens
##############################################

@pytest.fixture(scope='module', autouse=True)
def genesis_nft(DigitalaxGenesisNFT, access_controls):
    fundsMultisig = accounts[1]
    genesisStartTimestamp = chain.time() +10
    genesisEndTimestamp = chain.time() + 10 + GENESIS_AUCTION_TIME

    genesis_nft = DigitalaxGenesisNFT.deploy(
                            access_controls
                            , fundsMultisig
                            , genesisStartTimestamp
                            , genesisEndTimestamp
                            , GENESIS_TOKEN_URI
                            , {"from": accounts[0]})
    return genesis_nft


@pytest.fixture(scope='module', autouse=True)
def parent_nft(DigitalaxGenesisNFT, access_controls):
    fundsMultisig = accounts[1]
    genesisStartTimestamp = chain.time() +10
    genesisEndTimestamp = chain.time() + 10 + GENESIS_AUCTION_TIME

    parent_nft = DigitalaxGenesisNFT.deploy(
                            access_controls
                            , fundsMultisig
                            , genesisStartTimestamp
                            , genesisEndTimestamp
                            , GENESIS_TOKEN_URI
                            , {"from": accounts[0]})
    return parent_nft

##############################################
# Staking
##############################################

@pytest.fixture(scope='module', autouse=True)
def staked_nft(DigitalaxGenesisNFT, access_controls):
    fundsMultisig = accounts[1]
    genesisStartTimestamp = chain.time() +10
    genesisEndTimestamp = chain.time() + 10 + GENESIS_AUCTION_TIME
    staked_nft = DigitalaxGenesisNFT.deploy(
               access_controls
               , fundsMultisig
               , genesisStartTimestamp
               , genesisEndTimestamp
               , GENESIS_TOKEN_URI
               , {"from": accounts[0]})
    chain.sleep(10)

    # Add some transactions for this instance to test
    txn = staked_nft.buy({'from':accounts[1],'value':'1 ethers'})
    assert 'GenesisPurchased' in txn.events
    txn = staked_nft.buyOrIncreaseContribution({'from':accounts[1],'value':'0.5 ethers'})
    txn = staked_nft.buyOrIncreaseContribution({'from':accounts[2],'value':'0.1 ethers'})
    txn = staked_nft.buyOrIncreaseContribution({'from':accounts[3],'value':'0.2 ethers'})
    txn = staked_nft.buyOrIncreaseContribution({'from':accounts[4],'value':'1.1 ethers'})
    txn = staked_nft.buyOrIncreaseContribution({'from':accounts[5],'value':'1.1 ethers'})
    txn = staked_nft.buyOrIncreaseContribution({'from':accounts[6],'value':'1.7 ethers'})
    txn = staked_nft.buyOrIncreaseContribution({'from':accounts[7],'value':'0.1 ethers'})
    txn = staked_nft.buyOrIncreaseContribution({'from':accounts[8],'value':'0.3 ethers'})
    txn = staked_nft.buyOrIncreaseContribution({'from':accounts[9],'value':'0.5 ethers'})
    assert 'GenesisPurchased' in txn.events
    return staked_nft


@pytest.fixture(scope='module', autouse=True)
def staking_genesis(DigitalaxGenesisStaking, mona_token, staked_nft, access_controls):
    staking_genesis = DigitalaxGenesisStaking.deploy({'from': accounts[0]})
    staking_genesis.initGenesisStaking(
            accounts[1]
            , mona_token
            , staked_nft
            , access_controls
            , {"from": accounts[0]})
    # So the genesis contracts did not have any way to check how much was contributed
    # So instead we put in the amounts using setContributions()
    # The conftest.py should have the contributions set
    tokens = [1,2,3,4,5,6,7,8,9]
    amounts = [1.5*TENPOW18,0.1*TENPOW18,0.2*TENPOW18,1*TENPOW18,1*TENPOW18,1.7*TENPOW18,0.1*TENPOW18,0.3*TENPOW18,0.5*TENPOW18]
    staking_genesis.setContributions(tokens,amounts)
    staking_genesis.setTokensClaimable(True)

    return staking_genesis

@pytest.fixture(scope='module', autouse=True)
def staking_nft(DigitalaxNFTStaking, mona_token, parent_nft, access_controls):
     #rewardsPerSecond = REWARDS_PER_SECOND
     staking_nft = DigitalaxNFTStaking.deploy({'from': accounts[0]})
     staking_nft.initStaking(
              mona_token
             , parent_nft
             , access_controls
             , {"from": accounts[0]})
     return staking_nft 

@pytest.fixture(scope='module', autouse=True)
def staking_lp(DigitalaxLPStaking,lp_token, mona_token, weth_token, access_controls):
     #rewardsPerSecond = REWARDS_PER_SECOND
     staking_lp = DigitalaxLPStaking.deploy({'from': accounts[0]})
     staking_lp.initLPStaking(
              mona_token
             , lp_token
             , weth_token
             , access_controls
             , {"from": accounts[0]})

     return staking_lp



##############################################
# Rewards
##############################################
@pytest.fixture(scope='module', autouse=True)
def staking_genesis_mock(MockStaking):
    return MockStaking.deploy(0.5*TENPOW18, {'from':accounts[0]})
@pytest.fixture(scope='module', autouse=True)
def staking_nft_mock(MockStaking):
    return MockStaking.deploy(0.5*TENPOW18, {'from':accounts[0]})
@pytest.fixture(scope='module', autouse=True)
def staking_lp_mock(MockStaking):
    return MockStaking.deploy(0*TENPOW18, {'from':accounts[0]})    

@pytest.fixture(scope='module', autouse=True)
def staking_rewards_mock(DigitalaxRewards,MockStaking, mona_token, access_controls, staking_genesis_mock, staking_nft_mock, staking_lp_mock):
    start_time = chain.time() 
    staking_rewards_mock = DigitalaxRewards.deploy(
                mona_token,
                access_controls,
                staking_genesis_mock,
                staking_nft_mock,
                staking_lp_mock,
                start_time,
                start_time,0,0,0,
                {'from':accounts[0]}
    )
    access_controls.addMinterRole(staking_rewards_mock)
    assert access_controls.hasMinterRole(staking_rewards_mock) == True
    staking_genesis_mock.setRewardsContract(staking_rewards_mock)
    staking_nft_mock.setRewardsContract(staking_rewards_mock)
    staking_lp_mock.setRewardsContract(staking_rewards_mock)

    weeks = [0,1,2,3,4,5]
    rewards = [700*TENPOW18,700*TENPOW18,500*TENPOW18,350*TENPOW18,150*TENPOW18,100*TENPOW18]
    staking_rewards_mock.setRewards(weeks,rewards)

    weeks = [0,1]
    rewards = [450*TENPOW18,350*TENPOW18]
    staking_rewards_mock.bonusRewards(staking_genesis_mock,weeks,rewards)

    return staking_rewards_mock


@pytest.fixture(scope='module', autouse=True)
def staking_rewards(DigitalaxRewards,mona_token,access_controls,staked_nft,staking_genesis,staking_nft,staking_lp_mock):
    start_time = chain.time() 
    staking_rewards = DigitalaxRewards.deploy(
                mona_token,
                access_controls,
                staking_genesis,
                staking_nft,
                staking_lp_mock,
                start_time,
                start_time,0,0,0,
                {'from':accounts[0]}
    )
    access_controls.addMinterRole(staking_rewards)
    assert access_controls.hasMinterRole(staking_rewards) == True
    staking_genesis.setRewardsContract(staking_rewards)
    # staking_nft.setRewardsContract(staking_rewards)
    # staking_lp.setRewardsContract(staking_rewards)

    weeks = [0,1,2,3,4,5]
    rewards = [700*TENPOW18,700*TENPOW18,500*TENPOW18,350*TENPOW18,150*TENPOW18,100*TENPOW18]
    staking_rewards.setRewards(weeks,rewards)

    weeks = [0,1]
    rewards = [450*TENPOW18,350*TENPOW18]
    staking_rewards.bonusRewards(staking_genesis,weeks,rewards)

    chain.sleep(GENESIS_AUCTION_TIME +20)
    chain.mine()
    staking_genesis.setTokensClaimable(True, {'from':accounts[0]})
    for tokenId in range(1,7):
        staked_nft.setApprovalForAll(staking_genesis, True, {'from':accounts[tokenId]})
        staking_genesis.stake(tokenId,{'from':accounts[tokenId]})
    
    totalEth =  (1.5 +0.1 +0.2 +1 +1 +1.7)*TENPOW18
   
    #Ask why there is 200 more wei
    assert staking_genesis.stakedEthTotal() == totalEth

    return staking_rewards

