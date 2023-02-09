from .definitions.TokenStreamer import TokenStreamer
from .definitions.Table import Table
from .definitions.Index import Index
from .Tokenizer import Tokenizer
import sys
import time
from .helper.Timer import Timer, timer
from typing import List, Dict

class FirebirdParser:
    def __init__(self, text) -> None:
        self.tokens = Tokenizer().parse(text)
        self.streamer = TokenStreamer(self.tokens)

        self.tables: List[Table] = []
        self.indexes: List[Index] = []
        self.graph: Dict[str, Table] = {

        }

    @timer
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
                        self.graph[results.name] = results
                    elif isinstance(results, Index):
                        self.indexes.append(results)
                    break
            else:
                raise SyntaxError("Close to " + streamer.context)
        for i in self.indexes:
            self.graph[results.target_table].indexes.append(i)
        return self

def get_table_info(results: FirebirdParser, table: str):
    reference = results.graph[table]
    print(reference.sql())
    for i in reference.references_():
        get_table_info(results, i)

if __name__ == "__main__":
    # TODO: Add nice cli interface
    arguments = sys.argv[1]
    debug = False
    content = None
    with open(arguments, "r") as file:
        content = file.read()
    start = time.time()
    results = FirebirdParser(content).parse()

    print(results.tables)
