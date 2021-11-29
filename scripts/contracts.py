from brownie import *
from .settings import *
from .contract_addresses import *

def load_accounts():
    if network.show_active() == 'mainnet':
        # replace with your keys
        accounts.load("digitalax")
    # add accounts if active network is goerli
    if network.show_active() in ['goerli', 'ropsten','kovan','rinkeby']:
        # 0x2A40019ABd4A61d71aBB73968BaB068ab389a636
        accounts.add('4ca89ec18e37683efa18e0434cd9a28c82d461189c477f5622dae974b43baebf')
        # 0x1F3389Fc75Bf55275b03347E4283f24916F402f7
        accounts.add('fa3c06c67426b848e6cef377a2dbd2d832d3718999fbe377236676c9216d8ec0')

def deploy_access_control():
    access_control_address = CONTRACTS[network.show_active()]["access_control"]
    if access_control_address == '':
        access_control = DigitalaxAccessControls.deploy({'from': accounts[0]})
    else:
        access_control = DigitalaxAccessControls.at(access_control_address)
    # new_admin = web3.toChecksumAddress('0x66d7Dd55646100541F2B6ec15781b6d4C8372b1c')
    # access_control.addAdminRole(new_admin, {'from': accounts[0]})
    return access_control

def deploy_uniswap_pool(tokenA, tokenB):
    uniswap_pool_address = CONTRACTS[network.show_active()]["lp_token"]
    if uniswap_pool_address == '':
        uniswap_factory = interface.IUniswapV2Factory(UNISWAP_FACTORY)
        tx = uniswap_factory.createPair(tokenA, tokenB, {'from': accounts[0]})
        assert 'PairCreated' in tx.events
        uniswap_pool = interface.IUniswapV2Pair(web3.toChecksumAddress(tx.events['PairCreated']['pair']))
    else:
        uniswap_pool = interface.IUniswapV2Pair(uniswap_pool_address)
    return uniswap_pool

def get_uniswap_pool():
    uniswap_pool_address = CONTRACTS[network.show_active()]["lp_token"]
    return interface.IUniswapV2Pair(uniswap_pool_address)

def deploy_mona_token(access_control, symbol, name, treasury, initial_supply ,cap):
    mona_token_address = CONTRACTS[network.show_active()]["mona_token"]
    if mona_token_address == '':
        decimals = 18
        mona_token = MONA.deploy(symbol, name, decimals,access_control, treasury, initial_supply, {'from': accounts[0]})
        mona_token.setCap(cap, False, {'from': accounts[0]})
    else:
        mona_token = MONA.at(mona_token_address)
    return mona_token

def get_mona_token():
    mona_token_address = CONTRACTS[network.show_active()]["mona_token"]
    return MONA.at(mona_token_address)

def deploy_weth_token():
    weth_token_address = CONTRACTS[network.show_active()]["weth"]
    if weth_token_address == '':
        weth_token = WETH9.deploy({'from': accounts[0]})
    else:
        weth_token = WETH9.at(weth_token_address)
    return weth_token

def get_weth_token():
    weth_token_address = web3.toChecksumAddress(CONTRACTS[network.show_active()]["weth"])
    return WETH9.at(weth_token_address)

def deploy_genesis_nft(funds_multisig, access_control, start_time, end_time):
    genesis_nft_address = CONTRACTS[network.show_active()]["genesis_nft"]
    if genesis_nft_address == "":
        genesis_nft = DigitalaxGenesisNFT.deploy(
                                access_control
                                , funds_multisig
                                , start_time
                                , end_time
                                , GENESIS_TOKEN_URI
                                , {'from': accounts[0]})
    else:
        genesis_nft = DigitalaxGenesisNFT.at(genesis_nft_address)
    return genesis_nft

def get_genesis_nft():
    genesis_nft_address = web3.toChecksumAddress(CONTRACTS[network.show_active()]["genesis_nft"])
    return DigitalaxGenesisNFT.at(genesis_nft_address)

def deploy_child_nft(funds_multisig):
    child_nft_address = CONTRACTS[network.show_active()]["child_nft"]
    if child_nft_address == "":
        child_nft = DigitalaxMaterials.deploy(
                                MATERIAL_NAME
                                , MATERIAL_SYMBOL
                                , funds_multisig
                                , {'from': accounts[0]})
    else:
        child_nft = DigitalaxMaterials.at(child_nft_address)
    return child_nft

