

class TokenStreamer:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.index = 0

    @property
    def is_done(self):
        return self.index == len(self.tokens)

    def peek(self, step=0):
        return str(self.tokens[self.index + step])

    def read(self):
        results = self.peek()
        self.increment(1)
        return results

    def is_sequence(self, tokens):
        if list(map(str, self.tokens[self.index:self.index+len(tokens)])) == tokens:
            return True
        return False

    def increment(self, step):
        self.index += step
        return self

    @property
    def context(self):
        tokens = self.tokens[max(self.index-5, 0):self.index + 5]
        return " ".join(list(map(str, tokens)))
