from PyQt6.QtCore import QEvent

# Stats editor window
STAT_EDITOR_TABLE_HEADERS: list[str] = ["Name", "Value", "Max", "Min"]
"""Headers for the stat editor table."""
STAT_EDITOR_HISTORY_TABLE_HEADERS: list[str] = ["Description", "Edit", "Total"]
"""Headers for the stat editor history table."""
CARD_CONFIG_STAT_TABLE_HEADERS: list[str] = ["Stat Name", "Display Name", "Subtext", "Show Max", "Show Min"]
"""Headers for the card config stat table."""

STAT_NAME_CHANGED: int = QEvent.registerEventType()
"""Stat name changed event type"""
