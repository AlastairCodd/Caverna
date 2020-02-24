from enum import Enum, auto
from typing import Union, List, Dict, Tuple, Callable, Generator, NewType

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


CamelStack = NewType('CamelStack', List[CamelColourEnum])
CamelPositions = NewType('CamelPosition', Dict[int, CamelStack])
OrderedDice = NewType('OrderedDice', List[Tuple[CamelColourEnum, int]])
UnorderedDice = NewType('UnorderedDice', Dict[CamelColourEnum, int])


class CamelService(object):
    def __init__(
            self,
            camels_which_move_backwards: Union[List[CamelColourEnum], None] = None,
            number_of_dice_to_roll: int = 5,
            camel_dice: Union[Dict[CamelColourEnum, Dict[int, int]], None] = None):
        self._list_permutation_forge: ListPermutationForge = ListPermutationForge()
        if camels_which_move_backwards is None:
            camels_which_move_backwards = []

        self._total_path_length: int = 15
        self._camels_which_move_backwards: List[CamelColourEnum] = camels_which_move_backwards
        self._number_of_dice_to_roll: int = number_of_dice_to_roll

        self._camel_dice: Dict[CamelColourEnum, Dict[int, int]]
        if camel_dice is None:
            self._camel_dice = {}
            forward_dice: Dict[int, int] = {1: 1, 2: 1, 3: 1}
            backward_dice: Dict[int, int] = {-1: 1, -2: 1, -3: 1}

            for camel in CamelColourEnum:
                if camel in camels_which_move_backwards:
                    self._camel_dice[camel] = backward_dice
                else:
                    self._camel_dice[camel] = forward_dice
        else:
            self._camel_dice = camel_dice

    def get_possible_positions_for_camels(
            self,
            camel_positions: CamelPositions,
            oasis_positions: Union[Dict[int, OasisTypeEnum], None] = None) -> Dict[CamelPositions, List[OrderedDice]]:
        """Get all possible end states of camel positions after all dice have been rolled, and the rolls which put the camels in this state

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
    def _generate_dice_combinations(self) -> Generator[UnorderedDice, None, None]:
        number_of_combinations: int = reduce(lambda x, y: x * y, [len(x) for x in self._camel_dice.values()])
        for i in range(number_of_combinations):
            j: int = 0
            dice_combination: UnorderedDice = UnorderedDice({})
            q_product: int = 1
            for camel in self._camel_dice:
                current_camel_dice: Dict[int, int] = self._camel_dice[camel]
                q_current: int = sum(current_camel_dice.values())
                q_next: int = q_current * q_product
                chosen_dice_index: int = math.floor((i % q_next) / q_product)
                chosen_dice: int = list(current_camel_dice.keys())[chosen_dice_index]
                dice_combination[camel] = chosen_dice
                j += 1
                q_product = q_next
            yield dice_combination

    def _is_finished(self, camel_positions: Dict[int, List[CamelColourEnum]]) -> bool:
        is_finished: bool = False
        for position in camel_positions:
            if position > self._total_path_length:
                is_finished = True
                break
        return is_finished

    def _move_camel(
            self,
            camel: CamelColourEnum,
            steps: int,
            camel_positions: CamelPositions,
            oasis_positions: Union[Dict[int, OasisTypeEnum], None] = None) -> ResultLookup[CamelPositions]:
        result: ResultLookup[CamelPositions]

        if oasis_positions is None:
            oasis_positions = {}

        camel_position_result: ResultLookup[Tuple[int, List[CamelColourEnum]]] = self._find_camel_stack(camel, camel_positions)

        if not camel_position_result.flag:
            result = ResultLookup(errors=camel_position_result.errors)
        else:
            camel_position: int
            camel_stack: CamelStack
            camel_position, camel_stack = camel_position_result.value

            result_camel_position: int = camel_position + steps
            result_camel_positions: CamelPositions = CamelPositions({})
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
            camel_positions: Dict[int, List[CamelColourEnum]]) -> ResultLookup[Tuple[int, CamelStack]]:
        success: bool = False
        result_position: int = -1
        result_camel_stack: CamelStack = CamelStack([])

        for position in camel_positions:
            camels_at_position: List[CamelColourEnum] = camel_positions[position]
            if camel in camels_at_position:
                success = True
                result_position = position
                result_camel_stack = CamelStack(camels_at_position[:camels_at_position.index(camel) + 1])
                break

        result: ResultLookup[Tuple[int, CamelStack]]
        if success:
            result_value: Tuple[int, CamelStack] = (result_position, result_camel_stack)
            result = ResultLookup(success, result_value)
        else:
            result = ResultLookup(errors=f"camel {camel.name} not found at any position")

        return result

    def _place_camel_at_position_on_top(
            self,
            moving_camel_stack: CamelStack,
            current_camel_stack: CamelStack) -> CamelStack:
        result: CamelStack = CamelStack(moving_camel_stack + current_camel_stack)
        return result

    def _place_camel_at_position_on_bottom(
            self,
            moving_camel_stack: CamelStack,
            current_camel_stack: CamelStack) -> CamelStack:
        result: CamelStack = CamelStack(current_camel_stack + moving_camel_stack)
        return result
