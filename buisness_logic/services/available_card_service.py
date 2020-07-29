from typing import List

from core.repositories.base_player_repository import BasePlayerRepository
from core.baseClasses.base_card import BaseCard


class AvailableCardService(object):
    def get_cards_which_are_free_to_use(
            self,
            cards: List[BaseCard]) -> List[BaseCard]:
        return [card for card in cards if card.is_available]

    def get_cards_which_are_used_by_someone_else(
            self,
            cards: List[BaseCard],
            player: BasePlayerRepository) -> List[BaseCard]:
        cards_which_are_used_by_someone_else: List[BaseCard] = []
        for card in cards:
            if card.is_active and not self.is_card_used_by_player(card, player):
                cards_which_are_used_by_someone_else.append(card)

        return cards_which_are_used_by_someone_else

    def is_card_used_by_player(
            self,
            card: BaseCard,
            player: BasePlayerRepository) -> bool:
        result: bool

        if card.is_active:
            result = False
        else:
            result: bool = False
            for dwarf in player.dwarves:
                if dwarf.is_active:
                    result = dwarf.current_card_id == card.id
                    if result:
                        break

        return result
