from abc import ABC
from typing import Union
from unittest import TestCase

from buisness_logic.services.complete_dwarf_player_choice_transfer_service import CompleteDwarfPlayerChoiceTransferService
from common.entities.dwarf import Dwarf
from common.entities.multiconditional import Conditional
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from common.entities.weapon import Weapon
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard

# noinspection PyPep8Naming
from core.enums.harvest_type_enum import HarvestTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository


class Given_A_CompleteDwarfPlayerChoiceTransferService(TestCase, ABC):
    def setUp(self) -> None:
        self.SUT: CompleteDwarfPlayerChoiceTransferService = CompleteDwarfPlayerChoiceTransferService()
        self._turn_descriptor: TurnDescriptorLookup = TurnDescriptorLookup([], [], 0, 0, HarvestTypeEnum.Harvest)

        self.because()

    def because(self) -> None:
        pass

    def _initialise_dwarf(
            self,
            dwarf_weapon_level: int = 0,
            is_adult: bool = True,
            is_active: bool = False,
            active_card: Union[BaseCard, None] = None):
        dwarf: Dwarf = Dwarf()
        if is_adult:
            dwarf.make_adult()

        if dwarf_weapon_level > 0:
            dwarf.give_weapon(Weapon(level=dwarf_weapon_level))

        if is_active:
            if active_card is None:
                active_card = FakeCard()
            dwarf.set_active(active_card)

        return dwarf


class FakeCard(BaseCard):
    def __init__(
            self,
            name: str = "fake card",
            card_id: int = -1,
            actions: Union[BaseAction, Conditional, None] = None):
        if actions is None:
            actions = NullAction()
        super().__init__(name, card_id, actions=actions)


class NullAction(BaseAction):
    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        return ResultLookup(True, 1)

    def new_turn_reset(self):
        pass
