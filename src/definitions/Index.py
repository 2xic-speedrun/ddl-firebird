from .TokenStreamer import TokenStreamer

class Index:
    def __init__(self) -> None:
        self.name = None
        self.target_table = None
        self.columns = []

    def parse(self, token_stream: TokenStreamer):
        if  token_stream.is_sequence(["CREATE", "INDEX"]) or\
            token_stream.is_sequence(["CREATE", "UNIQUE", "INDEX"]):
            # TODO: Make this clean
            if token_stream.is_sequence(["CREATE", "UNIQUE", "INDEX"]):
                token_stream.increment(3)
            else:
                token_stream.increment(2)

            self.name = token_stream.read()

            assert token_stream.read() == "ON"

            self.target_table = token_stream.read()
            assert token_stream.read() == "("
            column = token_stream.read()
            while column != ")":
                self.columns.append(column)
                column = token_stream.read()
            assert token_stream.read() == ";"
            return (self, token_stream)
        return (None, token_stream)

    def __str__(self) -> str:
        return f"Index {self.name}"

    def __repr__(self):
        return self.__str__()
