from PyQt6.QtCore import QEvent

# Stats editor window
STAT_EDITOR_TABLE_HEADERS: list[str] = ["Name", "Value", "Max", "Min"]
"""Headers for the stat editor table."""
STAT_EDITOR_HISTORY_TABLE_HEADERS: list[str] = ["Description", "Edit", "Total"]
"""Headers for the stat editor history table."""

STAT_CHANGED_EVENT_TYPE: int = QEvent.registerEventType()
"""Stat changed event type id."""
NOTE_CHANGED_EVENT_TYPE: int = QEvent.registerEventType()
"""Note changed event type id."""
