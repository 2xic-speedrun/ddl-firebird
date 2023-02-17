from ..helper.Timer import timer
from .StringToken import StringToken

class Scanner:
    def __init__(self) -> None:
        self.index = 0

        self.quote = [
            '"'
        ]
        self.stop_char = self.quote + [
            "(",
            ")",
            ",",
            ";",
            "-",
            ".",
            "=",
            "/",
            "*",
            ":",
            "+",
            ">",
            "<",
            "|",
            "!",
            "^"
        ]

    @timer
    def find_tokens(self, text):
        self.index = 0
        token = ""
        while self.index < len(text):
            if self.get_text(text, self.index, self.index + 1) == "--":
                if len(token):
                    yield token
                while text[self.index] != "\n":
                    self.index += 1
                continue
            elif self.get_text(text, self.index, self.index + 1) == "/*":
                if len(token):
                    yield token
                while self.get_text(text, self.index, self.index + 1) != "*/":
                    self.index += 1
                self.index += 2
                continue
            elif text[self.index] in ['"', "'"]:
                quote_type = text[self.index]
                yield text[self.index]
                self.index += 1
                while text[self.index] != quote_type:
                    token += text[self.index]
                    self.index += 1
                yield StringToken(token)
                yield text[self.index]
                self.index += 1
                token = ""
            elif text[self.index] in [" ", "\t", "\n"]:
                if len(token):
                    yield token
                token = ""
                self.index += 1
            elif text[self.index] in self.stop_char:
                if len(token):
                    yield token
                yield text[self.index]
                token = ""
                self.index += 1
            elif text[self.index].isalnum() or text[self.index] in ["_", "$"]:
                token += text[self.index]
                self.index += 1
            else:
                print(text[self.index])
                print(text[self.index-5:self.index])
                raise Exception("???")

    @timer
    def get_text(self, text, from_index, to_index):
        if to_index < len(text):
            chars = ""
            for i in range(from_index, to_index + 1):
                chars += text[i]
            return chars
        return ""
