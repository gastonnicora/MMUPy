"""Gestión de la memoria física de la simulación."""

from .frame import Frame


class Memory:
    """Contiene los marcos físicos disponibles para la simulación."""

    def __init__(self, frame_count: int, reserved: bool = False):
        """Crea los marcos y, si corresponde, un marco reservado."""
        count = frame_count - 1 if reserved else frame_count
        self.frames = [Frame(i, reserved=False) for i in range(count)]

        if reserved:
            self.frames.append(Frame(count, reserved=True))

    def find_page(self, page_number: str):
        """Busca el marco que contiene la página indicada."""
        return next(
            (
                frame
                for frame in self.frames
                if frame.page is not None and frame.page.number == page_number
            ),
            None,
        )

    def first_empty(self):
        """Devuelve el primer marco libre y no reservado."""
        return next((frame for frame in self.frames if frame.empty), None)

    def get_reserved_frame(self):
        """Devuelve el marco reservado, si existe."""
        return next((frame for frame in self.frames if frame.reserved), None)

    def __repr__(self):
        """Devuelve una representación de todos los marcos."""
        return "\n".join(str(frame) for frame in self.frames)
