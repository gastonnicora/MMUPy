from core.algorithm.algorithm import Algorithm
from core.memory.frame import Frame


class Fifo2(Algorithm):

    def select_frame(self,index: int) -> Frame:

        while True:

            frame = self.queue.frames[0]

            if not frame.page.referenced:
                return frame

            frame.page.referenced = False

            self.queue.pop()
            self.queue.push(frame)

    def referenced(self, frame: Frame):

        frame.page.referenced = True
