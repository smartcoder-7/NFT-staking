from brownie import *
from .settings import *
from .contracts import *
from .contract_addresses import *
import time

from .deploy_setRewards import *
from .deploy_setBonus import *
from .deploy_setContributions import *

def main():
    # Acocunts
    load_accounts()
    funds_multisig = CONTRACTS[network.show_active()]["fund_multisig"]
    treasury = CONTRACTS[network.show_active()]["fund_multisig"]
    # AG: Get these parameters for Mainnet

    
    # MONA Token
    access_control = deploy_access_control()
    mona_token = deploy_mona_token(access_control, MONA_SYMBOL, MONA_NAME, treasury, MONA_TREASURY_SUPPLY + MONA_UNISWAP_SUPPLY, MONA_TOKEN_CAP)

    # mona_token.transfer(treasury, MONA_TREASURY_SUPPLY, {'from':accounts[0]})

    # # Uniswap Pool
    weth_token = get_weth_token()
    # lp_token = deploy_uniswap_pool(mona_token, weth_token)
    lp_token = get_uniswap_pool()
    print("Uniswap Pool Token (LP): ", str(lp_token))

    # Initial ETH deposit
    # weth_token.deposit({'from': accounts[0], 'value': '10 ether'})
    # mona_token.transfer(lp_token, MONA_UNISWAP_SUPPLY, {'from':accounts[0]})
    # weth_token.transfer( lp_token,'10 ether',{'from':accounts[0]})
    # lp_token.mint(treasury,{'from':accounts[0]})

    #AG: need to add some liquidity

    # Staking Tokens
    genesis_nft = get_genesis_nft()
    parent_nft = get_parent_nft()

    # Staking Contracts 
    genesis_staking = deploy_genesis_staking(funds_multisig, mona_token,genesis_nft,access_control)
    parent_staking = deploy_parent_staking(mona_token,parent_nft,access_control)
    lp_staking = deploy_lp_staking(mona_token,lp_token,weth_token,access_control)

    # Set Genesis Contributions
    token_id = 356
    genesis_contribution = genesis_staking.getGenesisContribution(token_id)
    if genesis_contribution == 0 :
        set_contributions(genesis_staking)

    token_id = 356
    genesis_contribution = genesis_staking.getGenesisContribution(token_id)
    print("genesis contribution for token[",token_id,"]",genesis_contribution)

    # # Rewards Contract
    rewards = deploy_rewards(mona_token,genesis_staking,parent_staking,lp_staking,access_control,REWARDS_START_TIME)
    if rewards.weeklyRewardsPerSecond(0) == 0:
        set_bonus(genesis_staking, rewards)
        set_rewards(rewards)
        print("rewards per second for week[0] =",rewards.weeklyRewardsPerSecond(0)* 7*24*60*60 /TENPOW18)
        print("rewards per second for week[8]=",rewards.weeklyRewardsPerSecond(8)* 7*24*60*60/TENPOW18)

    # # Set Rewards contract
    genesis_staking.setRewardsContract(rewards,{'from': accounts[0]})
    parent_staking.setRewardsContract(rewards,{'from': accounts[0]})
    lp_staking.setRewardsContract(rewards,{'from': accounts[0]}) 

    # # Set Minter permissions 
    access_control.addMinterRole(rewards, {'from': accounts[0]})

