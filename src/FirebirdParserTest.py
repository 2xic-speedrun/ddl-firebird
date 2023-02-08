import unittest
from .FirebirdParser import FirebirdParser

class TestFirebirdParser(unittest.TestCase):
    def test_simple_table(self):
        content = None
        with open("examples/SimpleTable.sql", "r") as file:
            content = file.read()

        results = FirebirdParser(content).parse()
        tables = results.tables
        assert len(tables) == 1
        table = tables[0]
        assert table.name == "LOGS"
        assert len(table.columns) == 3
        assert len(table.constraints) == 1

    def test_multiple_simple_table(self):
        content = None
        with open("examples/MultipleTables.sql", "r") as file:
            content = file.read()

        results = FirebirdParser(content).parse()
        tables = results.tables
        assert len(tables) == 2

        assert tables[0].name == "LOGS"
        assert len(tables[0].columns) == 3
        assert len(tables[0].constraints) == 1

        assert tables[1].name == "FROGS"
        assert len(tables[1].columns) == 2
        assert len(tables[1].constraints) == 1

    def test_column_string_name(self):
        content = None
        with open("examples/SimpleTableStringName.sql", "r") as file:
            content = file.read()

        results = FirebirdParser(content).parse()
        tables = results.tables

        assert len(tables) == 1
        table = tables[0]
        assert table.columns[0].name == "ID"
        assert table.columns[1].name == "MESSAGE"
        assert table.columns[2].name == "CONNECT_ID"

    def column_table_types(self):
        content = None
        with open("examples/SimpleTableTypes.sql", "r") as file:
            content = file.read()

        results = FirebirdParser(content).parse()
        tables = results.tables
        assert len(tables) == 1
        table = tables[0]
        assert len(table.columns) == 7
        assert table.columns[0].name == "ID"
        assert table.columns[1].name == "MESSAGE"
        assert table.columns[2].name == "CONNECT_ID"
        assert table.columns[3].name == "COST"
        assert table.columns[4].name == "CREATE_AT"
        assert table.columns[5].name == "REF"
        assert table.columns[6].name == "DEFAULT_COST"

        assert len(tables[1].constraints) == 1

    def test_table_and_index(self):
        content = None
        with open("examples/SimpleTableWithIndex.sql", "r") as file:
            content = file.read()

        results = FirebirdParser(content).parse()
        assert len(results.tables) == 1
        assert len(results.indexes) == 1

        assert results.indexes[0].name == "FK_LOGS"

    def test_table_with_foreign_key(self):
        content = None
        with open("examples/SimpleTableWithForeignKey.sql", "r") as file:
            content = file.read()

        results = FirebirdParser(content).parse()
        assert len(results.tables) == 2

if __name__ == '__main__':
    unittest.main()
