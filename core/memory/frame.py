"""Representación de un marco de memoria física."""

from copy import deepcopy

from .page import Page


class Frame:
    """Representa un marco físico que puede contener una página."""

    def __init__(self, number: str, reserved: bool = False):
        """Inicializa un marco con su número y estado de reserva."""
        self.number = number
        self.page: Page | None = None
        self.reserved = reserved

    @property
    def empty(self):
        """Indica si el marco está disponible para cargar una página."""
        return self.page is None and not self.reserved

    def load(self, page: Page):
        """Carga una página en el marco."""
        self.page = page

    def clear(self):
        """Vacía el marco."""
        self.page = None

    def __repr__(self):
        """Devuelve una representación legible del marco."""
        if self.page is None:
            return f"Frame({self.number}, empty, reserved={self.reserved})"
        return f"Frame({self.number}, page={self.page.number}, reserved={self.reserved})"

    def __copy__(self):
        """Crea una copia superficial del marco."""
        new = Frame(self.number, self.reserved)
        new.page = self.page
        return new

    def __deepcopy__(self, memo):
        """Crea una copia profunda del marco y de su página."""
        new = Frame(self.number, self.reserved)
        new.page = deepcopy(self.page, memo)
        return new
