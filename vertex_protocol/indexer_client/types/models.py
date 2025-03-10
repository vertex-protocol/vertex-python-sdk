from enum import IntEnum
from vertex_protocol.utils.enum import StrEnum

from typing import Any, Optional, Union
from vertex_protocol.engine_client.types.models import (
    PerpProduct,
    PerpProductBalance,
    SpotProduct,
    SpotProductBalance,
)

from vertex_protocol.utils.model import VertexBaseModel


class IndexerEventType(StrEnum):
    LIQUIDATE_SUBACCOUNT = "liquidate_subaccount"
    DEPOSIT_COLLATERAL = "deposit_collateral"
    WITHDRAW_COLLATERAL = "withdraw_collateral"
    SETTLE_PNL = "settle_pnl"
    MATCH_ORDERS = "match_orders"
    MATCH_ORDER_A_M_M = "match_order_a_m_m"
    SWAP_AMM = "swap_a_m_m"
    MINT_LP = "mint_lp"
    BURN_LP = "burn_lp"
    MANUAL_ASSERT = "manual_assert"
    LINK_SIGNER = "link_signer"
    TRANSFER_QUOTE = "transfer_quote"
    CREATE_ISOLATED_SUBACCOUNT = "create_isolated_subaccount"


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


class IndexerBaseModel(VertexBaseModel):
    submission_idx: str
    timestamp: Optional[str]


class IndexerBaseOrder(VertexBaseModel):
    sender: str
    priceX18: str
    amount: str
    expiration: Union[str, int]
    nonce: Union[str, int]


class IndexerOrderFill(IndexerBaseModel):
    digest: str
    base_filled: str
    quote_filled: str
    fee: str


class IndexerHistoricalOrder(IndexerOrderFill):
    subaccount: str
    product_id: int
    amount: str
    price_x18: str
    expiration: str
    nonce: str
    isolated: bool


class IndexerSignedOrder(VertexBaseModel):
    order: IndexerBaseOrder
    signature: str


class IndexerMatch(IndexerOrderFill):
    order: IndexerBaseOrder
    cumulative_fee: str
    cumulative_base_filled: str
    cumulative_quote_filled: str
    isolated: bool


class IndexerMatchOrdersTxData(VertexBaseModel):
    product_id: int
    amm: bool
    taker: IndexerSignedOrder
    maker: IndexerSignedOrder


class IndexerMatchOrdersTx(VertexBaseModel):
    match_orders: IndexerMatchOrdersTxData


class IndexerWithdrawCollateralTxData(VertexBaseModel):
    sender: str
    product_id: int
    amount: str
    nonce: int


class IndexerWithdrawCollateralTx(VertexBaseModel):
    withdraw_collateral: IndexerWithdrawCollateralTxData


class IndexerLiquidateSubaccountTxData(VertexBaseModel):
    sender: str
    liquidatee: str
    mode: int
    health_group: int
    amount: str
    nonce: int


class IndexerLiquidateSubaccountTx(VertexBaseModel):
    liquidate_subaccount: IndexerLiquidateSubaccountTxData


class IndexerMintLpTxData(VertexBaseModel):
    sender: str
    product_id: int
    amount_base: str
    quote_amount_low: str
    quote_amount_high: str
    nonce: int


class IndexerMintLpTx(VertexBaseModel):
    mint_lp: IndexerMintLpTxData


class IndexerBurnLpTxData(VertexBaseModel):
    sender: str
    product_id: int
    amount: str
    nonce: int


class IndexerBurnLpTx(VertexBaseModel):
    burn_lp: IndexerBurnLpTxData


IndexerTxData = Union[
    IndexerMatchOrdersTx,
    IndexerWithdrawCollateralTx,
    IndexerLiquidateSubaccountTx,
    IndexerMintLpTx,
    IndexerBurnLpTx,
]


class IndexerTx(IndexerBaseModel):
    tx: Union[IndexerTxData, Any]


class IndexerSpotProductBalanceData(VertexBaseModel):
    spot: SpotProductBalance


class IndexerPerpProductBalanceData(VertexBaseModel):
    perp: PerpProductBalance


IndexerProductBalanceData = Union[
    IndexerSpotProductBalanceData, IndexerPerpProductBalanceData
]


class IndexerSpotProductData(VertexBaseModel):
    spot: SpotProduct


class IndexerPerpProductData(VertexBaseModel):
    perp: PerpProduct


