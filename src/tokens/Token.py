

class Token:
    def __init__(self, is_within_quote) -> None:
        self.text = ""
        self.quote = [
            '"'
        ]
        self.stop_char = self.quote + [
            "(",
            ")",
            ",",
            ";",
        ]
        self.is_within_quote = is_within_quote

    def add_char(self, char):
        is_white_space = len(char.strip()) == 0        
        is_text_special_token = not is_white_space and self.text in self.stop_char
        is_current_char_a_stop_char_or_space = not self.is_within_quote and (char in self.stop_char or is_white_space) and len(self.text)
        is_quote_end = char in self.quote or self.text in self.quote

        """
            This looks complicated.
        """
        if is_current_char_a_stop_char_or_space:
            return True
        elif self.is_within_quote:
            if is_quote_end and len(self.text):
                return True
            self.text += char
        elif is_text_special_token:
            return True
        elif not is_white_space:
            self.text += char
        return False

    @property
    def is_quote(self):
        return self.text in self.quote

    def __str__(self) -> str:
        return self.text

    def __repr__(self):
        return self.__str__()
