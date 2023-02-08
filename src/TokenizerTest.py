import unittest
from .Tokenizer import Tokenizer
import json

class TestTokenizer(unittest.TestCase):
    def test_simple_table(self):
        content = None
        with open("examples/SimpleTable.sql", "r") as file:
            content = file.read()

        tokens = Tokenizer().parse(content)
        assert list(map(str, tokens)) == ["CREATE", "TABLE", "LOGS", "(", "ID", "BIGINT", "NOT", "NULL", ",", "MESSAGE", "VARCHAR", "(", "500", ")", ",", "CONNECT_ID", "INTEGER", ",", "CONSTRAINT", "PK_AGENTLOGG", "PRIMARY", "KEY", "(", "ID", ")", ")", ";"]

    def test_quotes(self):
        tokens = Tokenizer().parse('"Test quote"')        
        assert list(map(str, tokens)) == ['"', 'Test quote', '"']

    def test_quotes_and_text(self):
        tokens = Tokenizer().parse('"Test quote" AND ')        
        assert list(map(str, tokens)) == ['"', 'Test quote', '"', "AND"]

if __name__ == '__main__':
    unittest.main()
