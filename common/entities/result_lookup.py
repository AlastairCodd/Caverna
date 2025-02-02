from typing import Generic, TypeVar, Iterable, Union, List

T = TypeVar('T')


class ResultLookup(Generic[T]):
    def __init__(
            self,
            flag: bool = None,
            value: Union[T, None] = None,
            errors: Union[str, Iterable[str], None] = None):
        self._flag: bool
        self._value: Union[T, None]
        self._errors: List[str]

        if flag is None:
            if errors is None:
                raise ValueError("both flag and errors cannot be none simultaneously")
            else:
                self._flag = False
                self._value = None
                if isinstance(errors, str):
                    self._errors = [errors]
                else:
                    self._errors = list(errors)
        else:
            self._flag = flag
            self._value = value
            self._errors = [] if errors is None else [errors] if isinstance(errors, str) else list(errors)

    @property
    def flag(self) -> bool:
        return self._flag

    @property
    def value(self) -> Union[T, None]:
        return self._value

    @property
    def errors(self) -> Iterable[str]:
        return self._errors

    def __str__(self) -> str:
        errors_str: str = ""
        number_of_errors = len(self._errors)
        for i in range(number_of_errors):
            if i == number_of_errors - 1:
                errors_str += f"{self._errors[i]}"
            else:
                errors_str += f"{self._errors[i]}, "

        result: str = f"ResultLookup({self._flag}, {self._value}, errors=[{errors_str}])"

        return result
