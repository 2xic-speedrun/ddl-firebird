from .tokens.Token import Token
from .tokens.StringToken import StringToken
from .tokens.Scanner import Scanner
from .helper.Timer import timer

class Tokenizer:
    def parse(self, text):
        return self.find_token(text)

    @timer
    def find_token(self, text):
        output = []
        for i in Scanner().find_tokens(text):
            if isinstance(i, StringToken):
                token = i
            else:
                token = Token(i)
            output.append(token)
        return output
