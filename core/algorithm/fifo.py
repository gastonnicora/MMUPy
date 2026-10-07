from core.algorithm.algorithm import Algorithm
from core.memory.frame import Frame


class FIFO(Algorithm):

    def select_frame(self,index: int) -> Frame:
        return self.queue.frames[0]

    def referenced(self, frame: Frame):
        pass
