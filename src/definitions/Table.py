from .TokenStreamer import TokenStreamer
from .Column import Column
from .Constraint import Constraint
from typing import List, Union

class Table:
    def __init__(self) -> None:
        self.name = None
        self.columns = []
        self.constraints = []

    def parse(self, token_stream: TokenStreamer):
        # TODO: add a method, increment if sequence
        if token_stream.is_sequence(["CREATE", "TABLE"]):
            token_stream.increment(2)
            self.name = token_stream.read()
            # TODO: add a method, while inside loop
            if token_stream.read() == "(":
                while token_stream.peek() != ")":
                    keywords: List[Union[Constraint, Column]] = [
                        Constraint(),
                        Column(),
                    ]
                    for i in keywords:
                        (definition, token_stream) = i.parse(token_stream)
                        if definition is not None:
                            if isinstance(definition, Constraint):
                                self.constraints.append(definition)
                                break
                            else:
                                self.columns.append(definition)
                                break
                    if token_stream.peek() == ",":
                        token_stream.increment(1)
                token_stream.increment(1)
                assert token_stream.read() == ";"            
            return (self, token_stream)
        return (None, token_stream)
