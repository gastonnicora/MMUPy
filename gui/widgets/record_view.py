from PySide6.QtWidgets import (
QGroupBox,
QVBoxLayout,
QTableWidget,
QTableWidgetItem,
QHeaderView,
QAbstractItemView,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

from core.memory.page import Page
from core.simulator import Simulator
from core.utilities.record import Record

class RecordView(QGroupBox):

    INVALID_COLOR = QColor("#9e9e9e")
    FRAME_RESERVED_BACKGROUND = QColor("#f0f000")
    TEXT_COLOR = QColor("#000000")

    def __init__(self):
        super().__init__("Cola de páginas")

        self._build_ui()

    # =============================================================
    # UI
    # =============================================================

    def _build_ui(self):

        layout = QVBoxLayout(self)

        self.table = QTableWidget()

        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.table.setSelectionMode(
            QAbstractItemView.NoSelection
        )

        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self.setMaximumHeight(75)

        layout.addWidget(self.table)

    # =============================================================
    # UPDATE
    # =============================================================

    def update(
        self,
        simulator: Simulator,
        current_step: int
    ):

        if simulator is None or current_step < 0:
            self.clear()
            return

        pages = simulator.record.get_record_pages(current_step)

        row_count = 1
        column_count = len(pages) + 1

        self.table.setRowCount(row_count)
        self.table.setColumnCount(column_count)

        self._clear_table()

        self._build_row_label()
        self._fill_pages(pages)

        self.table.resizeColumnsToContents()

    # =============================================================
    # ROW LABEL
    # =============================================================

    def _build_row_label(self):

        self._set_item(
            row=0,
            column=0,
            text="Cola:",
            bold=True
        )

    # =============================================================
    # PAGES
    # =============================================================

    def _fill_pages(self, pages):

        for column, page in enumerate(
            pages,
            start=1
        ):

            text = self._page_text(page)

            item = QTableWidgetItem(text)

            self._center(item)


            if not page.valid:
                self._mark_invalid(item)

            self.table.setItem(
                0,
                column,
                item
            )


    # =============================================================
    # PAGE TEXT
    # =============================================================

    def _page_text(self, page:Page):

        if page.number is None:
            return ""

        text = str(page.number)

        if page.referenced:
            text += "*"
        
        if page.modified:
            text += "M"

        return text

    
    # =============================================================
    # HELPERS
    # =============================================================

    def _set_item(
        self,
        row,
        column,
        text,
        bold=False
    ):

        item = QTableWidgetItem(text)

        self._center(item)

        if bold:

            item.setFont(
                QFont(
                    "Consolas",
                    10,
                    QFont.Bold
                )
            )

        self.table.setItem(
            row,
            column,
            item
        )

    def _center(self, item):

        item.setTextAlignment(
            Qt.AlignCenter
        )

    def _clear_table(self):

        self.table.clearContents()

    # =============================================================
    # CLEAR
    # =============================================================

    def clear(self):

        self.table.clear()

        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        
    def _mark_invalid(self, item):

        item.setForeground(
            self.INVALID_COLOR
        )

        font = item.font()
        font.setStrikeOut(True)

        item.setFont(font)

