import unittest
from ..Tokenizer import Tokenizer
from .TestUtils import get_full_path

class TestTokenizer(unittest.TestCase):
    def test_simple_table(self):
        content = None
        with open(get_full_path("examples/SimpleTable.sql"), "r") as file:
            content = file.read()

        tokens = Tokenizer().parse(content)
        assert list(map(str, tokens)) == ["CREATE", "TABLE", "LOGS", "(", "ID", "BIGINT", "NOT", "NULL", ",", "MESSAGE", "VARCHAR", "(", "500", ")", ",", "CONNECT_ID", "INTEGER", ",", "CONSTRAINT", "PK_AGENTLOGG", "PRIMARY", "KEY", "(", "ID", ")", ")", ";"]

    def test_quotes(self):
        tokens = Tokenizer().parse('"Test quote"')
        assert list(map(str, tokens)) == ['"', 'Test quote', '"']

    def test_quotes_and_text(self):
        tokens = Tokenizer().parse('"Test quote" AND ')
        assert list(map(str, tokens)) == ['"', 'Test quote', '"', "AND"]

    def test_comments_and_text(self):
        tokens = Tokenizer().parse("""
            -- This is a comment
            "quote"
        """)
        assert list(map(str, tokens)) == ['"', 'quote', '"']

    def test_long_comment_and_text(self):
        tokens = Tokenizer().parse("""
            /* This is a comment */
            "quote"
        """)
        assert list(map(str, tokens)) == ['"', 'quote', '"']

    def test_single_quote(self):
        tokens = Tokenizer().parse("""
            /* This is a comment */
            'quote'
        """)
        assert list(map(str, tokens)) == ["'", 'quote', "'"]

    def test_select_from_substring(self):
        tokens = Tokenizer().parse("""
            S = substring(new.ref from I for 1);
        """)
        print(list(map(str, tokens)))
        assert list(map(str, tokens)) == ['S', '=', 'substring', '(', 'new', '.', 'ref', 'from', 'I', 'for', '1', ')', ';']

if __name__ == '__main__':
    unittest.main()
