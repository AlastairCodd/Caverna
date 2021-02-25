from typing import List

from common.forges.base_card_forge import BaseCardForge
from common.forges.card_forge_1_3 import OneToThreeCardForge
from common.forges.card_forge_3 import ThreeCardForge
from common.forges.card_forge_4_7 import FourToSevenCardForge
from common.forges.card_forge_5 import FiveCardForge
from common.forges.card_forge_6_7 import SixToSevenCardForge
from common.forges.card_forge_7 import SevenCardForge
from core.baseClasses.base_card import BaseCard


class CardDefault(object):
    def __init__(
            self,
            number_of_players: int) -> None:
        if number_of_players < 1:
            raise IndexError(f"Must have at least one player (number_of_players={number_of_players})")
        if number_of_players > 7:
            raise IndexError(f"The maximum number of players is 7 (number_of_players={number_of_players})")

        self._number_of_players: int = number_of_players

        cards_1_3: BaseCardForge = OneToThreeCardForge()
        cards_4_7: BaseCardForge = FourToSevenCardForge()
        cards_6_7: BaseCardForge = SixToSevenCardForge()

        cards_3: BaseCardForge = ThreeCardForge()
        cards_5: BaseCardForge = FiveCardForge()
        cards_7: BaseCardForge = SevenCardForge()

        self._forges: List[BaseCardForge] = [
            cards_1_3,
            cards_4_7,
            cards_6_7,

            cards_3,
            cards_5,
            cards_7,
        ]

    def get_cards(self) -> List[BaseCard]:
        cards: List[BaseCard] = []

        for forge in self._forges:
            if forge.is_valid_for_number_of_players(self._number_of_players):
                cards.extend(forge.get_cards())

        return cards
