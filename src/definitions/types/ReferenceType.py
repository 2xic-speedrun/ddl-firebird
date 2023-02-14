
class ReferenceType:
    def __init__(self, reference, type):
        assert type in ["UPDATE", "SELECT", "INSERT"]
        self.reference = reference
        self.type = type

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            other.reference == self.reference and
            other.type == self.type
        )

    def __hash__(self):
        return hash(self.reference + str(self.type))

    def __str__(self):
        return self.reference
