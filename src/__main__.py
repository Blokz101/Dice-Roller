from typing import Optional, Any
from PyQt6.QtCore import QMimeData, Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QWidget,
    QApplication,
    QPushButton,
    QGridLayout,
    QSizePolicy,
)
from PyQt6.QtGui import (
    QDropEvent,
    QMouseEvent,
    QDrag,
    QPixmap,
    QDragEnterEvent,
    QDragMoveEvent,
)
from src.view.DiceRollerWindow import DiceRollerWindow
from src.view.StatWidget import StatWidget
from src.view.SheetWidget import SheetWidget

if __name__ == "__main__":
    app: QApplication = QApplication([])
    app.setStyle("Fusion")
    window: DiceRollerWindow = DiceRollerWindow()
    window.show()
    sheet: SheetWidget = SheetWidget()
    window.add_sheet(sheet, "Testing")

    sheet.add_card(StatWidget(), 1, 1)
    sheet.add_card(StatWidget(), 1, 3)

    app.exec()
