from .TokenStreamer import TokenStreamer

class Column:
    def __init__(self) -> None:
        self.name = None
        self.type = None

    def parse(self, token_stream: TokenStreamer):
        # TYPE is special token
#        (constraints, token_stream) = self.parse_keyword(token_stream)
#        if constraints:
#            return (self, token_stream)
        name = token_stream.read()
        (type, token_stream) = self.parse_type(token_stream)

        self.type = type
        self.name = name

        return (
            self,
            token_stream
        )

    def parse_type(self, token_stream: TokenStreamer):
        type = token_stream.read()
        if type == "VARCHAR":
            # (500)
            token_stream.increment(3)
        else:
            pass
        if token_stream.is_sequence(["NOT", "NULL"]):
            token_stream = token_stream.increment(2)
        #    raise Exception("??")
        return (type, token_stream)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()
