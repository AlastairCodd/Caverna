from typing import List

from common.forges.base_card_forge import BaseLevelledCardForge
from common.forges.card_forge_level_1 import Level1CardForge
from common.forges.card_forge_level_2 import Level2CardForge
from common.forges.card_forge_level_3 import Level3CardForge
from common.forges.card_forge_level_4 import Level4CardForge
from core.baseClasses.base_card import BaseCard


class LevelledCardService(object):
    def __init__(self):
        cards_level_1: BaseLevelledCardForge = Level1CardForge()
        cards_level_2: BaseLevelledCardForge = Level2CardForge()
        cards_level_3: BaseLevelledCardForge = Level3CardForge()
        cards_level_4: BaseLevelledCardForge = Level4CardForge()

        self._forges: List[BaseLevelledCardForge] = [
            cards_level_1,
            cards_level_2,
            cards_level_3,
            cards_level_4,
        ]

    def get_cards(self) -> List[BaseCard]:
        cards: List[BaseCard] = []
        additional_cards: List[BaseCard] = []

        for forge in self._forges:
            cards.extend(forge.get_sequential_cards())
            additional_cards.extend(forge.get_additional_cards())

        cards.extend(additional_cards)

        return cards

    def get_next_card_to_reveal(
            self,
            round_index: int,
            cards: List[BaseCard]) -> BaseCard:
        return cards[round_index]
