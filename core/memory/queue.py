"""Cola utilizada para administrar el orden de reemplazo."""

from copy import copy, deepcopy

from ..memory.frame import Frame


class Queue:
    """Mantiene los marcos en el orden utilizado por los algoritmos."""

    def __init__(self):
        """Inicializa una cola vacía."""
        self.frames = []

    def find_frame(self, frame_number: str):
        """Busca un marco por su número."""
        return next((frame for frame in self.frames if frame.number == frame_number), None)

    def find_frame_index(self, frame: Frame):
        """Devuelve la posición de un marco o ``None`` si no está presente."""
        try:
            return self.frames.index(frame)
        except ValueError:
            return None

    def find_frame_by_page(self, page_number: str):
        """Busca el marco que contiene una página."""
        return next(
            (
                frame
                for frame in self.frames
                if frame.page is not None and frame.page.number == page_number
            ),
            None,
        )

    def push(self, frame: Frame):
        """Agrega un marco al final de la cola."""
        self.frames.append(frame)

    def insert(self, frame: Frame):
        """Agrega un marco al comienzo de la cola."""
        self.frames.insert(0, frame)

    def pop(self):
        """Extrae y devuelve el primer marco de la cola."""
        return self.frames.pop(0)

    def remove(self, frame: Frame):
        """Elimina de la cola el marco indicado."""
        self.frames.remove(frame)

    def __repr__(self):
        """Devuelve la cola como una línea por marco."""
        return "\n".join(str(frame) for frame in self.frames)

    def __copy__(self):
        """Crea una copia superficial de la cola."""
        new = Queue()
        new.frames = [copy(frame) for frame in self.frames]
        return new

    def __deepcopy__(self, memo):
        """Crea una copia profunda de la cola."""
        new = Queue()
        new.frames = [deepcopy(frame, memo) for frame in self.frames]
        return new