def deploy_parent_nft(access_control,child_nft):
    parent_nft_address = CONTRACTS[network.show_active()]["parent_nft"]
    if parent_nft_address == "":
        parent_nft = DigitalaxGarmentNFT.deploy(
                                access_control
                                , child_nft
                                , {'from': accounts[0]})
    else:
        parent_nft = DigitalaxGarmentNFT.at(parent_nft_address)
    return parent_nft

def get_parent_nft():
    parent_nft_address = web3.toChecksumAddress(CONTRACTS[network.show_active()]["parent_nft"])
    return DigitalaxGarmentNFT.at(parent_nft_address)

def deploy_genesis_staking(funds_multisig, rewards_token, genesis_nft, access_control):
    genesis_staking_address = CONTRACTS[network.show_active()]["genesis_staking"]
    if genesis_staking_address == "":
        genesis_staking = DigitalaxGenesisStaking.deploy({'from': accounts[0]})
        genesis_staking.initGenesisStaking(funds_multisig, rewards_token, genesis_nft, access_control,{'from': accounts[0]})
    else:
        genesis_staking = DigitalaxGenesisStaking.at(genesis_staking_address)
    return genesis_staking

def get_genesis_staking():
    genesis_staking_address = CONTRACTS[network.show_active()]["genesis_staking"]
    genesis_staking = DigitalaxGenesisStaking.at(genesis_staking_address)
    return genesis_staking

def deploy_parent_staking(rewards_token, nft_token, access_control):
    parent_staking_address = CONTRACTS[network.show_active()]["parent_staking"]
    if parent_staking_address == "":
        parent_staking = DigitalaxNFTStaking.deploy({'from': accounts[0]})
        parent_staking.initStaking(rewards_token, nft_token, access_control,{'from': accounts[0]})
    else:
        parent_staking = DigitalaxNFTStaking.at(parent_staking_address)
    return parent_staking

def get_parent_staking():
    parent_staking_address = CONTRACTS[network.show_active()]["parent_staking"]
    parent_staking = DigitalaxNFTStaking.at(parent_staking_address)
    return parent_staking

def deploy_lp_staking(rewards_token, lp_token,weth_token, access_control):
    lp_staking_address = CONTRACTS[network.show_active()]["lp_staking"]
    lp_token_address = CONTRACTS[network.show_active()]["lp_token"]

    if lp_staking_address == "":
        lp_staking = DigitalaxLPStaking.deploy({'from': accounts[0]})
        lp_staking.initLPStaking(rewards_token, lp_token, weth_token, access_control,{'from': accounts[0]})
    else:
        lp_staking = DigitalaxLPStaking.at(lp_staking_address)
    return lp_staking

def get_lp_staking():
    lp_staking_address = CONTRACTS[network.show_active()]["lp_staking"]
    lp_staking = DigitalaxLPStaking.at(lp_staking_address)
    return lp_staking


def deploy_rewards(rewards_token,genesis_staking,parent_staking,lp_staking, access_control, start_time,last_time, g_paid, p_paid, lp_paid):
    rewards_address = CONTRACTS[network.show_active()]["rewards_contract"]
    if rewards_address == "":
        rewards = DigitalaxRewards.deploy(rewards_token,
                                        access_control,
                                        genesis_staking,
                                        parent_staking,
                                        lp_staking,
                                        start_time,
                                        last_time,
                                        g_paid,
                                        p_paid,
                                        lp_paid,
                                        {'from': accounts[0]})
    else:
        rewards = DigitalaxRewards.at(rewards_address)
    return rewards


def deploy_new_rewards(rewards_token,genesis_staking,parent_staking,lp_staking, access_control, start_time,last_time, g_paid, p_paid, lp_paid):
    rewards_address = CONTRACTS[network.show_active()]["rewards_contract"]
    rewards = DigitalaxRewards.deploy(rewards_token,
                                        access_control,
                                        genesis_staking,
                                        parent_staking,
                                        lp_staking,
                                        start_time,
                                        last_time,
                                        g_paid,
                                        p_paid,
                                        lp_paid,
                                        {'from': accounts[0]})
    return rewards


def get_rewards():
    rewards_address = CONTRACTS[network.show_active()]["rewards_contract"]
    rewards = DigitalaxRewards.at(rewards_address)
    return rewards