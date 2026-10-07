from abc import ABC, abstractmethod

from core.memory.memory import Memory
from core.memory.queue import Queue
from core.memory.frame import Frame


class Algorithm(ABC):

    def __init__(
        self,
        queue: Queue = None,
        memory: Memory = None,
        refs: list =[]
    ):
        self.queue = queue
        self.memory = memory
        self.refs = refs

    @abstractmethod
    def select_frame(self,index: int) -> Frame:
        pass

    @abstractmethod
    def referenced(self, frame: Frame):
        pass
