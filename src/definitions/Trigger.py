from .TokenStreamer import TokenStreamer
from ..tokens.StringToken import StringToken

class Trigger:
    def __init__(self) -> None:
        self.name = None
        self.references_tables = set([])
        self.references_procedures = set([])
        self.target_table = None

    def parse(self, token_stream: TokenStreamer):
        if token_stream.is_sequence(["CREATE", "TRIGGER"]):
            token_stream.increment(2)
            (self.name, token_stream) = self._read_name(token_stream)
            assert token_stream.read() == "FOR"
            (self.target_table, token_stream) = self._read_name(token_stream)

            reference_count = 1
            early_stopping = False
            seen_as_keyword = False
            while not token_stream.is_sequence(["BEGIN"]):
                if token_stream.peek().upper() == "AS":
                    seen_as_keyword = True
                elif token_stream.peek() == ";" and not seen_as_keyword:
                    early_stopping = True
                    break
                token_stream = token_stream.increment(1)

            print(self.name, early_stopping, token_stream.tokens[token_stream.index:token_stream.index+3])
            if not early_stopping:
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
            return (self, token_stream)
        return (None, token_stream)

    def _read_name(self, token_stream: TokenStreamer):
        name = token_stream.read()
        if name == '"':
            name = token_stream.read()
            assert token_stream.read() == '"'
        return (name, token_stream)
