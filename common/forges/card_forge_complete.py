from typing import Dict, List, Type

from common.forges import *
from common.forges.base_card_forge import BaseCardForge, BaseLevelledCardForge
from core.baseClasses.base_card import BaseCard


class CompleteCardForge(object):
    def get_cards(self) -> Dict[int, BaseCard]:
        forges: List[BaseCardForge] = [
            card_forge_1_3.OneToThreeCardForge(),
            card_forge_1_7.OneToSevenCardForge(),
            card_forge_3.ThreeCardForge(),
            card_forge_4_7.FourToSevenCardForge(),
            card_forge_5.FiveCardForge(),
            card_forge_6_7.SixToSevenCardForge(),
            card_forge_7.SevenCardForge(),
        ]
        levelled_forges: List[BaseLevelledCardForge] = [
            card_forge_level_1.Level1CardForge(),
            card_forge_level_2.Level2CardForge(),
            card_forge_level_3.Level3CardForge(),
            card_forge_level_4.Level4CardForge(),
        ]

        cards: Dict[int, BaseCard] = {}

        for forge in forges:
            sequential_cards: List[BaseCard] = forge.get_cards()
            for card in sequential_cards:
                if card.id not in cards:
                    cards[card.id] = card
                # else:
                #     raise IndexError(f"Duplicate cards with id {card.id}: \"{cards[card.id].name}\" and \"{card.name}\"")

        for forge in levelled_forges:
            sequential_cards: List[BaseCard] = forge.get_sequential_cards()
            for card in sequential_cards:
                if card.id not in cards:
                    cards[card.id] = card
                # else:
                #     raise IndexError(f"Duplicate cards with id {card.id}: \"{cards[card.id].name}\" and \"{card.name}\"")

            sequential_cards: List[BaseCard] = forge.get_additional_cards()
            for card in sequential_cards:
                if card.id not in cards:
                    cards[card.id] = card
                # else:
                #     raise IndexError(f"Duplicate cards with id {card.id}: \"{cards[card.id].name}\" and \"{card.name}\"")

        return cards
