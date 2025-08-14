from typing import Optional, Self
from abc import ABC, abstractmethod
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QMimeData, QRect
from PyQt6.QtGui import (
    QMouseEvent,
    QDrag,
    QPixmap,
)
from src.model.Card import Card
from src.model.Stat import Stat
from src.model.Note import Note


class CardWidget(QWidget):

    def __init__(
        self,
        card: Card,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)

        # Model related instance vars
        self.card: Card = card
        """Card model instance."""

        # GUI related instance vars
        self.loc: QRect = QRect(
            self.card.column, self.card.row, self.cells_width(), self.cells_height()
        )
        """Location of this card on a sheet."""

    @classmethod
    def from_card(cls, card: Card, data_list: list[Stat | Note]) -> Self:
        """
        Creates a CardWidget from a Card model instance.
        :param card: Card model instance
        :returns: CardWidget instance
        """
        raise NotImplementedError

    def cells_width(self) -> int:
        """
        Gets the width of this card in grid cells.
        :returns: Width of this card in grid cells
        """
        raise NotImplementedError()

    def cells_height(self) -> int:
        """
        Gets the height of this card in grid cells.
        :returns: Height of this card in grid cells
        """
        raise NotImplementedError()

    def set_loc(self, column: int, row: int) -> None:
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
