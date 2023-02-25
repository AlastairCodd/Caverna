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
            print(f"[DBG] - dwarf {i}: is_adult={dwarf.is_adult}, is_active={dwarf.is_active}")
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
        print("[DBG] checking if game is finished")
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
            print(f"[DBG] Incrementing round index: roud_index={self._round_index}, harvest_type={self._harvest_type.name}")

        if not card.is_available:
            card.reveal_card(self._cards)

        self._cards.append(card)

        print(f"[DBG] Resetting Cards")

        for card in self._cards:
            if not card.has_been_revealled:
                if logging:
                    print(f"[VRB]   Card \"{card.name}\" hasn't been revealled, not resetting")
                continue
            if logging:
                print(f"[VRB]   Resetting card \"{card.name}\"")
            card.new_turn_reset()
            if isinstance(card, BaseResourceContainingCard):
                if logging:
                    print(f"[VRB]   > holds resources! refilling resources. currently:")
                    for (resource, amount) in card.resources.items():
                        print(f"[VRB]    > {resource.name}: {amount}")
                card.refill_action()
                if logging:
                    print(f"[VRB]   ! refilled. now:")
                    for (resource, amount) in card.resources.items():
                        print(f"[VRB]    > {resource.name}: {amount}")

        print(f"[DBG] Resetting players")

        for player in self._players:
            if logging:
                print(f"[VRB]   Resetting player \"{player.descriptor}\"")
            for (i, dwarf) in enumerate(player.dwarves):
                if logging:
                    print(f"[VRB]   > Resetting dwarf {i}")
                dwarf.clear_active_card()
                if dwarf.is_adult:
                    continue
                if logging:
                    print(f"[VRB]     > is a child! happy birthday {i}")
                dwarf.make_adult()

        self._players_in_order = self._players[self.starting_player_index_next_round:] \
            + self._players[:self.starting_player_index_next_round]

    def get_next_player(
            self,
            logging: bool = True) -> ResultLookup[BasePlayerService]:
        """Gets the next player to go this round, if applicable.
        :param logging: (Optional) Whether to perform any console logging. Defaults to true.
        :returns: A result lookup, containing the next player if any players still remain without dwarves.
            Flag will be false if this is not the case, true otherwise.
            This will never be null.
        """
        if logging:
            print(f"[DBG] getting next player. using dwarf number {self._turn_index + 1}")
        if self._next_player_index == len(self._players):
            self._turn_index += 1
            self._next_player_index = 0

        for i in range(len(self._players)):
            self._current_player = self._players_in_order[self._next_player_index]
            if logging:
                print(f"[DBG] > is it player {self._next_player_index + 1} ({self._current_player.descriptor}'s) turn?")
            self._next_player_index += 1

            does_current_player_have_any_available_dwarves: bool = any(dwarf for dwarf in self._current_player.dwarves if dwarf.is_adult and not dwarf.is_active)

            if does_current_player_have_any_available_dwarves:
                if logging:
                    print("[DBG]   < yes!")
                return ResultLookup(True, self._current_player)

            if logging:
                print(f"[DBG]   < no: has_dwarves={does_current_player_have_any_available_dwarves}")

            # how does this work with non-zero starting player? weird
            if self._next_player_index == len(self._players):
                if logging:
                    print("[VRB] exhausted all players, going to next turn")
                self._turn_index += 1
                self._next_player_index = 0

        if logging:
            print("[DBG] no remaining players in turn")
        return ResultLookup(errors="No remaining players in turn")
