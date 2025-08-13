from typing import Optional, Callable
from src.model.Card import Card


class Stat(Card):

    def __init__(
        self,
        name: str = "",
        initial_value: int = 0,
        max_value: Optional[int] = None,
    ):
        self.name: str = name
        self.value: int = initial_value
        self.max: Optional[int] = max_value
