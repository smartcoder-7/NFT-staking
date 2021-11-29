from brownie import *
from .settings import *
from .contracts import *
from .contract_addresses import *
import time

from .deploy_setRewards import *
from .deploy_setContributions import *
from .deploy_setBonus import *
from .deploy_setRewards import *

def main():
    # Acocunts
    load_accounts()
    funds_multisig = accounts[0]
    treasury = accounts[0]
    # AG: Get these parameters for Mainnet
    # treasury = web3.toChecksumAddress('0x66d7Dd55646100541F2B6ec15781b6d4C8372b1c')

    genesis_start_time = chain.time() +10
    genesis_end_time = chain.time() + 100
    start_time = chain.time()
    
    # MONA Token
    access_control = deploy_access_control()
    mona_token = deploy_mona_token(access_control, MONA_SYMBOL, MONA_NAME, treasury, MONA_TREASURY_SUPPLY, MONA_TOKEN_CAP)

    # Uniswap Pool
    weth_token = deploy_weth_token()
    lp_token = deploy_uniswap_pool(mona_token, weth_token)
    print("Uniswap Pool Token (LP): ", str(lp_token))

    # Initial ETH deposit
    # weth_token.deposit({'from': accounts[0], 'value': '0.011 ether'})
    # mona_token.transfer(lp_token, 20 * 10**18, {'from':accounts[0]})
    # weth_token.transfer( lp_token,'0.010 ether',{'from':accounts[0]})
    # lp_token.mint(treasury,{'from':accounts[0]})

    #AG: need to add some liquidity

    # Staking Tokens
    genesis_nft = deploy_genesis_nft(funds_multisig, access_control, genesis_start_time, genesis_end_time)
    child_nft = deploy_child_nft(funds_multisig)
    parent_nft = deploy_parent_nft(access_control, child_nft)
  
    # Staking Contracts 
    # genesis_staking = CONTRACTS[network.show_active()]["genesis_staking"]
    genesis_staking = deploy_genesis_staking(funds_multisig, mona_token,genesis_nft,access_control)
    lp_staking = deploy_lp_staking(mona_token,lp_token,weth_token,access_control)
    parent_staking = deploy_parent_staking(mona_token,parent_nft,access_control)

    # Rewards Contract
    rewards = deploy_rewards(mona_token,genesis_staking,parent_staking,lp_staking,access_control,start_time, 0, 0, 0, 0)
    if rewards.weeklyRewardsPerSecond(0) == 0:
        set_bonus(genesis_staking, rewards)
        rewards = set_rewards(rewards)
        print("rewards per second for week[0] =",rewards.weeklyRewardsPerSecond(0)* 7*24*60*60 /TENPOW18)
        print("rewards per second for week[8]=",rewards.weeklyRewardsPerSecond(8)* 7*24*60*60/TENPOW18)

    # Set Rewards contract
    genesis_staking.setRewardsContract(rewards,{'from': accounts[0]})
    parent_staking.setRewardsContract(rewards,{'from': accounts[0]})
    lp_staking.setRewardsContract(rewards,{'from': accounts[0]}) 

    # Set Minter permissions 
    access_control.addMinterRole(rewards, {'from': accounts[0]})

    # Set Genesis Contributions 
    set_contributions(genesis_staking)

    token_id = 1
    genesis_contribution = genesis_staking.getGenesisContribution(token_id)
    print("genesis contribution for token[",token_id,"]",genesis_contribution)

    # rewards.up
