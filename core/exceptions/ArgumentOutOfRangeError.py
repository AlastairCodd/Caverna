class ArgumentOutOfRangeError(Exception):
    def __init__(self, length_one: str = "", length_two: str = "") -> None:
        if length_one.isspace():
            self.message = "Argument is outside range"
        if length_two.isspace():
            self.message = f"{length_one} is outside range."
        self.message = f"{length_one} is not equal to {length_two}"
