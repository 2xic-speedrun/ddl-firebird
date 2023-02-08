from .TokenStreamer import TokenStreamer

class Constraint:
    def __init__(self) -> None:
        self.name = None

    def parse(self, token_stream: TokenStreamer):
        if token_stream.peek() == "CONSTRAINT":
            token_stream.increment(1)
            self.name = token_stream.read()

            if token_stream.is_sequence(["PRIMARY", "KEY"]):
                token_stream.increment(2)
                token_stream = self._read_scope(token_stream)
            elif token_stream.is_sequence(["FOREIGN", "KEY"]):
                token_stream.increment(2)
                token_stream = self._read_scope(token_stream)
                assert token_stream.read() == "REFERENCES"
                _name = token_stream.read()
                token_stream = self._read_scope(token_stream)
                token_stream = self._on_actions(token_stream)
            else:
                raise Exception("Unknown")
            return (self, token_stream)
        return (None, token_stream)

    def _on_actions(self, token_stream):
        while token_stream.peek() == "ON":
            token_stream.read()
            action = token_stream.read()
            results = token_stream.read()
        return token_stream

    def _read_scope(self, token_stream):
        assert token_stream.peek() == "("
        while token_stream.read() != ")":
            pass
        return token_stream

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()
