from PySide6.QtWidgets import (
    QGroupBox,
    QGridLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QSpinBox,
    QSlider,
    QLineEdit,
    QHBoxLayout,
)

from PySide6.QtCore import Qt, Signal


class ControlsWidget(QGroupBox):

    play_clicked = Signal()
    pause_clicked = Signal()
    reset_clicked = Signal()
    back_clicked = Signal()
    forward_clicked = Signal()

    frames_changed = Signal(int)
    references_changed = Signal()
    algorithm_changed = Signal(str)


    def __init__(self):
        super().__init__("Controles")

        self._build_ui()
        self._connect_signals()

    def _build_ui(self):
        grid = QGridLayout(self)

        # Algoritmo
        grid.addWidget(QLabel("Algoritmo:"), 0, 0)

        self.combo_algo = QComboBox()
        self.combo_algo.addItems([
            "FIFO",
            "FIFO2",
            "LRU",
            "OPTIMO"
        ])


        grid.addWidget(self.combo_algo, 0, 1)

        # Marcos
        grid.addWidget(QLabel("Marcos físicos:"), 0, 2)

        self.spin_frames = QSpinBox()
        self.spin_frames.setRange(1, 100)
        self.spin_frames.setValue(3)

        grid.addWidget(self.spin_frames, 0, 3)

        # Referencias
        grid.addWidget(QLabel("Referencias:"), 1, 0)

        self.input_refs = QLineEdit()
        self.input_refs.setPlaceholderText(
            "1 2 3 3M 4 1 2M 5 1M 6 7"
        )

        self.input_refs.setText(
            "1 2 3 3M 4 1 2M 5 1M 6 7"
        )

        grid.addWidget(
            self.input_refs,
            1, 1, 1, 3
        )

        # Velocidad
        grid.addWidget(QLabel("Velocidad:"), 2, 0)

        self.slider_speed = QSlider(Qt.Horizontal)
        self.slider_speed.setRange(100, 3000)
        self.slider_speed.setValue(10000)
        self.slider_speed.setInvertedAppearance(True)

        grid.addWidget(
            self.slider_speed,
            2, 1, 1, 2
        )

        self.label_speed = QLabel("0.1 s")
        grid.addWidget(self.label_speed, 2, 3)

        # Botones
        buttons = QHBoxLayout()

        self.btn_play = QPushButton("▶ Iniciar")
        self.btn_pause = QPushButton("⏸ Pausar")
        self.btn_reset = QPushButton("↻ Reiniciar")
        self.btn_back = QPushButton("◀")
        self.btn_fwd = QPushButton("▶")

        self.btn_pause.setEnabled(False)

        self.btn_back.setFixedWidth(40)
        self.btn_fwd.setFixedWidth(40)

        buttons.addWidget(self.btn_play)
        buttons.addWidget(self.btn_pause)
        buttons.addWidget(self.btn_reset)

        buttons.addStretch()

        buttons.addWidget(self.btn_back)
        buttons.addWidget(self.btn_fwd)

        grid.addLayout(buttons, 3, 0, 1, 4)

    def _connect_signals(self):
        self.btn_play.clicked.connect(
            self.play_clicked.emit
        )

        self.btn_pause.clicked.connect(
            self.pause_clicked.emit
        )

        self.btn_reset.clicked.connect(
            self.reset_clicked.emit
        )

        self.btn_back.clicked.connect(
            self.back_clicked.emit
        )

        self.btn_fwd.clicked.connect(
            self.forward_clicked.emit
        )

        self.spin_frames.valueChanged.connect(
            self.frames_changed.emit
        )
        
        self.combo_algo.currentTextChanged.connect(
            self.algorithm_changed.emit
        )


        self.input_refs.editingFinished.connect(
            self.references_changed.emit
        )

        self.slider_speed.valueChanged.connect(
            self._update_speed_label
        )

    # ─────────────────────────────────────────────────────────────

    @property
    def frame_count(self):
        return self.spin_frames.value()

    @property
    def references(self):
        return self.input_refs.text().strip()

    @property
    def interval(self):
        return 3100 - self.slider_speed.value()

    def _update_speed_label(self, value):
        seconds = (3100 - value) / 1000
        self.label_speed.setText(
            f"{seconds:.1f} s"
        )

    def set_playing(self, playing):
        self.btn_play.setEnabled(not playing)
        self.btn_pause.setEnabled(playing)


    @property
    def algorithm(self):
        return self.combo_algo.currentText()
