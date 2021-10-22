// SPDX-License-Identifier: GPLv2

pragma solidity 0.6.12;

import "@openzeppelin/contracts/math/SafeMath.sol";
import "../DreamAccessControls.sol";
import "../DreamGenesisNFT.sol";
import "../../interfaces/IERC20.sol";

/**
 * @title Dream Staking
 * @dev Stake NFTs, earn tokens on the Digitialax platform
 * @author Adrian Guerrera (deepyr)
 */

/// @dev an interface to interact with the Genesis MONA NFT that will
interface IDreamGenesisNFT {
    function contribution(address user) external view returns (uint256);

    function totalContributions() external view returns (uint256);

    function tokenOfOwnerByIndex(address owner, uint256 index)
        external
        view
        returns (uint256);

    function balanceOf(address owner) external view returns (uint256);

    function safeTransferFrom(
        address from,
        address to,
        uint256 tokenId
    ) external;
}

/// @dev an interface to interact with the Genesis MONA NFT that will
interface IDreamRewards {
    function updateRewards() external returns (bool);

    function genesisRewards(uint256 _from, uint256 _to)
        external
        view
        returns (uint256);

    function parentRewards(uint256 _from, uint256 _to)
        external
        view
        returns (uint256);

    function LPRewards(uint256 _from, uint256 _to)
        external
        view
        returns (uint256);

    function lastRewardTime() external view returns (uint256);
}

contract MockStaking {
    using SafeMath for uint256;
    bytes4 private constant _ERC721_RECEIVED = 0x150b7a02;

    /// @notice
    IERC20 public rewardsToken;
    IDreamGenesisNFT public genesisNFT;
    DreamAccessControls public accessControls;
    IDreamRewards public rewardsContract;

    // @notice all funds will be sent to this address pon purchase of a Genesis NFT
    address payable public fundsMultisig;

    /// @notice total ethereum staked currently in the gensesis staking contract
    uint256 public stakedEthTotal;
    uint256 public lastUpdateTime;

    uint256 public rewardsPerTokenPoints;
    uint256 public totalUnclaimedRewards;

    uint256 constant pointMultiplier = 10e32;

    /**
    @notice to track what user is staking what tokens
    @notice tokenIds are all the tokens staked by the staker
    @notice balance is the current ether balance of the staker
    @notice rewardsEarned is the total reward for the staker till now
    @notice rewardsReleased is how much reward has been paid to the staker
    */
    struct Staker {
        uint256[] tokenIds;
        mapping(uint256 => uint256) tokenIndex;
        uint256 balance;
        uint256 lastRewardPoints;
        uint256 rewardsEarned;
        uint256 rewardsReleased;
    }

    /// @notice mapping of a staker to its current properties
    mapping(address => Staker) public stakers;

    // Mapping from token ID to owner address
    mapping(uint256 => address) public tokenOwner;

    /// @notice tokenId => amount contributed
    mapping(uint256 => uint256) public contribution;
    uint256 public totalContributions;
    // @notice the maximum accumulative amount a user can contribute to the genesis sale
    uint256 public constant maximumContributionAmount = 2 ether;

    /// @notice sets the token to be claimable or not, cannot claim if it set to false
    bool public tokensClaimable;

    /// @notice event emitted when a user has staked a token
    event Staked(address owner, uint256 amount);

    /// @notice event emitted when a user has unstaked a token
    event Unstaked(address owner, uint256 amount);

    /// @notice event emitted when a user claims reward
    event RewardPaid(address indexed user, uint256 reward);

    /// @notice
    event ClaimableStatusUpdated(bool _status);

    // @notice event emitted when a contributors amount is increased
    event ContributionIncreased(uint256 indexed tokenId, uint256 contribution);

    constructor(uint256 _stakedEthTotal) public {
        stakedEthTotal = _stakedEthTotal;
    }

    /**
     * @dev Single gateway to intialize the staking contract after deploying
     * @dev Sets the contract with the MONA genesis nfts and a reward token so that they can be used for staking and giving out reward
     */
    function initGenesisStaking(
        address payable _fundsMultisig,
        IERC20 _rewardsToken,
        IDreamGenesisNFT _genesisNFT,
        DreamAccessControls _accessControls
    ) public {
        // AG: require !init
        fundsMultisig = _fundsMultisig;
        rewardsToken = _rewardsToken;
        genesisNFT = _genesisNFT;
        accessControls = _accessControls;
    }

    function setRewardsContract(address _addr) public {
        require(_addr != address(0));
        rewardsContract = IDreamRewards(_addr);
    }

    // AG add setters for reward tokens
    function setTokensClaimable(bool _enabled) public {
        tokensClaimable = _enabled;
        emit ClaimableStatusUpdated(_enabled);
    }

    function setStakedEthTotal(uint256 _stakedEthTotal) public {
        stakedEthTotal = _stakedEthTotal;
    }
}
