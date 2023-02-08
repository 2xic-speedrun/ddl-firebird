from .TokenStreamer import TokenStreamer

class Types:
    def __init__(self) -> None:
        self.name = None
        self.is_nullable = False
        self.default = None

    def parse(self, token_stream: TokenStreamer):
        self.name = token_stream.read()
        if self.name == "VARCHAR":
            token_stream = self._read_loop(token_stream)
        elif self.name == "NUMERIC":
            token_stream = self._read_loop(token_stream)
        else:
            pass

        if token_stream.is_sequence(["DEFAULT"]):
            token_stream = token_stream.increment(2)

        if token_stream.is_sequence(["NOT", "NULL"]):
            token_stream = token_stream.increment(2)

        return (self, token_stream)

    def _read_loop(self, token_stream):
        if token_stream.peek() == "(":
            while token_stream.read() != ")":
                pass
        return token_stream

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()
