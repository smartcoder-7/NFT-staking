from brownie import *

from brownie import network
from brownie.network.gas.strategies import GasNowScalingStrategy
from brownie.network import gas_price
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

    gas_strategy = GasNowScalingStrategy("fast", increment=1.2)
    gas_price(gas_strategy)

    # MONA Token
    access_control = deploy_access_control()
    mona_token = get_mona_token()

    # Get Contracts 
    genesis_staking = get_genesis_staking()
    parent_staking = get_parent_staking()
    lp_staking = get_lp_staking()
    rewards = get_rewards()

    # # Set Tokens Claimable
    genesis_staking.setTokensClaimable(False, {'from':accounts[0]})
    parent_staking.setTokensClaimable(False, {'from':accounts[0]})
    lp_staking.setTokensClaimable(False, {'from':accounts[0]})

    # Accounting snapshot
    last_rewards = rewards.lastRewardTime({'from':accounts[0]})
    print("Last Rewards: ", str(last_rewards))

    genesis_paid = rewards.genesisRewardsPaid({'from':accounts[0]})
    parent_paid = rewards.parentRewardsPaid({'from':accounts[0]})
    lp_paid = rewards.lpRewardsPaid({'from':accounts[0]})
    print("Rewards Paid: G:", str(genesis_paid), " P:", str(parent_paid), " L:",str(lp_paid))

    week_points0 = rewards.weeklyWeightPoints(0, {'from':accounts[0]})
    print("Weekly Points0:", str(week_points0))
    week_points1 = rewards.weeklyWeightPoints(1, {'from':accounts[0]})
    print("Weekly Points1:", str(week_points1))

    # # Rewards Contract
    new_rewards = deploy_new_rewards(mona_token,genesis_staking,parent_staking,lp_staking,
                                    access_control,REWARDS_START_TIME, last_rewards,
                                     genesis_paid, parent_paid, lp_paid)

    # Set weekly rewards
    set_bonus(genesis_staking, new_rewards)
    set_rewards(new_rewards)
    print("rewards per second for week[0] =",new_rewards.weeklyRewardsPerSecond(0)* 7*24*60*60 /TENPOW18)
    print("rewards per second for week[8]=",new_rewards.weeklyRewardsPerSecond(8)* 7*24*60*60/TENPOW18)

    new_rewards.setInitialPoints(0, week_points0[0], week_points0[1], week_points0[2],{'from': accounts[0]})
    new_rewards.setInitialPoints(1, week_points1[0], week_points1[1], week_points1[2],{'from': accounts[0]})

    # Add Minter permissions 
    access_control.addMinterRole(new_rewards, {'from': accounts[0]})

    # Set Rewards contract on staking pooks
    genesis_staking.setRewardsContract(new_rewards,{'from': accounts[0]})
    parent_staking.setRewardsContract(new_rewards,{'from': accounts[0]})
    lp_staking.setRewardsContract(new_rewards,{'from': accounts[0]}) 

    # Set Tokens Claimable
    genesis_staking.setTokensClaimable(True, {'from':accounts[0]})
    parent_staking.setTokensClaimable(True, {'from':accounts[0]})
    lp_staking.setTokensClaimable(True, {'from':accounts[0]})

    # Refresh the updated time to check it works
    new_rewards.updateRewards({'from': accounts[0]})
