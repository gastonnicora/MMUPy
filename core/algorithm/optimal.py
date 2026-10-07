"""Implementación del algoritmo óptimo de reemplazo."""

from core.algorithm.algorithm import Algorithm
from core.memory.frame import Frame


class Optimal(Algorithm):
    """Reemplaza la página cuyo próximo uso está más alejado en el futuro."""

    def select_frame(self, index: int) -> Frame:
        """Selecciona la página que tardará más en volver a utilizarse."""
        farthest = -1
        victim = None

        for frame in self.memory.frames:
            if frame.page is None:
                continue

            page_number = frame.page.number
            next_use = self._next_use(page_number, index)

            if next_use is None:
                return frame

            if next_use > farthest:
                farthest = next_use
                victim = frame

        if victim is not None:
            return victim

        return self.queue.frames[0]

    def _next_use(self, page_number: str, index: int) -> int | None:
        """Devuelve el siguiente índice de uso de una página."""
        for ref_index in range(index + 1, len(self.refs)):
            if self.refs[ref_index][0] == page_number:
                return ref_index
        return None

    def referenced(self, frame: Frame) -> None:
        """El algoritmo óptimo no necesita actualizar metadatos ante un acceso."""
        return None
