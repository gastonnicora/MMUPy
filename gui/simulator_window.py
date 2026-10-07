from PySide6.QtWidgets import (
QMainWindow,
QWidget,
QVBoxLayout,
QSplitter,
)
from PySide6.QtCore import QTimer, Qt

from core.simulator import Simulator

from gui.widgets.controls import ControlsWidget
from gui.widgets.record_view import RecordView
from gui.widgets.simulation_table import SimulationTable
from gui.widgets.history_table import HistoryTable

class SimulatorWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simulador MMU")
        self.setMinimumSize(900, 750)

        self.simulator: Simulator | None = None
        self.current_step = -1

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._auto_advance)

        self._build_ui()
        self._connect_signals()
        self._update_display()

                                                                   
        
                                                                   

    def _build_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        self.controls = ControlsWidget()
        self.queue_view = RecordView()
        
        self.simulation_table = SimulationTable()
        self.history_table = HistoryTable()

        splitter = QSplitter(Qt.Vertical)

        splitter.addWidget(self.controls)
        splitter.addWidget(self.queue_view)
        splitter.addWidget(self.simulation_table)
        splitter.addWidget(self.history_table)

                            
         
                   
              
                    
                   
         
        splitter.setSizes([
            120,
            70,
            300,
            200,
        ])

        layout.addWidget(splitter)

        self.main_splitter = splitter

                                                                   
             
                                                                   

    def _connect_signals(self):

        self.controls.play_clicked.connect(
            self._on_play
        )

        self.controls.algorithm_changed.connect(
            self._on_algorithm_changed
        )

        self.controls.pause_clicked.connect(
            self._on_pause
        )

        self.controls.reset_clicked.connect(
            self._on_reset
        )

        self.controls.back_clicked.connect(
            self._step_back
        )

        self.controls.forward_clicked.connect(
            self._step_fwd
        )

        self.controls.frames_changed.connect(
            self._on_frames_changed
        )

        self.controls.references_changed.connect(
            self._on_references_changed
        )

        self.history_table.step_selected.connect(
            self._on_table_click
        )

                                                                   
               
                                                                   

    def _create_simulator(self):

        self.simulator = Simulator(
            self.controls.frame_count,
            self.controls.references,
            self.controls.algorithm
        )

        self.current_step = -1

        self.history_table.set_simulator(
            self.simulator
        )


    def _ensure_simulator(self):

        if self.simulator is None:
            self._create_simulator()
            return

        if (
            self.simulator.references_text
            != self.controls.references
        ):
            self._create_simulator()
            return

        if (
            self.simulator.memory_size
            != self.controls.frame_count
        ):
            self._create_simulator()
            return

        if (
            self.simulator.algorithm_name
            != self.controls.algorithm
        ):
            self._create_simulator()

                                                                   
               
                                                                   

    def _on_play(self):

        self._ensure_simulator()

        if (
            self.current_step
            >= self.simulator.total_steps - 1
        ):
            self.current_step = -1

        self.controls.set_playing(True)
        self.timer.start(self.controls.interval)

    def _on_pause(self):

        self.timer.stop()
        self.controls.set_playing(False)

    def _on_reset(self):

        self.timer.stop()

        self.simulator = None
        self.current_step = -1

        self.controls.set_playing(False)

        self.history_table.clear()
        self.simulation_table.clear()
        self.queue_view.clear()

        self._update_display()

    def _step_fwd(self):

        self._ensure_simulator()

        if (
            self.current_step
            < self.simulator.total_steps - 1
        ):
            self.current_step += 1
            self._update_display()

    def _step_back(self):

        if self.current_step > 0:

            self.current_step -= 1
            self._update_display()

        elif self.current_step == 0:

            self.current_step = -1
            self._update_display()

    def _auto_advance(self):

        if self.simulator is None:
            self._on_pause()
            return

        if (
            self.current_step
            < self.simulator.total_steps - 1
        ):
            self.current_step += 1
            self._update_display()

        else:
            self._on_pause()

                                                                   
             
                                                                   

    def _on_frames_changed(self, _):

        self._create_simulator()
        self._update_display()

    def _on_references_changed(self):

        self._create_simulator()
        self._update_display()

    def _on_table_click(self, row):

        if self.simulator is None:
            return

        if 0 <= row < self.simulator.total_steps:

            self.timer.stop()
            self.controls.set_playing(False)

            self.current_step = row
            self._update_display()

                                                                   
            
                                                                   

    def _update_display(self):

        if (
            self.simulator is None
            or self.current_step < 0
        ):
            self.queue_view.clear()
            self.simulation_table.clear()
            return

        self.queue_view.update(
            self.simulator,
            self.current_step
        )

        self.simulation_table.update(
            self.simulator,
            self.current_step
        )

        self.history_table.select_step(
            self.current_step
        )
        
    def _on_algorithm_changed(self, _):

        self._create_simulator()
        self._update_display()
