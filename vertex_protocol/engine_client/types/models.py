from pydantic import BaseModel


class MintLp(BaseModel):
    product_id: int
    subaccount: str
    amount_base: str
    quote_amount_low: str
    quote_amount_high: str


class BurnLp(BaseModel):
    product_id: int
    subaccount: str
    amount_lp: str


class ApplyDelta(BaseModel):
    product_id: int
    subaccount: str
    amount_delta: str
    v_quote_delta: str


class MintLpTx(BaseModel):
    mint_lp: MintLp


class BurnLpTx(BaseModel):
    burn_lp: BurnLp


class ApplyDeltaTx(BaseModel):
    apply_delta: ApplyDelta


class SubaccountHealth(BaseModel):
    assets: str
    liabilities: str
    health: str


class SpotLpBalance(BaseModel):
    amount: str


class SpotBalance(BaseModel):
    amount: str
    last_cumulative_multiplier_x18: str


class SpotProductBalance(BaseModel):
    product_id: int
    lp_balance: SpotLpBalance
    balance: SpotBalance


class PerpLpBalance(BaseModel):
    amount: str
    last_cumulative_funding_x18: str


class PerpBalance(BaseModel):
    amount: str
    v_quote_balance: str
    last_cumulative_funding_x18: str


class PerpProductBalance(BaseModel):
    product_id: int
    lp_balance: PerpLpBalance
    balance: PerpBalance


class ProductRisk(BaseModel):
    long_weight_initial_x18: str
    short_weight_initial_x18: str
    long_weight_maintenance_x18: str
    short_weight_maintenance_x18: str
    large_position_penalty_x18: str


class ProductBookInfo(BaseModel):
    size_increment: str
    price_increment_x18: str
    min_size: str
    collected_fees: str
    lp_spread_x18: str


class BaseProduct(BaseModel):
    product_id: int
    oracle_price_x18: str
    risk: ProductRisk
    book_info: ProductBookInfo


class BaseProductLpState(BaseModel):
    supply: str


class SpotProductConfig(BaseModel):
    token: str
    interest_inflection_util_x18: str
    interest_floor_x18: str
    interest_small_cap_x18: str
    interest_large_cap_x18: str


class SpotProductState(BaseModel):
    cumulative_deposits_multiplier_x18: str
    cumulative_borrows_multiplier_x18: str
    total_deposits_normalized: str
    total_borrows_normalized: str


class SpotProductLpAmount(BaseModel):
    amount: str
    last_cumulative_multiplier_x18: str


class SpotProductLpState(BaseProductLpState):
    quote: SpotProductLpAmount
    base: SpotProductLpAmount


class SpotProduct(BaseProduct):
    config: SpotProductConfig
    state: SpotProductState
    lp_state: SpotProductLpState


class PerpProductState(BaseModel):
    cumulative_funding_long_x18: str
    cumulative_funding_short_x18: str
    available_settle: str
    open_interest: str


class PerpProductLpState(BaseModel):
    last_cumulative_funding_x18: str
    cumulative_funding_per_lp_x18: str
    base: str
    quote: str


class PerpProduct(BaseProduct):
    state: PerpProductState
    lp_state: PerpProductLpState
