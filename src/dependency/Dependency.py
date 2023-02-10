from typing import Union
from ..definitions.Trigger import Trigger
from ..definitions.Procedure import Procedure
from ..definitions.Table import Table
from typing import List
import graphviz

class Dependency:
    def __init__(self, parsed) -> None:
        self.parsed = parsed

    def plot(self, procedure: str):
        dot = graphviz.Digraph(comment='Dependency', format='png')
        dependency = []
        visited = {}
        procedure = self.parsed.procedure_graph[procedure.upper()]
        self._resolve_dependency(procedure, dependency, visited, dot)
        dot.render('dependency')

    def get_procedure_dependency(self, procedure: str):
        # 1. First we need to know all tables
        # 2. Then we need to know all procedures
        # 3. Then we need to know all triggers
        dependency = []
        visited = {}
        procedure = self.parsed.procedure_graph[procedure.upper()]
        self._resolve_dependency(procedure, dependency, visited)
        return dependency

    def _resolve_dependency(self, item: Union[Trigger, Procedure, Table], dependency: List[str], visited, dot=None):
        self._plot_dot(dot, lambda: dot.node(item.name, item.name))

        if not isinstance(item, Table):
            revisit_tables = []
            for i in item.references_tables:
                self._plot_dot(dot, lambda: dot.edge(item.name, i))
                if i not in visited:
                    visited[i] = True
                    revisit_tables.append(i)
                    self._resolve_dependency(
                        self.parsed.table_graph[i],
                        dependency,
                        visited,
                        dot
                    )
            for i in item.references_procedures:
                self._plot_dot(dot, lambda: dot.edge(item.name, i))
                if i not in visited:
                    visited[i] = True
                    self._resolve_dependency(
                        self.parsed.procedure_graph[i],
                        dependency,
                        visited,
                        dot
                    )
        else:
            for i in item.triggers:
                self._plot_dot(dot, lambda: dot.edge(item.name, i.name))
                if i.name not in visited:
                    visited[i.name] = True
                    self._resolve_dependency(
                        i,
                        dependency,
                        visited,
                        dot
                    )

        dependency.append(item.name)

    def _plot_dot(self, dot, func):
        if dot is not None:
            func()
