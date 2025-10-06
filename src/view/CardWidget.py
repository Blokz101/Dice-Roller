from typing import Optional, Self
from PyQt6.QtWidgets import QWidget, QMenu
from PyQt6.QtCore import Qt, QMimeData, QRect, QPoint
from PyQt6.QtGui import (
    QMouseEvent,
    QAction,
    QDrag,
    QPixmap,
)
from src.model.Sheet import Sheet
from src.model.Card import Card
from src.model.Stat import Stat
from src.model.Note import Note


class CardWidget(QWidget):

    def __init__(
        self,
        sheet: Sheet,
        card: Card,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)

        # Model related instance vars
        self.sheet: Sheet = sheet
        """Sheet model instance."""
        self.card: Card = card
        """Card model instance."""

        # GUI related instance vars
        self.loc: QRect = QRect(
            self.card.column, self.card.row, self.cells_width(), self.cells_height()
        )
        """Location of this card on a sheet."""

        # Widget config
        self.setStyleSheet(
            "CardWidget {background-color: palette(Midlight); border-radius: 4px}"
        )
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)  # type: ignore

    def show_context_menu(self, pos: QPoint) -> None:
        """
        Shows the context menu for this card.
        :param pos: The position of the mouse event
        """
        menu: QMenu = QMenu(self)
        menu.addAction("Edit", self.edit_card)  # type: ignore
        menu.addAction("Delete", self.delete_card)  # type: ignore
        menu.exec(self.mapToGlobal(pos))  # type: ignore

    def edit_card(self) -> None:
        """
        Opens a dialog to edit the card.
        """
        raise NotImplementedError

    def delete_card(self) -> None:
        """
        Deletes the card.
        """
        raise NotImplementedError

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
