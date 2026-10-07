"""Representación de una página virtual."""


class Page:
    """Contiene el estado de una página durante la simulación."""

    def __init__(self, number: str):
        """Inicializa una página con todos sus indicadores desactivados."""
        self.number = number
        self.valid = False
        self.modified = False
        self.referenced = False

    def __repr__(self):
        """Devuelve una representación del estado de la página."""
        return (
            f"Page("
            f"number={self.number}, "
            f"valid={self.valid}, "
            f"modified={self.modified}, "
            f"referenced={self.referenced}, "
            f")"
        )

    def __copy__(self):
        """Crea una copia superficial de la página."""
        new = Page(self.number)
        new.valid = self.valid
        new.modified = self.modified
        new.referenced = self.referenced
        return new

    def __deepcopy__(self, memo):
        """Crea una copia independiente de la página."""
        new = Page(self.number)
        new.valid = self.valid
        new.modified = self.modified
        new.referenced = self.referenced
        return new
