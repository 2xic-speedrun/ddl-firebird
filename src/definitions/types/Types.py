from ..TokenStreamer import TokenStreamer
from .Varchar import Varchar

class Types:
    def __init__(self) -> None:
        self.name = None
        self.is_nullable = True
        self.default = None
        self.parameters = None

    def parse(self, token_stream: TokenStreamer):
        type = self

        if token_stream.is_sequence(["DOUBLE", "PRECISION"]):
            self.name = token_stream.read() + " " + token_stream.read()
        else:
            self.name = token_stream.read()
            if self.name == "VARCHAR" or self.name == "CHAR":
                (token_stream, values) = self._read_loop(token_stream)
                type = Varchar()
                type.name = self.name
                assert len(values) <= 1, values
                if len(values):
                    type.length = values[0]
            elif self.name == "NUMERIC":
                (token_stream, values) = self._read_loop(token_stream)
                self.parameters = f"({' '.join(values)})"
            elif self.name == "BLOB":
                self.parameters = ""
                self.parameters += token_stream.read()
                self.parameters += " "
                if token_stream.peek() == "-":
                    self.parameters += token_stream.read()
                self.parameters += token_stream.read()
                assert token_stream.peek() in [",", ")"], token_stream.peek()

        if token_stream.is_sequence(["DEFAULT"]):
            token_stream.increment(1)
            (token_stream, default) = self._read_default(token_stream)
            type.default = default

        if token_stream.is_sequence(["NOT", "NULL"]):
            token_stream = token_stream.increment(2)
            type.is_nullable = False

        return (type, token_stream)

    def _read_default(self, token_stream: TokenStreamer):
        if token_stream.peek() == "'":
            token_stream.increment(1)
            value = token_stream.read()
            token_stream.increment(1)

            return (token_stream, value)
        elif token_stream.peek().isnumeric():
            value = token_stream.read()
            if token_stream.peek() == ".":
                value += token_stream.read()
                value += token_stream.read()
            return (token_stream, value)
        else:
            return (token_stream, token_stream.read())

    def _read_loop(self, token_stream: TokenStreamer):
        values = []
        if token_stream.peek() == "(":
            token_stream.increment(1)
            value = token_stream.read()
            while value != ")":
                values.append(value)
                value = token_stream.read()
        return (token_stream, values)

    def sql(self):
        results = f"{self.name}"
        if self.parameters is not None:
            results = f"{self.name} {self.parameters}"

        if self.default is not None:
            results = f"{results} DEFAULT {self.default}"

        return results

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()
