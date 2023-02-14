
class Varchar:
    def __init__(self) -> None:
        self.name = None
        self.default = None
        self.length = None
        self.is_nullable = True

    def sql(self):
        base_name = f"{self.name}"

        length = self.length
        if length is None:
            length = 30

        if self.default:
            return f"{self.name} ({length}) DEFAULT '{self.default}'"
        else:
            return f"{self.name} ({length})"
