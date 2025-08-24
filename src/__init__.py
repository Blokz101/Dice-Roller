from enum import Enum

class CardType(Enum):
    """Type of card. Either Stat card or Note card."""

    STAT = 0
    NOTE = 1

GRID_SIZE: int = 100
"""Size of each square on the sheet grid."""
SHEET_CARD_WIDTH: int = 10
"""Number of columns in each sheet."""
SHEET_CARD_HEIGHT: int = 20
"""Number of rows in each sheet."""