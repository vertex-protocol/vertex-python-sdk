from typing import Annotated

from pydantic import conlist

# (price, amount)
Liquidity = Annotated[list, conlist(str, min_items=2, max_items=2)]
