from .tokens.Token import Token

class Tokenizer:
    def __init__(self) -> None:
        pass

    def parse(self, text):
        index = 0
        tokens = []
        is_within_quote = False
        token = Token(is_within_quote)
        while index < len(text):
            char = text[index]
            complete = token.add_char(char)
            if complete:
                tokens.append(token)
                # TODO: Do this in a cleaner way
                if token.is_quote:
                    is_within_quote = not is_within_quote
                token = Token(is_within_quote)
            else:
                index += 1
        if token.text:
            tokens.append(token)
        return tokens
