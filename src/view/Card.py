from typing import Optional
from dataclasses import dataclass
from PyQt6.QtWidgets import QScrollArea, QWidget, QGridLayout, QPushButton
from PyQt6.QtCore import QSize, QObject, Qt, QMimeData, QRect
from PyQt6.QtGui import (
    QDropEvent,
    QMouseEvent,
    QDrag,
    QPixmap,
    QDragEnterEvent,
    QDragMoveEvent,
)
from src import GRID_SIZE


class Card(QWidget):

    def __init__(
        self,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)

        self.loc: Optional[QRect] = None
        """Location of this card on a sheet."""

    def cells_width(self) -> int:
        """
        Gets the width of this card in grid cells.
        :returns: Width of this card in grid cells
        """
        hinted_size: QSize = super().sizeHint()

        if hinted_size.width() % GRID_SIZE == 0:
            return hinted_size // GRID_SIZE
        return hinted_size.width() // GRID_SIZE + 1

    def cells_height(self) -> int:
        """
        Gets the height of this card in grid cells.
        :returns: Height of this card in grid cells
        """
        hinted_size: QSize = super().sizeHint()

        if hinted_size.height() % GRID_SIZE == 0:
            return hinted_size // GRID_SIZE
        return hinted_size.height() // GRID_SIZE + 1

    def set_location(self, column: int, row: int) -> None:
        """
        Sets this cards rectangle in the grid layout. Uses indexes.
        :param column: Top left column index
        :param row: Top left row index
        """
        self.loc = QRect(column, row, self.cells_width(), self.cells_height())

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        """
        Called by Qt when a click and drag mouse event is thrown. Starts a drag.
        :param e: Event that contains mouse event info
        """
        if e.buttons() == Qt.MouseButton.LeftButton:
            drag: QDrag = QDrag(self)

            mime: QMimeData = QMimeData()
            drag.setMimeData(mime)

            pixmap: QPixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec(Qt.DropAction.MoveAction)

    def mouseDoubleClickEvent(self, e: QMouseEvent) -> None:
        return super().mouseDoubleClickEvent(e)
