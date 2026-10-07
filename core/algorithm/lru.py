"""Implementación del algoritmo LRU."""

from core.algorithm.algorithm import Algorithm
from core.memory.frame import Frame


class Lru(Algorithm):
    """Mantiene al frente la página utilizada menos recientemente."""

    def select_frame(self, index: int) -> Frame:
        """Devuelve el primer marco de la cola."""
        return self.queue.frames[0]

    def referenced(self, frame: Frame) -> None:
        """Mueve al final de la cola el marco que acaba de ser utilizado."""
        self.queue.remove(frame)
        self.queue.push(frame)
