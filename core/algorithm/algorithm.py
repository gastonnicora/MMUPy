"""Clases base para los algoritmos de reemplazo de páginas."""

from abc import ABC, abstractmethod

from core.memory.frame import Frame
from core.memory.memory import Memory
from core.memory.queue import Queue


class Algorithm(ABC):
    """Define la interfaz común de los algoritmos de reemplazo."""

    def __init__(
        self,
        queue: Queue | None = None,
        memory: Memory | None = None,
        refs: list | None = None,
    ) -> None:
        """Inicializa el algoritmo con el estado de la simulación."""
        self.queue = queue
        self.memory = memory
        self.refs = refs or []

    @abstractmethod
    def select_frame(self, index: int) -> Frame:
        """Selecciona el marco que será reemplazado."""
        raise NotImplementedError

    @abstractmethod
    def referenced(self, frame: Frame) -> None:
        """Actualiza el estado del algoritmo ante un acceso exitoso."""
        raise NotImplementedError
