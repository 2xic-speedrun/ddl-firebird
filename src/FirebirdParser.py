from .definitions.TokenStreamer import TokenStreamer
from .definitions.Table import Table
from .definitions.Index import Index
from .Tokenizer import Tokenizer

class FirebirdParser:
    def __init__(self, text) -> None:
        self.tokens = Tokenizer().parse(text)
        self.streamer = TokenStreamer(self.tokens)

        self.tables = []
        self.indexes = []

    def parse(self):
        streamer = self.streamer
        while not streamer.is_done:
            types = [
                Table(),
                Index()
            ]
            for i in types:            
                (results, streamer) = i.parse(self.streamer)
                if results is not None:
                    if isinstance(results, Table):
                        self.tables.append(results)
                    elif isinstance(results, Index):
                        self.indexes.append(results)
                    break
                
        return self

