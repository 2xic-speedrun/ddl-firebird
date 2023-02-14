import unittest
from ..FirebirdParser import FirebirdParser
from .TestUtils import get_full_path

class TestFirebirdParser(unittest.TestCase):
    def test_simple_table(self):
        content = None
        with open(get_full_path("examples/SimpleTable.sql"), "r") as file:
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
        with open(get_full_path("examples/MultipleTables.sql"), "r") as file:
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
        with open(get_full_path("examples/SimpleTableStringName.sql"), "r") as file:
            content = file.read()

        results = FirebirdParser(content).parse()
        tables = results.tables

        assert len(tables) == 1
        table = tables[0]
        assert table.columns[0].name == "ID"
        assert table.columns[1].name == "MESSAGE"
        assert table.columns[2].name == "CONNECT_ID"

    def test_column_table_types(self):
        content = None
        with open(get_full_path("examples/SimpleTableTypes.sql"), "r") as file:
            content = file.read()

        results = FirebirdParser(content).parse()
        tables = results.tables
        assert len(tables) == 1
        table = tables[0]
        assert len(table.columns) == 12
        assert table.columns[0].name == "ID"
        assert table.columns[0].type.name == "BIGINT"
        assert table.columns[0].type.is_nullable == False

        assert table.columns[1].name == "MESSAGE"
        assert table.columns[1].type.is_nullable == True
        assert table.columns[1].type.length == "500"

        assert table.columns[2].name == "CONNECT_ID"
        assert table.columns[2].type.name == "INTEGER"
        assert table.columns[2].type.is_nullable == True

        assert table.columns[3].name == "COST"

        assert table.columns[4].name == "CREATE_AT"
        assert table.columns[4].type.name == "DATE"
        assert table.columns[4].type.is_nullable == True

        assert table.columns[5].name == "REF"
        assert table.columns[5].type.name == "VARCHAR"
        assert table.columns[5].type.is_nullable == True

        assert table.columns[6].name == "DEFAULT_COST"
        assert table.columns[6].type.name == "NUMERIC"
        assert table.columns[6].type.default == "0"
        assert table.columns[6].type.is_nullable == False

        assert table.columns[7].name == "BOOLEAN"
        assert table.columns[7].type.name == "CHAR"
        assert table.columns[7].type.default == "N"
        assert table.columns[7].type.is_nullable == True

        assert table.columns[8].name == "DOCUMENT"
        assert table.columns[8].type.name == "BLOB"
        assert table.columns[8].type.default == None
        assert table.columns[8].type.is_nullable == True

        assert table.columns[9].name == "NOTES"
        assert table.columns[9].type.name == "BLOB"
        assert table.columns[9].type.default == None
        assert table.columns[9].type.is_nullable == True

        assert table.columns[10].name == "SATS"
        assert table.columns[10].type.name == "DOUBLE PRECISION"
        assert table.columns[10].type.default == '24.00'
        assert table.columns[10].type.is_nullable == True

        assert table.columns[11].name == "NEGATIVE_NUM"
        assert table.columns[11].type.name == "SMALLINT"
        assert table.columns[11].type.default == '-20'
        assert table.columns[11].type.is_nullable == True

        assert len(tables[0].constraints) == 1

    def test_table_and_index(self):
        content = None
        with open(get_full_path("examples/SimpleTableWithIndex.sql"), "r") as file:
            content = file.read()

        results = FirebirdParser(content).parse()
        assert len(results.tables) == 1
        assert len(results.indexes) == 2

        assert results.indexes[0].name == "FK_LOGS"
        assert results.indexes[1].name == "FK_LOGS_UQ"

    def test_table_with_foreign_key(self):
        content = None
        with open(get_full_path("examples/SimpleTableWithForeignKey.sql"), "r") as file:
            content = file.read()

        results = FirebirdParser(content).parse()
        assert len(results.tables) == 2

    def test_table_with_comments(self):
        content = None
        with open(get_full_path("examples/SimpleTableWithComments.sql"), "r") as file:
            content = file.read()

        results = FirebirdParser(content).parse()
        assert len(results.tables) == 1

    def test_procedures(self):
        content = None
        with open(get_full_path("examples/Procedure.sql"), "r") as file:
            content = file.read()

        results = FirebirdParser(content).parse()
        assert len(results.procedures) == 1
        assert results.procedures[0].name == "ISMULTIPLE"
        results.procedures[0].references_procedures = list(results.procedures[0].references_procedures)
        assert len(results.procedures[0].references_procedures) == 1
        assert results.procedures[0].references_procedures[0] == "LOG"

    def test_procedures_substring(self):
        content = None
        with open(get_full_path("examples/ProcedureSubString.sql"), "r") as file:
            content = file.read()

        results = FirebirdParser(content).parse()
        assert len(results.procedures) == 1
        assert results.procedures[0].name == "ISMULTIPLE"
        assert len(results.procedures[0].references_procedures) == 0
        assert len(results.procedures[0].references_tables) == 0

    def test_procedures_substring_2(self):
        content = None
        with open(get_full_path("examples/ProcedureSubString2.sql"), "r") as file:
            content = file.read()

        results = FirebirdParser(content).parse()
        assert len(results.procedures) == 1
        assert results.procedures[0].name == "ISMULTIPLE"
        assert len(results.procedures[0].references_procedures) == 0
        assert len(results.procedures[0].references_tables) == 0

    def test_trigger_substring(self):
        content = None
        with open(get_full_path("examples/TriggerWithSubstring.sql"), "r") as file:
            content = file.read()

        results = FirebirdParser(content).parse()
        assert len(results.triggers) == 1
        assert results.triggers[0].name == "LOGG_OF_CONNECTION_ID"
        assert len(results.triggers[0].references_procedures) == 0
        assert len(results.triggers[0].references_tables) == 0
        assert results.triggers[0].trigger_types == ['INSERT', 'UPDATE']

if __name__ == '__main__':
    unittest.main()
