"""Registro de fallos de página."""


class PF:
    """Acumula los fallos de página producidos durante la simulación."""

    def __init__(self):
        """Inicializa los contadores de fallos."""
        self.page_faults_cant = 0
        self.page_faults = []

    def add_page_fault(self, page_fault: bool):
        """Registra si el acceso actual produjo un fallo de página."""
        if page_fault:
            self.page_faults_cant += 1
        self.page_faults.append(page_fault)
