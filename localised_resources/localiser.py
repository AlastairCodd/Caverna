from enum import Enum
from typing import List, Union, Dict

from core.enums.caverna_enums import ResourceTypeEnum
from localised_resources import user_interface_res


def format_list_with_separator(
        list_to_convert: List[Union[Enum, str]],
        separator: str) -> str:
    result: str
    if len(list_to_convert) > 1:
        result = ", ".join([entry.name for entry in list_to_convert[:-1]]) \
            if isinstance(list_to_convert[0], Enum) \
            else ", ".join(list_to_convert[:-1])

        final_value: str = list_to_convert[-1].name if isinstance(list_to_convert[0], Enum) else list_to_convert[-1]
        result += separator + final_value
    else:
        result = list_to_convert[0].name \
            if isinstance(list_to_convert[0], Enum) \
            else list_to_convert[0]
    return result


def format_resource_dict(
        resources: Dict[ResourceTypeEnum, int],
        separator: str) -> str:
    resources_readable: List[str] = [f"{amount} {resource.name if amount == 1 else user_interface_res.resource_plural_name[resource]}"\
                                     for resource, amount in resources.items()]
    return format_list_with_separator(resources_readable, separator)
