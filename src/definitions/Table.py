from .TokenStreamer import TokenStreamer
from .Column import Column
from .Index import Index
from .constraints.Constraint import Constraint
from .constraints.ForeignKey import ForeignKey
from typing import List, Union
from ..helper.Timer import timer
from .Trigger import Trigger

class Table:
    def __init__(self) -> None:
        self.name = None
        self.columns: List[Column] = []
        self.constraints: List[Constraint] = []
        self.indexes: List[Index] = []
        self.triggers: List[Trigger] = []

    @timer
    def parse(self, token_stream: TokenStreamer):
        # TODO: add a method, increment if sequence
        if token_stream.is_sequence(["CREATE", "TABLE"]):
            token_stream.increment(2)
            (name, token_stream) = self._read_name(token_stream)
            self.name = name
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
                            if isinstance(definition, Constraint) or \
                                isinstance(definition, ForeignKey):
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

    def sql(self):
        columns = ",\n".join([
            f"\t{i.sql()}" for i in self.columns
        ])
        statements = [
            f'CREATE TABLE "{self.name}" (',
            columns,
            ');'
        ]
        return "\n".join(statements)

    def _read_name(self, token_stream: TokenStreamer):
        name = token_stream.read()
        if name == '"':
            name = token_stream.read()
            assert token_stream.read() == '"'
        return (name, token_stream)

    def references_(self):
        for i in self.constraints:
            if isinstance(i, ForeignKey):
                yield i.target_table

    def __str__(self) -> str:
        format = f"Table {self.name}\n" + "\n".join([
            f"\t{column.name}" for column in self.columns
        ])
        return format

    def __repr__(self):
        return self.__str__()
