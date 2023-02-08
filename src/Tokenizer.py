from .tokens.Token import Token

class Tokenizer:
    def __init__(self) -> None:
        pass

    def parse(self, text):
        index = 0
        tokens = []
        token = Token()
        while index < len(text):
            char = text[index]
            complete = token.add_char(char)
            if complete:
                tokens.append(token)
                token = Token()
            else:
                index += 1
        return tokens
