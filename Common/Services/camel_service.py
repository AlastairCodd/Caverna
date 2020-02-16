from enum import Enum, auto
from typing import Union, List, Dict, Tuple, Callable

from common.entities.result_lookup import ResultLookup
from common.forges.list_permutation_forge import ListPermutationForge


class CamelColourEnum(Enum):
    white = auto()
    yellow = auto()
    green = auto()
    blue = auto()
    orange = auto()


class OasisTypeEnum(Enum):
    positive = auto()
    negative = auto()


class CamelService(object):
    def __init__(
            self,
            camels_which_move_backwards: Union[List[CamelColourEnum], None] = None,
            number_of_dice_to_roll: int = 5):
        self._list_permutation_forge: ListPermutationForge = ListPermutationForge()
        if camels_which_move_backwards is None:
            camels_which_move_backwards = []

        self._camels_which_move_backwards: List[CamelColourEnum] = camels_which_move_backwards
        self._number_of_dice_to_roll: int = number_of_dice_to_roll

        self._camel_dice: Dict[CamelColourEnum, Dict[int, int]] = {}
        forward_dice: Dict[int, int] = {1:1, 2:1, 3:1}
        backward_dice: Dict[int, int] = {-1:1, -2:1, -3:1}

        for camel in CamelColourEnum:
            if camel in camels_which_move_backwards:
                self._camel_dice[camel] = backward_dice
            else:
                self._camel_dice[camel] = forward_dice

    def get_possible_positions_for_camels(
            self,
            camel_positions: Dict[int, List[CamelColourEnum]],
            oasis_positions: Union[Dict[int, OasisTypeEnum], None]) -> Dict[CamelColourEnum, Dict[int, float]]:
        """

        :param camel_positions: A dictionary keyed by position along the track, and a list containing the camels at this position.
            The list of camels is from highest camel (index 0) to lower camels down the stack. The dictionary does not have to contain
            keys for all positions along the track, but may not be none.
        :param oasis_positions: A dictionary keyed by position along the track, and the Oasis that is contained at that position. If
            the key is not in the dictionary, then no oasis is at this position. This dictionary may be null, in which case no oasis
            are placed.
        :returns: Something. This will never be null.
        """
        camel_dice_order: List[CamelColourEnum]
        for camel_dice_order in self._list_permutation_forge.generate_list_partitions([camel for camel in CamelColourEnum]):
            for camel in camel_dice_order:
                for dice in self._camel_dice[camel]:
                    print(dice)

    def _move_camel(
            self,
            camel: CamelColourEnum,
            steps: int,
            camel_positions: Dict[int, List[CamelColourEnum]],
            oasis_positions: Union[Dict[int, OasisTypeEnum], None] = None) -> ResultLookup[Dict[int, List[CamelColourEnum]]]:
        result: ResultLookup[Dict[int, List[CamelColourEnum]]]

        if oasis_positions is None:
            oasis_positions = {}

        camel_position_result: ResultLookup[Tuple[int, List[CamelColourEnum]]] = self._find_camel_stack(camel, camel_positions)

        if not camel_position_result.flag:
            result = ResultLookup(errors=camel_position_result.errors)
        else:
            camel_position: int
            camel_stack: List[CamelColourEnum]
            camel_position, camel_stack = camel_position_result.value

            result_camel_position: int = camel_position + steps
            result_camel_positions: Dict[int, List[CamelColourEnum]] = {}
            for position, stack in camel_positions.items():
                result_camel_positions[position]: List[CamelColourEnum] = []
                for stationary_camel in stack:
                    if stationary_camel not in camel_stack:
                        result_camel_positions[position].append(stationary_camel)

            if result_camel_position in oasis_positions:
                oasis_type: OasisTypeEnum = oasis_positions[result_camel_position]
                if oasis_type == OasisTypeEnum.positive:
                    camel_direction: int
                    if camel in self._camels_which_move_backwards:
                        camel_direction = -1
                    else:
                        camel_direction = 1

                    result_camel_position += camel_direction
                    if result_camel_position not in result_camel_positions:
                        result_camel_positions[result_camel_position] = []

                    result_camel_positions[result_camel_position] = self._place_camel_at_position_on_top(
                        camel_stack,
                        result_camel_positions[result_camel_position])
                if oasis_type == OasisTypeEnum.negative:
                    camel_direction: int
                    if camel in self._camels_which_move_backwards:
                        camel_direction = 1
                    else:
                        camel_direction = -1

                    result_camel_position += camel_direction
                    if result_camel_position not in result_camel_positions:
                        result_camel_positions[result_camel_position] = []

                    result_camel_positions[result_camel_position] = self._place_camel_at_position_on_bottom(
                        camel_stack,
                        result_camel_positions[result_camel_position])
            else:
                if result_camel_position not in result_camel_positions:
                    result_camel_positions[result_camel_position] = []

                result_camel_positions[result_camel_position] = self._place_camel_at_position_on_top(
                    camel_stack,
                    result_camel_positions[result_camel_position])

            result = ResultLookup(True, result_camel_positions)
        return result

    def _find_camel_stack(
            self,
            camel: CamelColourEnum,
            camel_positions: Dict[int, List[CamelColourEnum]]) -> ResultLookup[Tuple[int, List[CamelColourEnum]]]:
        success: bool = False
        result_position: int = -1
        result_camel_stack: List[CamelColourEnum] = []

        for position in camel_positions:
            camels_at_position: List[CamelColourEnum] = camel_positions[position]
            if camel in camels_at_position:
                success = True
                result_position = position
                result_camel_stack = camels_at_position[:camels_at_position.index(camel) + 1]
                break

        result: ResultLookup[Tuple[int, List[CamelColourEnum]]]
        if success:
            result_value: Tuple[int, List[CamelColourEnum]] = (result_position, result_camel_stack)
            result = ResultLookup(success, result_value)
        else:
            result = ResultLookup(errors=f"camel {camel.name} not found at any position")

        return result

    def _place_camel_at_position_on_top(
            self,
            moving_camel_stack: List[CamelColourEnum],
            current_camel_stack: List[CamelColourEnum]) -> List[CamelColourEnum]:
        result: List[CamelColourEnum] = moving_camel_stack + current_camel_stack
        return result

    def _place_camel_at_position_on_bottom(
            self,
            moving_camel_stack: List[CamelColourEnum],
            current_camel_stack: List[CamelColourEnum]) -> List[CamelColourEnum]:
        result: List[CamelColourEnum] = current_camel_stack + moving_camel_stack
        return result
