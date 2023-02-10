
class Varchar:
    def __init__(self) -> None:
        self.name = None
        self.default = None
        self.length = None
        self.is_nullable = True

    def sql(self):
        if self.default:
            return f"{self.name} ({self.length}) DEFAULT '{self.default}'"
        else:
            return f"{self.name} ({self.length})"