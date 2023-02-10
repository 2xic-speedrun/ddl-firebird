from .TokenStreamer import TokenStreamer
from ..tokens.StringToken import StringToken

class Procedure:
    def __init__(self) -> None:
        self.name = None
        self.references_tables = set([])
        self.references_procedures = set([])
        self.source = ""

    def parse(self, token_stream: TokenStreamer):
        if token_stream.is_sequence(["CREATE", "PROCEDURE"]) or \
            token_stream.is_sequence(["CREATE", "OR", "ALTER", "PROCEDURE"]):
            start_index = token_stream.index
            if token_stream.is_sequence(["CREATE", "OR", "ALTER", "PROCEDURE"]):
                token_stream.increment(4)
            else:
                token_stream.increment(2)
            self.name = token_stream.read().upper()

            reference_count = 1
            while not token_stream.is_sequence(["BEGIN"]):
                token_stream = token_stream.increment(1)
            token_stream.increment(1)
            while reference_count != 0:
                raw_token = token_stream.tokens[token_stream.index]
                token = str(raw_token).upper()

                if token_stream.is_sequence(["EXECUTE", "PROCEDURE"]):
                    self.references_procedures.add(
                        token_stream.peek(2).upper()
                    )
                elif token_stream.is_sequence(["EXECUTE", "PROCEDURE"]):
                    self.references_procedures.add(
                        token_stream.peek(2).upper()
                    )
                elif token_stream.is_sequence(["INSERT", "INTO"]):
                    self.references_tables.add(
                        token_stream.peek(2)
                    )
                elif token_stream.is_sequence(["UPDATE"]):
                    self.references_tables.add(
                        token_stream.peek(1)
                    )
                elif token_stream.is_sequence(["FROM"]):
                    if token_stream.peek().isalpha():
                        if token_stream.peek(2) == "(":
                            self.references_procedures.add(
                                token_stream.peek(1).upper()
                            )
                        else:
                            self.references_tables.add(
                                token_stream.peek(1)
                            )

                if not isinstance(raw_token, StringToken):
                    if token == "BEGIN" or token == "CASE":
                        reference_count += 1
                    elif token == "END":
                        reference_count -= 1
                token_stream.increment(1)

            if token_stream.peek() == ";":
                token_stream.increment(1)
            self.source = " ".join(list(map(str, token_stream.tokens[start_index:token_stream.index])))
            return (self, token_stream)
        return (None, token_stream)

