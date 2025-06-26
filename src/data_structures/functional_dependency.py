
# functional_dependency.py
class FD:
    def __init__(self, lhs: set, rhs: set):
        self.__lhs = lhs  # Left-hand side of the functional dependency
        self.__rhs = rhs  # Right-hand side of the functional dependency

    def __str__(self) -> str:
        left = ''.join(sorted(self.__lhs))
        right = ''.join(sorted(self.__rhs))
        return f"{left} → {right}"

    def __repr__(self) -> str:
        return f"FD({self.__lhs}, {self.__rhs})"

    def getLhs(self):
        return self.__lhs

    def getRhs(self):
        return self.__rhs

    def setLhs(self, lhs: set):
        self.__lhs = lhs

    def setRhs(self, rhs: set):
        self.__rhs = rhs