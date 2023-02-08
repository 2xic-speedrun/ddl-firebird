

class Token:
    def __init__(self) -> None:
        self.text = ""
        self.stop_char = [
            "(",
            ")",
            ",",
            ";",
        ]

    def add_char(self, char):
        is_white_space = len(char.strip()) == 0
        if (char in self.stop_char or is_white_space) and len(self.text):
            return True
        elif not is_white_space and self.text in self.stop_char:
            return True
        elif not is_white_space:
            self.text += char
        return False

    def __str__(self) -> str:
        return self.text

    def __repr__(self):
        return self.__str__()
