from PySide6.QtWidgets import (
QGroupBox,
QVBoxLayout,
QTableWidget,
QTableWidgetItem,
QHeaderView,
QAbstractItemView,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor

class HistoryTable(QGroupBox):

    step_selected = Signal(int)

    def __init__(self):
        super().__init__("Historial")

        self._build_ui()
        self._connect_signals()

    # ─────────────────────────────────────────────────────────────
    # UI
    # ─────────────────────────────────────────────────────────────

    def _build_ui(self):
        layout = QVBoxLayout(self)

        self.table = QTableWidget()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels([
            "#",
            "Ref",
            "Pág",
            "PF",
            "Estado",
            "Marcos",
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.verticalHeader().setVisible(False)

        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.setSelectionMode(
            QAbstractItemView.SingleSelection
        )

        self.table.setMinimumHeight(50)

        layout.addWidget(self.table)

    # ─────────────────────────────────────────────────────────────
    # SIGNALS
    # ─────────────────────────────────────────────────────────────

    def _connect_signals(self):
        self.table.currentCellChanged.connect(
            self._on_row_changed
        )

    def _on_row_changed(self, row, *_):
        if row < 0:
            return

        self.step_selected.emit(row)

    # ─────────────────────────────────────────────────────────────
    # SIMULATOR
    # ─────────────────────────────────────────────────────────────

    def set_simulator(self, simulator):
        """
        Carga todos los pasos del simulador en el historial.
        """

        self.clear()

        if simulator is None:
            return

        self.table.setRowCount(
            simulator.total_steps
        )

        for row, step in enumerate(simulator.steps):

            frames = " | ".join(
                frame if frame is not None else "·"
                for frame, _, _, _, _ in step.frames
            )

            data = [
                str(row + 1),
                step.ref,
                step.page_number,
                str(step.page_faults_total),
                step.state_msg,
                frames,
            ]

            for column, text in enumerate(data):
                print(text)
                item = QTableWidgetItem(text)

                item.setTextAlignment(
                    Qt.AlignCenter
                )

                self.table.setItem(
                    row,
                    column,
                    item
                )

            if step.is_page_fault:
                self._mark_page_fault(row)

        self.table.resizeRowsToContents()

    # ─────────────────────────────────────────────────────────────
    # PAGE FAULT
    # ─────────────────────────────────────────────────────────────

    def _mark_page_fault(self, row):
        for column in range(
            self.table.columnCount()
        ):
            item = self.table.item(
                row,
                column
            )

            if item is not None:
                item.setForeground(
                    QColor("#d32f2f")
                )

    # ─────────────────────────────────────────────────────────────
    # SELECTION
    # ─────────────────────────────────────────────────────────────

    def select_step(self, step):
        """
        Selecciona visualmente un paso del historial.
        """

        if not (
            0 <= step < self.table.rowCount()
        ):
            self.table.clearSelection()
            return

        self.table.blockSignals(True)

        self.table.selectRow(step)

        self.table.scrollToItem(
            self.table.item(step, 0)
        )

        self.table.blockSignals(False)

    # ─────────────────────────────────────────────────────────────
    # CLEAR
    # ─────────────────────────────────────────────────────────────

    def clear(self):
        self.table.clearContents()
        self.table.setRowCount(0)

    # ─────────────────────────────────────────────────────────────
    # PROPERTIES
    # ─────────────────────────────────────────────────────────────

    @property
    def current_step(self):
        return self.table.currentRow()