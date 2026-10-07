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

class SimulationTable(QGroupBox):

    MODIFIED_COLOR = QColor("#ef5350")
    FRAME_RESERVED_BACKGROUND = QColor("#f0f050")

    def __init__(self):
        super().__init__("Vista de simulación")

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

        # Ocultar números de fila de Qt.
        self.table.verticalHeader().setVisible(False)

        # Ocultar encabezados superiores de Qt.
        #
        # Esto es importante:
        # QTableWidget agrega sus propios encabezados de columnas
        # con números 1, 2, 3... si no usamos encabezados propios.
        self.table.horizontalHeader().setVisible(False)

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )

        layout.addWidget(self.table)

    # =============================================================
    # UPDATE
    # =============================================================

    def update(self, simulator, current_step):

        if simulator is None or current_step < 0:
            self.clear()
            return

        steps = simulator.steps[:current_step + 1]

        frame_count = simulator.memory_size

        # ---------------------------------------------------------
        # COLUMNAS
        #
        # Columna 0:
        #   nombres de filas
        #
        # Columnas 1..N:
        #   referencias
        #
        # Ejemplo:
        #
        #       | P1 | P2 | P3 | P4
        # Ref   | 1  | 2  | 3  | 4
        # Marco0|    |    |    |
        # Marco1|    |    |    |
        # PF    |    | X  |    |
        # ---------------------------------------------------------

        column_count = len(steps) + 1

        # ---------------------------------------------------------
        # FILAS
        #
        # 1 -> Referencia
        # N -> Marcos
        # 1 -> PF
        #
        # NO existe una fila para 1 2 3 4...
        # ---------------------------------------------------------

        row_count = frame_count + 2

        self.table.setRowCount(row_count)
        self.table.setColumnCount(column_count)

        self._clear_table()

        self._build_row_labels(frame_count)
        self._fill_references(steps)
        self._fill_frames(steps, frame_count)
        self._fill_page_faults(steps)

        self.table.resizeColumnsToContents()

    # =============================================================
    # ROW LABELS
    # =============================================================

    def _build_row_labels(self, frame_count):

        # ---------------------------------------------------------
        # Columna izquierda
        # ---------------------------------------------------------

        self._set_item(
            row=0,
            column=0,
            text="Ref",
            bold=True
        )

        for frame in range(frame_count):

            self._set_item(
                row=frame + 1,
                column=0,
                text=f"Marco {frame}",
                bold=True
            )

        self._set_item(
            row=frame_count + 1,
            column=0,
            text="PF",
            bold=True
        )

    # =============================================================
    # REFERENCES
    # =============================================================

    def _fill_references(self, steps):

        """
        Primera fila:

            Ref | 1 | 2 | 3M | 4 | 5
        """

        for column, step in enumerate(
            steps,
            start=1
        ):

            item = QTableWidgetItem(step.ref)

            self._center(item)

            if step.is_modified:

                item.setFont(
                    QFont(
                        "Consolas",
                        10
                    )
                )

            self.table.setItem(
                0,
                column,
                item
            )

    # =============================================================
    # FRAMES
    # =============================================================

    def _fill_frames(
        self,
        steps,
        frame_count
    ):

        for column, step in enumerate(
            steps,
            start=1
        ):

            for frame_index in range(frame_count):

                (
                    page_number,
                    valid,
                    referenced,
                    modified,
                    reserved
                ) = step.frames[frame_index]

                text = (
                    str(page_number)
                    if page_number is not None
                    else ""
                )

                if referenced:
                    text +="*"
                    
                if modified:
                    text += "M"
                    
                
                item = QTableWidgetItem(text)

                self._center(item)

                # -------------------------------------------------
                # Marco reservado
                # -------------------------------------------------

                if reserved:

                    item.setBackground(
                        self.FRAME_RESERVED_BACKGROUND
                    )

                    # Negro para que se vea sobre amarillo.
                    item.setForeground(
                        QColor("#000000")
                    )

                    item.setFont(
                        QFont(
                            "Consolas",
                            10
                        )
                    )


                if modified:


                    item.setFont(
                        QFont(
                            "Consolas",
                            10,
                        )
                    )
                    
                self.table.setItem(
                    frame_index + 1,
                    column,
                    item
                )

    # =============================================================
    # PAGE FAULTS
    # =============================================================

    def _fill_page_faults(self, steps):

        row = self.table.rowCount() - 1

        page_fault_number = 0

        for column, step in enumerate(
            steps,
            start=1
        ):

            if step.is_page_fault:

                page_fault_number += 1

                text = str(page_fault_number)

            else:

                text = ""

            item = QTableWidgetItem(text)

            self._center(item)

            if step.is_page_fault:

                item.setForeground(
                    self.MODIFIED_COLOR
                )

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