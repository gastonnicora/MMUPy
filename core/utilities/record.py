"""Registro histórico de la cola de páginas."""

from copy import copy, deepcopy

from ..memory.queue import Queue


class Record:
    """Conserva una copia de la cola después de cada paso de la simulación."""

    def __init__(self):
        """Inicializa el historial de colas."""
        self.queues = []
        self._snapshots = []

    def add_queue(self, queue: Queue):
        """Agrega al historial una copia del estado actual de la cola."""
        new_queue = copy(queue)
        self.queues.append(new_queue)
        self._snapshots.append(deepcopy(self.queues))

    def get_snapshot(self, index: int) -> list:
        """Devuelve el historial completo hasta el índice solicitado."""
        return self._snapshots[index]

    def get_record_pages(self, i: int = None):
        """Devuelve las páginas mostradas en la cola hasta el paso indicado."""
        pages = []
        index = {}

        queues = self._snapshots[i] if i is not None else self.queues

        for queue in queues:
            for frame in queue.frames:
                page = frame.page

                if page is None:
                    continue

                if page in index:
                    pages[index[page]] = None

                index[page] = len(pages)
                pages.append(page)

        return [page for page in pages if page is not None]

    def __repr__(self):
        """Devuelve una representación del historial de colas."""
        return "\n".join(str(queue) for queue in self.queues)
