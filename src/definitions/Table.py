from .TokenStreamer import TokenStreamer
from .Column import Column
from .Constraint import Constraint

class Table:
    def __init__(self) -> None:
        self.name = None
        self.columns = []
        self.constraints = []

    def parse(self, token_stream: TokenStreamer):
        if token_stream.is_sequence(["CREATE", "TABLE"]):
            token_stream.increment(2)
            self.name = token_stream.read()
            if token_stream.read() == "(":
                while token_stream.peek() != ")":
                    (constraint, token_stream) = Constraint().parse_keyword(token_stream)
                    if constraint:
                        self.constraints.append(constraint)
                        continue
                    (column, token_stream) = Column().parse(token_stream)
                    if token_stream.peek() == ",":
                        token_stream.increment(1)
                    self.columns.append(column)
        return (self, token_stream)
