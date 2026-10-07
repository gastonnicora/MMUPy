import sys

from PySide6.QtWidgets import QApplication

from gui.simulator_window import SimulatorWindow


                                                                        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimulatorWindow()
    window.show()
    sys.exit(app.exec())   