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
                assert token_stream.peek() == "("
                while token_stream.read() != ")":
                    pass
                return (self, token_stream)
            else:
                raise Exception("??")
        return (None, token_stream)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()
