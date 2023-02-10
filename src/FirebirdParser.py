from .definitions.TokenStreamer import TokenStreamer
from .definitions.Table import Table
from .definitions.Index import Index
from .Tokenizer import Tokenizer
import sys
import time
from .helper.Timer import Timer, timer
from typing import List, Dict
from .definitions.Procedure import Procedure
from .definitions.Trigger import Trigger
from .dependency.Dependency import Dependency

class FirebirdParser:
    def __init__(self, text) -> None:
        self.tokens = Tokenizer().parse(text)
        self.streamer = TokenStreamer(self.tokens)

        self.tables: List[Table] = []
        self.indexes: List[Index] = []
        self.procedures: List[Procedure] = []
        self.triggers: List[Trigger] = []

        self.table_graph: Dict[str, Table] = {}
        self.procedure_graph: Dict[str, Procedure] = {}

    @timer
    def parse(self):
        streamer = self.streamer
        while not streamer.is_done:
            if streamer.peek() == ";":
                streamer.increment(1)
                continue
            types = [
                Table(),
                Index(),
                Procedure(),
                Trigger()
            ]
            for i in types:
                (results, streamer) = i.parse(self.streamer)
              #  print((results))
                if results is not None:
                    if isinstance(results, Table):
                        self.tables.append(results)
                        self.table_graph[results.name] = results
                    elif isinstance(results, Index):
                        self.indexes.append(results)
                    elif isinstance(results, Procedure):
                        self.procedures.append(results)
                        self.procedure_graph[results.name] = results
                    elif isinstance(results, Trigger):
                        self.triggers.append(results)
                    break
                print(results)
            else:
                raise SyntaxError("Close to " + streamer.context)
        for i in self.triggers:
            if i.target_table in self.table_graph:
                self.table_graph[i.target_table].triggers.append(i)
        for i in self.procedures:
            self.procedure_graph[i.name] = i
    #    for i in self.indexes:
    #        self.table_graph[results.target_table].indexes.append(i)
        return self

def get_table_info(results: FirebirdParser, table: str):
    reference = results.table_graph[table]
    print(reference.sql())
    for i in reference.references_():
        get_table_info(results, i)

if __name__ == "__main__":
    # TODO: Add nice cli interface
    arguments = sys.argv[1]
    procedure = sys.argv[2]
    debug = False
    content = None
    with open(arguments, "r") as file:
        content = file.read()
    start = time.time()
    results = FirebirdParser(content).parse()
    dependency = Dependency(results)
    print(results.tables)

    dependency.plot(procedure)
    
