from enum import Enum


class CardType(Enum):
    """Type of card. Either Stat card or Note card."""

    STAT = 0
    NOTE = 1


GRID_SIZE: int = 100
SHEET_CARD_WIDTH: int = 10
SHEET_CARD_HEIGHT: int = 20
