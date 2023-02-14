from .TokenStreamer import TokenStreamer
from ..tokens.StringToken import StringToken
from .types.ReferenceType import ReferenceType

class Scope:
    def __init__(self):
        pass

    def parse_scope(self, token_stream):
        references_procedures = set([])
        references_tables = set([])
        reference_count = 1

        token_stream.increment(1)
        while reference_count != 0:
            raw_token = token_stream.tokens[token_stream.index]
            token = str(raw_token).upper()
            if token_stream.is_sequence(["SUBSTRING", "("]):
                while token_stream.read() != ")":
                    pass
                continue
            if token_stream.is_sequence(["EXECUTE", "PROCEDURE"]):
                references_procedures.add(
                    token_stream.peek(2).upper()
                )
            elif token_stream.is_sequence(["EXECUTE", "PROCEDURE"]):
                references_procedures.add(
                    token_stream.peek(2).upper()
                )
            elif token_stream.is_sequence(["INSERT", "INTO"]):
                references_tables.add(
                    ReferenceType(
                        token_stream.peek(2),
                        "INSERT"
                    )
                )
            elif token_stream.is_sequence(["UPDATE"]):
                references_tables.add(
                    ReferenceType(
                        token_stream.peek(1),
                        "UPDATE"
                    )
                )
            elif token_stream.is_sequence(["FROM"]):
                #  print(token_stream.context)
                if token_stream.peek().isalpha():
                    if token_stream.peek(2) == "(":
                        references_procedures.add(
                            token_stream.peek(1).upper()
                        )
                    else:
                        references_tables.add(
                            ReferenceType(
                                token_stream.peek(1),
                                "SELECT"
                            )
                        )

            if not isinstance(raw_token, StringToken):
                if token == "BEGIN" or token == "CASE":
                    reference_count += 1
                elif token == "END":
                    reference_count -= 1
            token_stream.increment(1)

        if token_stream.peek() == ";":
            token_stream.increment(1)

        return (
            token_stream,
            references_procedures,
            references_tables
        )
