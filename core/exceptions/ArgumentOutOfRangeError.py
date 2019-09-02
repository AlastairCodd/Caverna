class ArgumentOutOfRangeError(Exception):
    def __init__(self, length_one: str, length_two: str) -> None:
        self.message = f"{length_one} is not equal to {length_two}"