IndexerProductData = Union[IndexerSpotProductData, IndexerPerpProductData]


class IndexerEventTrackedData(VertexBaseModel):
    net_interest_unrealized: str
    net_interest_cumulative: str
    net_funding_unrealized: str
    net_funding_cumulative: str
    net_entry_unrealized: str
    net_entry_cumulative: str
    net_entry_lp_unrealized: str
    net_entry_lp_cumulative: str


class IndexerEvent(IndexerBaseModel, IndexerEventTrackedData):
    subaccount: str
    product_id: int
    event_type: IndexerEventType
    product: IndexerProductData
    pre_balance: IndexerProductBalanceData
    post_balance: IndexerProductBalanceData
    isolated: bool
    isolated_product_id: Optional[int]


class IndexerProduct(IndexerBaseModel):
    product_id: int
    product: IndexerProductData


class IndexerMarketSnapshot(VertexBaseModel):
    timestamp: int
    cumulative_users: int
    daily_active_users: int
    tvl: str

    # product_id -> cumulative_metric
    cumulative_trades: dict
    cumulative_volumes: dict
    cumulative_trade_sizes: dict
    cumulative_sequencer_fees: dict
    cumulative_maker_fees: dict
    cumulative_liquidation_amounts: dict
    open_interests: dict
    total_deposits: dict
    total_borrows: dict
    funding_rates: dict
    deposit_rates: dict
    borrow_rates: dict
    cumulative_inflows: dict
    cumulative_outflows: dict


class IndexerCandlestick(IndexerBaseModel):
    product_id: int
    granularity: int
    open_x18: str
    high_x18: str
    low_x18: str
    close_x18: str
    volume: str


class IndexerOraclePrice(VertexBaseModel):
    product_id: int
    oracle_price_x18: str
    update_time: str


class IndexerAddressReward(VertexBaseModel):
    product_id: int
    q_score: str
    sum_q_min: str
    uptime: int
    maker_volume: str
    taker_volume: str
    maker_fee: str
    taker_fee: str
    maker_tokens: str
    taker_tokens: str
    taker_referral_tokens: str
    rebates: str


class IndexerGlobalRewards(VertexBaseModel):
    product_id: int
    reward_coefficient: str
    q_scores: str
    maker_volumes: str
    taker_volumes: str
    maker_fees: str
    taker_fees: str
    maker_tokens: str
    taker_tokens: str


class IndexerTokenReward(VertexBaseModel):
    epoch: int
    start_time: str
    period: str
    address_rewards: list[IndexerAddressReward]
    global_rewards: list[IndexerGlobalRewards]


class IndexerMarketMakerData(VertexBaseModel):
    timestamp: str
    maker_fee: str
    uptime: str
    sum_q_min: str
    q_score: str
    maker_share: str
    expected_maker_reward: str


class IndexerMarketMaker(VertexBaseModel):
    address: str
    data: list[IndexerMarketMakerData]


class IndexerLiquidatableAccount(VertexBaseModel):
    subaccount: str
    update_time: int


class IndexerSubaccount(VertexBaseModel):
    id: str
    subaccount: str


class IndexerMerkleProof(VertexBaseModel):
    total_amount: str
    proof: list[str]


class IndexerPayment(VertexBaseModel):
    product_id: int
    idx: str
    timestamp: str
    amount: str
    balance_amount: str
    rate_x18: str
    oracle_price_x18: str


class IndexerTickerInfo(VertexBaseModel):
    ticker_id: str
    base_currency: str
    quote_currency: str
    last_price: float
    base_volume: float
    quote_volume: float
    price_change_percent_24h: float


class IndexerPerpContractInfo(IndexerTickerInfo):
    product_type: str
    contract_price: float
    contract_price_currency: str
    open_interest: float
    open_interest_usd: float
    index_price: float
    mark_price: float
    funding_rate: float
    next_funding_rate_timestamp: int


class IndexerTradeInfo(VertexBaseModel):
    ticker_id: str
    # submission_idx
    trade_id: int
    price: float
    base_filled: float
    quote_filled: float
    timestamp: int
    # side
    trade_type: str


class MarketType(StrEnum):
    SPOT = "spot"
    PERP = "perp"


class VrtxTokenQueryType(StrEnum):
    TOTAL_SUPPLY = "total_supply"
    CIRCULATING_SUPPLY = "circulating_supply"
