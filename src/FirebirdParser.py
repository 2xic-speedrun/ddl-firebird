from .definitions.TokenStreamer import TokenStreamer
from .definitions.Table import Table
from .Tokenizer import Tokenizer

class FirebirdParser:
    def __init__(self, text) -> None:
        self.tokens = Tokenizer().parse(text)
        self.streamer = TokenStreamer(self.tokens)

    def parse(self):
        tables = []
        streamer = self.streamer
        while not streamer.is_done:
            (table, streamer) = Table().parse(self.streamer)
            tables.append(table)      

        return tables

