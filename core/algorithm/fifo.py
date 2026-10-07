"""Implementación del algoritmo FIFO."""

from core.algorithm.algorithm import Algorithm
from core.memory.frame import Frame


class FIFO(Algorithm):
    """Reemplaza primero la página que lleva más tiempo en la cola."""

    def select_frame(self, index: int) -> Frame:
        """Devuelve el primer marco de la cola."""
        return self.queue.frames[0]

    def referenced(self, frame: Frame) -> None:
        """FIFO no necesita modificar información ante un acceso."""
        return None
