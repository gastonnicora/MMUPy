"""Implementación del algoritmo FIFO de segunda oportunidad."""

from core.algorithm.algorithm import Algorithm
from core.memory.frame import Frame


class Fifo2(Algorithm):
    """Aplica FIFO utilizando el bit de referencia como segunda oportunidad."""

    def select_frame(self, index: int) -> Frame:
        """Busca el primer marco cuya página no esté referenciada."""
        while True:
            frame = self.queue.frames[0]

            if not frame.page.referenced:
                return frame

            frame.page.referenced = False
            self.queue.pop()
            self.queue.push(frame)

    def referenced(self, frame: Frame) -> None:
        """Marca como referenciada la página accedida."""
        frame.page.referenced = True
