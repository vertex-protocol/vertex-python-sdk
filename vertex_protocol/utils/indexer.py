from enum import Enum


class VertexIndexer(str, Enum):
    ORDERS = "orders"
    MATCHES = "matches"
    EVENTS = "events"
    SUMMARY = "summary"
    PRODUCTS = "products"
    CANDLESTICKS = "candlesticks"
    FUNDING_RATE = "funding_rate"
    PERP_PRICES = "price"
    ORACLE_PRICES = "oracle_price"
    REWARDS = "rewards"
    MAKER_STATISTICS = "maker_statistics"
    LIQUIDATION_FEED = "liquidation_feed"
    LINKED_SIGNER_RATE_LIMIT = "linked_signer_rate_limit"
