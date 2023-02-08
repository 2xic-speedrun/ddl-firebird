from .TokenStreamer import TokenStreamer
from .Types import Types

class Column:
    def __init__(self) -> None:
        self.name = None
        self.type = None

    def parse(self, token_stream: TokenStreamer):
        (name, token_stream) = self.get_name(token_stream)
        (type, token_stream) = Types().parse(token_stream)

        self.type = type
        self.name = name

        return (
            self,
            token_stream
        )

    def get_name(self, token_streamer):
        if token_streamer.peek() == '"':
            token_streamer.read()
            name = token_streamer.read()
            token_streamer.read()
            return (name, token_streamer)
        else:
            return (token_streamer.read(), token_streamer)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()
