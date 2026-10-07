from copy import  deepcopy   

from .page import Page


class Frame:
    def __init__(self, number: str, reserved: bool = False):
        self.number = number
        self.page: Page | None = None
        self.reserved = reserved

    @property
    def empty(self):
        return self.page is None and not self.reserved

    def load(self, page: Page):
        self.page = page

    def clear(self):
        self.page = None

    def __repr__(self):
        if self.page is None:
            return f"Frame({self.number}, empty, reserved={self.reserved})"

        return f"Frame({self.number}, page={self.page.number}, reserved={self.reserved})"


    def __copy__(self):
        new = Frame(self.number, self.reserved)
        new.page = self.page
        return new

    def __deepcopy__(self, memo):
        new = Frame(self.number, self.reserved)
        new.page = deepcopy(self.page, memo)
        return new
