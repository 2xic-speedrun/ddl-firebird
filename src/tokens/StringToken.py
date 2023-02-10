
class StringToken:
    def __init__(self, token) -> None:
        self.token = token

    def __str__(self) -> str:
        return self.token

    def __repr__(self):
        return self.__str__()
