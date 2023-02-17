from .TokenStreamer import TokenStreamer
from ..tokens.StringToken import StringToken
from .Scope import Scope

class Procedure:
    def __init__(self) -> None:
        self.name = None
        self.references_tables = set([])
        self.references_procedures = set([])
        self.source = ""

    def parse(self, token_stream: TokenStreamer):
        if token_stream.is_sequence(["CREATE", "PROCEDURE"]) or \
            token_stream.is_sequence(["ALTER", "PROCEDURE"]) or \
            token_stream.is_sequence(["CREATE", "OR", "ALTER", "PROCEDURE"]):
            start_index = token_stream.index
            if token_stream.is_sequence(["CREATE", "OR", "ALTER", "PROCEDURE"]):
                token_stream.increment(4)
            else:
                token_stream.increment(2)
            self.name = token_stream.read().upper()

            while not token_stream.is_sequence(["BEGIN"]):
                token_stream = token_stream.increment(1)

            (token_stream, self.references_procedures, self.references_tables) = Scope().parse_scope(token_stream)

            self.source = " ".join(list(map(str, token_stream.tokens[start_index:token_stream.index])))
            return (self, token_stream)
        return (None, token_stream)

