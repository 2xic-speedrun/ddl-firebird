from .TokenStreamer import TokenStreamer
from ..tokens.StringToken import StringToken
from .Scope import Scope
from .helpers.StringReader import StringReader

class Trigger:
    def __init__(self) -> None:
        self.name = None
        self.references_tables = set([])
        self.references_procedures = set([])
        self.target_table = None
        self.trigger_types = None

    def parse(self, token_stream: TokenStreamer):
        if token_stream.is_sequence(["CREATE", "TRIGGER"]):
            token_stream.increment(2)
            (self.name, token_stream) = StringReader().read_string(token_stream)
            assert token_stream.read() == "FOR"
            (self.target_table, token_stream) = StringReader().read_string(token_stream)

            self.trigger_types = self.read_trigger_type(token_stream)
            if token_stream.peek() == "POSITION":
                token_stream.increment(2)

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

            if not early_stopping:
                (token_stream, self.references_procedures, self.references_tables) = Scope().parse_scope(token_stream)

            return (self, token_stream)
        return (None, token_stream)

    def read_trigger_type(self, token_stream):
        if token_stream.peek() == "ACTIVE":
            token_stream.increment(1)
        assert token_stream.read() in ["BEFORE", "AFTER"], token_stream.context
        actions = []
        while True:
            actions.append(token_stream.read())
            if token_stream.peek() != "OR":
                break
            else:
                token_stream.increment(1)
        return actions

