from ..memory.frame import Frame
from copy import copy, deepcopy

class Queue:
    def __init__(self):
        self.frames = []

    def find_frame(self, frame_number: str):
        for frame in self.frames:
            if frame.number == frame_number:
                return frame

        return None
    
    def find_frame_index(self, frame: Frame):

        for index, current_frame in enumerate(self.frames):

            if current_frame == frame:
                return index

        return None
    
    def find_frame_by_page(self, page_number: str):
        for frame in self.frames:
            if frame.page is not None:
                if frame.page.number == page_number:
                    return frame

        return None

    
    def push(self, frame: Frame):
        self.frames.append(frame)
    
    def insert(self, frame: Frame):
        self.frames.insert(0,frame)
    
    def pop(self):
        return self.frames.pop(0)
    
    def remove(self, frame: Frame):
        self.frames.remove(frame)


    def __repr__(self):
        return "\n".join(
            str(frame)
            for frame in self.frames
        )

    def __copy__(self):          
        new = Queue()
        new.frames = [copy(frame) for frame in self.frames]
        return new

    def __deepcopy__(self, memo):      
        new = Queue()
        new.frames = [deepcopy(frame, memo) for frame in self.frames]
        return new