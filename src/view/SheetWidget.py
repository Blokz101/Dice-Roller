from typing import Optional, cast
from PyQt6.QtWidgets import QScrollArea, QWidget, QGridLayout, QSizePolicy
from PyQt6.QtCore import QSize, QObject, QRect, QPoint, Qt
from PyQt6.QtGui import (
    QDropEvent,
    QDragEnterEvent,
    QDragLeaveEvent,
    QDragMoveEvent,
)
from src import GRID_SIZE, SHEET_CARD_WIDTH, SHEET_CARD_HEIGHT, CardType
from src.view.CardWidget import CardWidget
from src.view.StatWidget import StatWidget
from src.view.NoteWidget import NoteWidget
from src.model.Sheet import Sheet


class SheetWidget(QScrollArea):

    def __init__(self, sheet: Sheet, parent: Optional[QWidget] = None):
        super().__init__(parent)

        # Model related instance vars
        self.sheet: Sheet = sheet
        """Sheet model instance."""

        # GUI related instance vars
        self.card_widget_list: list[CardWidget] = []
        """List of card widgets in the sheet."""
        self.container_widget: QWidget
        """Container widget that holds the grid layout."""
        self.grid_layout: QGridLayout
        """Grid layout that cards will be placed on."""
        self.preview_widget: QWidget = QWidget()
        """Widget that is shown as a preview of drop during drag-and-drop operations."""

        self._setup_grid()
        self.populate_from_sheet()

    def _setup_grid(self) -> None:
        """Creates the grid and configures the layout."""
        self.container_widget = QWidget()
        self.grid_layout = QGridLayout()

        placeholder: QWidget
        for column in range(SHEET_CARD_WIDTH):
            for row in range(SHEET_CARD_HEIGHT):
                placeholder: QWidget = QWidget()
                placeholder.setStyleSheet(
                    "border: 1px solid palette(Midlight); border-radius: 3px"
                )
                placeholder.setFixedSize(QSize(GRID_SIZE, GRID_SIZE))
                self.grid_layout.addWidget(placeholder, row, column)

        self.container_widget.setLayout(self.grid_layout)
        self.setWidget(self.container_widget)

        # Widget config
        self.preview_widget.setStyleSheet(
            "background-color: palette(Midlight); border-radius: 3px"
        )
        self.setAcceptDrops(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

    def populate_from_sheet(self) -> None:
        """Adds all card widgets in the sheet to the grid layout."""
        for card in self.sheet.card_list:
            if card.card_type == CardType.STAT:
                self.add_card(StatWidget.from_card(card, self.sheet.stat_list))
            else:
                self.add_card(NoteWidget.from_card(card, self.sheet.note_list))

    def sizeHint(self) -> QSize:
        """
        Returns the size of the container widget and grid layout.
        :returns: Size the sheet should be
        """
        if self.container_widget:
            contents_size: QSize = self.container_widget.sizeHint()
            content_margins: tuple[
                Optional[int], Optional[int], Optional[int], Optional[int]
            ] = self.grid_layout.getContentsMargins()
            contents_size.setWidth(
                contents_size.width()
                + (0 if content_margins[0] is None else content_margins[0])  # Left
                + (0 if content_margins[2] is None else content_margins[2])  # Right
            )
            contents_size.setHeight(
                contents_size.height()
                + (0 if content_margins[1] is None else content_margins[1])  # Top
                + (0 if content_margins[3] is None else content_margins[3])  # Bottom
            )
            return contents_size

        return super().sizeHint()

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        """
        Called by Qt when a drag operation enters the sheet widget.
        :param e: Event that contains drag info
        """
        card: Optional[QObject] = e.source()
        if card is None or not isinstance(card, CardWidget):
            return

        size: QSize = QSize()
        size.setHeight(
            card.cells_height() * GRID_SIZE
            + (card.cells_height() - 1) * self.grid_layout.verticalSpacing()
        )
        size.setWidth(
            card.cells_width() * GRID_SIZE
            + (card.cells_width() - 1) * self.grid_layout.horizontalSpacing()
        )
        self.preview_widget.setFixedSize(size)
        e.accept()

    def dragLeaveEvent(self, _: QDragLeaveEvent):
        """Called by Qt when the drag operation leaves this widget. Hide the preview widget."""
        self.preview_widget.hide()

    def dragMoveEvent(self, e: QDragMoveEvent) -> None:
        """
        Called by Qt when a the mouse is moved while performing a drag operation.
        :param e: Event that contains drag info
        """
        card: Optional[QObject] = e.source()
        if card is None or not isinstance(card, CardWidget):
            return

        grid_idx: Optional[tuple[int, int]]
        grid_idx = self.pos_to_grid_idx(e.position().toPoint())
        if grid_idx is None:
            e.ignore()
            return
        if self.cells_free(card, *grid_idx):
            self.grid_layout.addWidget(self.preview_widget, grid_idx[1], grid_idx[0])
            self.preview_widget.show()
            e.accept()
        else:
            self.preview_widget.hide()
            e.ignore()

    def dropEvent(self, e: QDropEvent) -> None:
        """
        Called by Qt when the drag operation is completed with a drop.
        :param e: Event that contains drag info
        """

        # Type check the card and get the grid index
        card: Optional[QObject] = e.source()
        if card is None or not isinstance(card, CardWidget):
            return
        grid_idx: Optional[tuple[int, int]]
        grid_idx = self.pos_to_grid_idx(e.position().toPoint())
        if not grid_idx:
            return
        column: int
        row: int
        column, row = grid_idx

        if self.cells_free(card, column, row):
            self.preview_widget.hide()
            self.sheet.saved_to_file = False
            card.card.column = column
            card.card.row = row
            self.add_card(card)
            e.accept()
            return

    def pos_to_grid_idx(self, pos: QPoint) -> Optional[tuple[int, int]]:
        """
        Gets the grid row and column index from a mouse event point.
        :parm pos: Mouse event point in coordinates relative to the Sheet
        :returns: Row and column indexes respectively or none if the row and column cannot be found
        """
        rect: QRect
        for r in range(self.grid_layout.rowCount()):
            for c in range(self.grid_layout.columnCount()):
                rect = self.grid_layout.cellRect(r, c)
                if rect.contains(self.container_widget.mapFromParent(pos)):
                    return (c, r)

        return None

    def cells_free(self, new_card: CardWidget, column: int, row: int) -> bool:
        """
        Check if there is space for a card at a specific row and column location.
        :param new_card: Incoming card
        :param column: Column index the card is being checked against
        :param row: Row index the card is being checked against
        :returns: True if there is space, false otherwise
        """
        new_space: QRect = QRect(
            column, row, new_card.cells_width(), new_card.cells_height()
        )

        for card in self.card_widget_list:
            if card is new_card:
                continue
            if card.loc.intersects(new_space):
                return False

        return True

    def add_card(self, card: CardWidget) -> bool:
        """
        Adds a card to the sheet.
        :returns: Returns true if the card was placed successfully, false otherwise
        """

        # Requested location is not free
        if not self.cells_free(card, card.card.column, card.card.row):
            return False

        # Add card
        self.grid_layout.addWidget(
            card,
            card.card.row,
            card.card.column,
            card.cells_height(),
            card.cells_width(),
        )
        card.set_loc(card.card.column, card.card.row)
        if card not in self.card_widget_list:
            self.card_widget_list.append(card)
        return True
