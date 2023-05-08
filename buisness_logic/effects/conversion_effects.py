from typing import Dict
from core.baseClasses.base_effect import BaseEffect
from core.enums.caverna_enums import ResourceTypeEnum


class ConvertEffect(BaseEffect):
    def __init__(
            self,
            input_items: Dict[ResourceTypeEnum, int],
            output_items: Dict[ResourceTypeEnum, int]) -> None:
        """Optional conversion. Pay input and get output

        :param input_items:
        :param output_items:
        """
        self._input: Dict[ResourceTypeEnum, int] = input_items
        self._output: Dict[ResourceTypeEnum, int] = output_items
        BaseEffect.__init__(self, False)

    @property
    def input(self) -> Dict[ResourceTypeEnum, int]:
        return self._input

    @property
    def output(self) -> Dict[ResourceTypeEnum, int]:
        return self._output

    def __str__(self) -> str:
        return self.__format__(" ")

    def __format__(self, format_spec) -> str:
        text = [("", "Convert ")]
        for (i, (resource, amount)) in enumerate(self._input.items()):
            text.append(("class:count", str(amount)))
            text.append(("", " "))
            text.append(("", resource.name))
            if i == len(self._input) - 1:
                break
            text.append(("", ", "))

        text.append(("", " into "))

        for (i, (resource, amount)) in enumerate(self._output.items()):
            text.append(("class:count", str(amount)))
            text.append(("", " "))
            text.append(("", resource.name))
            if i == len(self._output) - 1:
                break
            text.append(("", ", "))

        if format_spec == "pp":
            return text
        if not format_spec:
            return "".join(e[1] for e in text)
        raise ValueError(f"format parameter must be 'pp' or whitespace/empty, was {format_spec!r}")

    def __repr__(self):
        return f"ConvertEffect({self._input}, {self._output})"
