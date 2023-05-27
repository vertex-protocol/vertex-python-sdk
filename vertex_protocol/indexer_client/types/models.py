from enum import Enum, IntEnum


class IndexerEventType(str, Enum):
    LIQUIDATE_SUBACCOUNT = "liquidate_subaccount"
    DEPOSIT_COLLATERAL = "deposit_collateral"
    WITHDRAW_COLLATERAL = "withdraw_collateral"
    SETTLE_PNL = "settle_pnl"
    MATCH_ORDERS = "match_orders"
    MINT_LP = "mint_lp"
    BURN_LP = "burn_lp"


class IndexerCandlesticksGranularity(IntEnum):
    ONE_MINUTE = 60
    FIVE_MINUTES = 300
    FIFTEEN_MINUTES = 900
    ONE_HOUR = 3600
    TWO_HOURS = 7200
    FOUR_HOURS = 14400
    ONE_DAY = 86400
    ONE_WEEK = 604800
    FOUR_WEEKS = 2419200
