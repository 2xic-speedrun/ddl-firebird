from ..TokenStreamer import TokenStreamer

class StringReader:
    def __init__(self):
        pass

    def read_string(self, token_stream: TokenStreamer):
        string = token_stream.read()
        if string == '"':
            string = token_stream.read()
            assert token_stream.read() == '"'
        return (string, token_stream)
