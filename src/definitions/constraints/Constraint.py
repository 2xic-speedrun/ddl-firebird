from ..TokenStreamer import TokenStreamer
from .ForeignKey import ForeignKey

class Constraint:
    def __init__(self) -> None:
        self.name = None

    def parse(self, token_stream: TokenStreamer):
        if token_stream.peek() == "CONSTRAINT":
            constraint = self
            token_stream.increment(1)
            self.name = token_stream.read()

            if token_stream.is_sequence(["PRIMARY", "KEY"]):
                token_stream.increment(2)
                token_stream = self._read_scope(token_stream)
            elif token_stream.is_sequence(["FOREIGN", "KEY"]):
                token_stream.increment(2)
                token_stream = self._read_scope(token_stream)
                assert token_stream.read() == "REFERENCES"
                target_table = token_stream.read()
                token_stream = self._read_scope(token_stream)
                token_stream = self._on_actions(token_stream)

                constraint = ForeignKey(
                    target_table=target_table
                )

            elif token_stream.is_sequence(["UNIQUE"]):
                token_stream.increment(1)
                token_stream = self._read_scope(token_stream)
            else:
                raise Exception("Unknown constraint " + token_stream.context)
            return (constraint, token_stream)
        return (None, token_stream)

    def _on_actions(self, token_stream: TokenStreamer):
        while token_stream.peek() == "ON":
            assert token_stream.read() == "ON"
            assert token_stream.read() in ["UPDATE", "DELETE"]
            if token_stream.is_sequence(["NO", "ACTION"]):
                token_stream.increment(2)
            elif token_stream.is_sequence(["CASCADE"]):
                token_stream.increment(1)
            elif token_stream.is_sequence(["SET", "DEFAULT"]):
                token_stream.increment(2)
            elif token_stream.is_sequence(["SET", "NULL"]):
                token_stream.increment(2)
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
