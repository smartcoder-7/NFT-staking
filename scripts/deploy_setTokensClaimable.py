from brownie import *
from .settings import *
from .contracts import *
from .contract_addresses import *
import time


def main():
    load_accounts()

    # Get Contracts 
    genesis_staking = get_genesis_staking()
    parent_staking = get_parent_staking()
    lp_staking = get_lp_staking()

    # Set Tokens Claimable
    genesis_staking.setTokensClaimable(True, {'from':accounts[0]})
    parent_staking.setTokensClaimable(True, {'from':accounts[0]})
    lp_staking.setTokensClaimable(True, {'from':accounts[0]})
