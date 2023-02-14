from .TokenStreamer import TokenStreamer
from .types.Types import Types
from .helpers.StringReader import StringReader

class Column:
    def __init__(self) -> None:
        self.name = None
        self.type = None

    def parse(self, token_stream: TokenStreamer):
        (self.name, token_stream) = StringReader().read_string(token_stream)
        (self.type, token_stream) = Types().parse(token_stream)

        return (
            self,
            token_stream
        )

    def sql(self):
        return f"{self.name} {self.type.sql()}"

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()
