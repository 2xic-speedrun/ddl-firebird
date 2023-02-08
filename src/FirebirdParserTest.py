import unittest
from .FirebirdParser import FirebirdParser

class TestFirebirdParser(unittest.TestCase):
    def test_simple_table(self):
        content = None
        with open("examples/SimpleTable.sql", "r") as file:
            content = file.read()

        table = FirebirdParser(content).parse()
        assert table.name == "LOGS"
        assert len(table.columns) == 3
        assert len(table.constraints) == 1

if __name__ == '__main__':
    unittest.main()
