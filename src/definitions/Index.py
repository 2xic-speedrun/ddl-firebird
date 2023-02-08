from .TokenStreamer import TokenStreamer

class Index:
    def __init__(self) -> None:
        self.name = None
        self.target_table = None
        self.columns = []

    def parse(self, token_stream: TokenStreamer):
        if token_stream.is_sequence(["CREATE", "INDEX"]):
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
        