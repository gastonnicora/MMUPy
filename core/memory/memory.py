from .frame import Frame


class Memory:
    def __init__(self, frame_count: int, reserved: bool = False):
        count = frame_count
        if reserved:
            count -= 1
        self.frames = [
            Frame(i, reserved=False)
            for i in range(count)
        ]
        if reserved:
            self.frames.append(Frame(count, reserved=True))

    def find_page(self, page_number: str):
        for frame in self.frames:
            if frame.page is not None:
                if frame.page.number == page_number:
                    return frame

        return None

    def first_empty(self):
        for frame in self.frames:
            if frame.empty:
                return frame

        return None
    
    def get_reserved_frame(self):
        for frame in self.frames:
            if frame.reserved:
                return frame
        return None
    

    def __repr__(self):
        return "\n".join(
            str(frame)
            for frame in self.frames
        )
