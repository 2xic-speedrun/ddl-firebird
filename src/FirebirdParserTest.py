import unittest
from .FirebirdParser import FirebirdParser

class TestFirebirdParser(unittest.TestCase):
    def test_simple_table(self):
        content = None
        with open("examples/SimpleTable.sql", "r") as file:
            content = file.read()

        tables = FirebirdParser(content).parse()
        assert len(tables) == 1
        table = tables[0]
        assert table.name == "LOGS"
        assert len(table.columns) == 3
        assert len(table.constraints) == 1

    def test_multiple_simple_table(self):
        content = None
        with open("examples/MultipleTables.sql", "r") as file:
            content = file.read()

        tables = FirebirdParser(content).parse()
        assert len(tables) == 2

        assert tables[0].name == "LOGS"
        assert len(tables[0].columns) == 3
        assert len(tables[0].constraints) == 1

        assert tables[1].name == "FROGS"
        assert len(tables[1].columns) == 2
        assert len(tables[1].constraints) == 1

if __name__ == '__main__':
    unittest.main()
