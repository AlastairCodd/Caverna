from typing import Optional, List

from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_resource_containing_card import BaseResourceContainingCard
from core.constants import game_constants
from core.enums.harvest_type_enum import HarvestTypeEnum
from core.services.base_player_service import BasePlayerService


class CavernaStateService(object):
    def __init__(
            self,
            players: List[BasePlayerService],
            cards: List[BaseCard],
            starting_player_index: int = 0) -> None:
        self._cards: List[BaseCard] = list(cards)
        self._players: List[BasePlayerService] = list(players)

        self._past_harvest_types: List[HarvestTypeEnum] = []

        self._round_index: int = -1
        self._turn_index = 0
        self._harvest_type: HarvestTypeEnum = HarvestTypeEnum.NoHarvest

        self._starting_player_index_this_round: int = starting_player_index
        self.starting_player_index_next_round: int = starting_player_index
        self._current_player: Optional[BasePlayerService] = None

        self._players_in_order: List[BasePlayerService] = []
        self._next_player_index: int = 0

    @property
    def current_player(self) -> Optional[BasePlayerService]:
        return self._current_player

    @property
    def is_current_players_final_turn(self) -> bool:
        if self._current_player is None:
            return False
        number_of_available_dwarves: int = 0
        for (i, dwarf) in enumerate(self._current_player.dwarves):
            print(f" > dwarf {i}: is_adult={dwarf.is_adult}, is_active={dwarf.is_active}")
            if not dwarf.is_adult:
                continue
            if dwarf.is_active:
                continue
            number_of_available_dwarves += 1
        result = number_of_available_dwarves == 1
        return result

    @property
    def cards(self) -> List[BaseCard]:
        result: List[BaseCard] = []
        result.extend(self._cards)
        return result

    @property
    def is_game_finished(self) -> bool:
        result: bool = self.is_current_players_final_turn and self._round_index == game_constants.number_of_rounds - 1
        return result

    @property
    def round_index(self) -> int:
        return self._round_index

    @property
    def turn_index(self) -> int:
        return self._turn_index

    @property
    def round_harvest_type(self) -> HarvestTypeEnum:
        return self._harvest_type

    @property
    def starting_player_index_this_round(self) -> int:
        return self._starting_player_index_this_round

    def increment_round_index(
            self,
            card: BaseCard,
            harvest_type: HarvestTypeEnum,
            logging: bool = True) -> None:
        """Increments the round index.
        :param card: The new card to reveal for this round
        :param harvest_type: The harvest type for this round.
        :param logging: (Optional) Whether to perform any console logging. Defaults to true.
        :returns: A boolean indicating if the round was incremented successfully.
        """
        if card is None:
            raise ValueError("Card cannot be None")
        if self._round_index == game_constants.number_of_rounds:
            raise IndexError(f"Round index must be less than {game_constants.number_of_rounds}")

        self._round_index += 1
        self._turn_index = 0
        self._next_player_index = 0

        self._starting_player_index_this_round = self.starting_player_index_next_round

        self._harvest_type = harvest_type
        self._past_harvest_types.append(harvest_type)

        if logging:
            print(f"[DBG] Round {self._round_index}, Harvest Type: {self._harvest_type.name}")

        if not card.is_available:
            card.reveal_card(self._cards)

        self._cards.append(card)

        for card in self._cards:
            card.new_turn_reset()
            if isinstance(card, BaseResourceContainingCard):
                card.refill_action()

        for player in self._players:
            for dwarf in player.dwarves:
                dwarf.clear_active_card()
                if not dwarf.is_adult:
                    dwarf.make_adult()

        self._players_in_order = self._players[self.starting_player_index_next_round:] \
            + self._players[:self.starting_player_index_next_round]

    def get_next_player(self) -> ResultLookup[BasePlayerService]:
        """Gets the next player, if applicable.

        :returns: A result lookup, containing the next player if any players still remain without dwarves.
            Flag will be false if this is not the case, true otherwise.
            This will never be null.
        """
        if self._next_player_index == len(self._players):
            self._turn_index += 1
            self._next_player_index = 0

        was_player_found: bool = False
        for i in range(len(self._players)):
            self._current_player = self._players_in_order[self._next_player_index]
            self._next_player_index += 1

            is_current_players_final_turn: bool = self.is_current_players_final_turn
            does_current_player_have_any_available_dwarves: bool = any(dwarf for dwarf in self._current_player.dwarves if dwarf.is_adult and not dwarf.is_active)

            if not is_current_players_final_turn and does_current_player_have_any_available_dwarves:
                was_player_found = True
                break
            elif self._next_player_index == len(self._players):
                self._turn_index += 1
                self._next_player_index = 0

        result: ResultLookup[BasePlayerService] = ResultLookup(True, self._current_player) \
            if was_player_found \
            else ResultLookup(errors="No remaining players in turn")

        return result
