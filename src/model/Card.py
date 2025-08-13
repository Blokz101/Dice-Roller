from typing import Optional
from src import CardType


class Card:

    def __init__(
        self,
        name: str,
        card_type: CardType,
        column: Optional[int] = None,
        row: Optional[int] = None,
        column_span: Optional[int] = None,
        row_span: Optional[int] = None,
    ):
        self.name: int = name
        self.card_type: CardType = card_type
        self.column: Optional[int] = column
        self.row: Optional[int] = row
        self.column_span: Optional[int] = column_span
        self.row_span: Optional[int] = row_span
