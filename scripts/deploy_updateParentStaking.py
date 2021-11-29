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
    mona_token = get_mona_token()

    # Staking Token
    parent_nft = get_parent_nft()

    # Parent Staking Contract 
    parent_staking = DreamNFTStaking.deploy({'from': accounts[0]})
    parent_staking.initStaking(mona_token, parent_nft, access_control, {'from': accounts[0]})
    
    rewards = get_rewards()
    # # Set Rewards contract
    parent_staking.setRewardsContract(rewards,{'from': accounts[0]})    
    rewards.setParentStaking(parent_staking,{'from': accounts[0]})
    parent_staking.setTokensClaimable(True, {'from':accounts[0]})

