from typing import Union
from typing import Annotated
from vertex_protocol.utils.enum import StrEnum
from vertex_protocol.utils.model import VertexBaseModel
from pydantic import conlist


class ResponseStatus(StrEnum):
    SUCCESS = "success"
    FAILURE = "failure"


class EngineStatus(StrEnum):
    ACTIVE = "active"
    FAILED = "failed"


class MintLp(VertexBaseModel):
    product_id: int
    subaccount: str
    amount_base: str
    quote_amount_low: str
    quote_amount_high: str


class BurnLp(VertexBaseModel):
    product_id: int
    subaccount: str
    amount_lp: str


class ApplyDelta(VertexBaseModel):
    product_id: int
    subaccount: str
    amount_delta: str
    v_quote_delta: str


class MintLpTx(VertexBaseModel):
    mint_lp: MintLp


class BurnLpTx(VertexBaseModel):
    burn_lp: BurnLp


class ApplyDeltaTx(VertexBaseModel):
    apply_delta: ApplyDelta


class SubaccountHealth(VertexBaseModel):
    assets: str
    liabilities: str
    health: str


class SpotLpBalance(VertexBaseModel):
    amount: str


class SpotBalance(VertexBaseModel):
    amount: str
    last_cumulative_multiplier_x18: str


class SpotProductBalance(VertexBaseModel):
    product_id: int
    lp_balance: SpotLpBalance
    balance: SpotBalance


class PerpLpBalance(VertexBaseModel):
    amount: str
    last_cumulative_funding_x18: str


class PerpBalance(VertexBaseModel):
    amount: str
    v_quote_balance: str
    last_cumulative_funding_x18: str


class PerpProductBalance(VertexBaseModel):
    product_id: int
    lp_balance: PerpLpBalance
    balance: PerpBalance


class ProductRisk(VertexBaseModel):
    long_weight_initial_x18: str
    short_weight_initial_x18: str
    long_weight_maintenance_x18: str
    short_weight_maintenance_x18: str
    large_position_penalty_x18: str


class ProductBookInfo(VertexBaseModel):
    size_increment: str
    price_increment_x18: str
    min_size: str
    collected_fees: str
    lp_spread_x18: str


class BaseProduct(VertexBaseModel):
    product_id: int
    oracle_price_x18: str
    risk: ProductRisk
    book_info: ProductBookInfo


class BaseProductLpState(VertexBaseModel):
    supply: str


class SpotProductConfig(VertexBaseModel):
    token: str
    interest_inflection_util_x18: str
    interest_floor_x18: str
    interest_small_cap_x18: str
    interest_large_cap_x18: str


class SpotProductState(VertexBaseModel):
    cumulative_deposits_multiplier_x18: str
    cumulative_borrows_multiplier_x18: str
    total_deposits_normalized: str
    total_borrows_normalized: str


class SpotProductLpAmount(VertexBaseModel):
    amount: str
    last_cumulative_multiplier_x18: str


class SpotProductLpState(BaseProductLpState):
    quote: SpotProductLpAmount
    base: SpotProductLpAmount


class SpotProduct(BaseProduct):
    config: SpotProductConfig
    state: SpotProductState
    lp_state: SpotProductLpState


class PerpProductState(VertexBaseModel):
    cumulative_funding_long_x18: str
    cumulative_funding_short_x18: str
    available_settle: str
    open_interest: str


class PerpProductLpState(BaseProductLpState):
    last_cumulative_funding_x18: str
    cumulative_funding_per_lp_x18: str
    base: str
    quote: str


class PerpProduct(BaseProduct):
    state: PerpProductState
    lp_state: PerpProductLpState


class MaxOrderSizeDirection(StrEnum):
    LONG = "long"
    SHORT = "short"


class ProductSymbol(VertexBaseModel):
    product_id: int
    symbol: str


class SymbolData(VertexBaseModel):
    type: str
    product_id: str
    symbol: str
    price_increment_x18: str
    size_increment: str
    min_size: str
    min_depth_x18: str
    max_spread_rate_x18: str
    maker_fee_rate_x18: str
    taker_fee_rate_x18: str
    long_weight_initial_x18: str
    long_weight_maintenance_x18: str


class SubaccountPosition(VertexBaseModel):
    balance: Union[PerpProductBalance, SpotProductBalance]
    product: Union[PerpProduct, SpotProduct]


# (price, amount)
MarketLiquidity = Annotated[list, conlist(str, min_items=2, max_items=2)]
