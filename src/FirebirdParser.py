from .definitions.TokenStreamer import TokenStreamer
from .definitions.Table import Table
from .Tokenizer import Tokenizer

class FirebirdParser:
    def __init__(self, text) -> None:
        self.tokens = Tokenizer().parse(text)
        self.streamer = TokenStreamer(self.tokens)

    def parse(self):
        prev_index = self.streamer.index
        (table, streamer) = Table().parse(self.streamer)
                
        #if streamer.index != prev_index:
        #    raise Exception("Streamer did not move")

        return table

