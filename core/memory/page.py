

class Page:
    def __init__(self, number: str):
        self.number = number
        self.valid = False
        self.modified = False
        self.referenced = False

    def __repr__(self):
        return (
            f"Page("
            f"number={self.number}, "
            f"valid={self.valid}, "
            f"modified={self.modified}, "
            f"referenced={self.referenced}, "
            f")"
        )

    def __copy__(self):
        new = Page(self.number)
        new.valid = self.valid
        new.modified = self.modified
        new.referenced = self.referenced
        return new

    def __deepcopy__(self, memo):
        new = Page(self.number)
        new.valid = self.valid
        new.modified = self.modified
        new.referenced = self.referenced
        return new