from typing import List

from buisness_logic.cards.imitation_card import ImitationCard
from common.entities.result_lookup import ResultLookup
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
            if not card.is_active:
                continue
            if self.is_card_used_by_player(card, player):
                continue
            if isinstance(card, ImitationCard):
                continue
            cards_which_are_used_by_someone_else.append(card)

        return cards_which_are_used_by_someone_else

    def is_card_used_by_player(
            self,
            card: BaseCard,
            player: BasePlayerRepository) -> bool:

        if card.is_active:
            return False

        for dwarf in player.dwarves:
            if not dwarf.is_active:
                continue
            if dwarf.current_card_id == card.id:
                return True

        return result

    def get_imitation_card(
            self,
            unused_available_cards: List[BaseCard]) -> ResultLookup[ImitationCard]:
        if unused_available_cards is None:
            raise ValueError("Unused Available Cards cannot be None")
        imitation_cards_available: List[ImitationCard] = [card for card in unused_available_cards if isinstance(card, ImitationCard)]

        if not any(imitation_cards_available):
            return ResultLookup(errors="No imitation cards are available")

        imitation_card: ImitationCard = sorted(imitation_cards_available, key=lambda card: card.amount_of_food)[0]
        result = ResultLookup(True, imitation_card)
        return result

    def can_use_card_already_in_use(
            self,
            unused_available_cards: List[BaseCard],
            used_available_cards: List[BaseCard]) -> ResultLookup[bool]:
        if unused_available_cards is None:
            raise ValueError("Unused Available Cards cannot be None")
        if used_available_cards is None:
            raise ValueError("Used Available Cards cannot be None")
        success: bool = True
        errors: List[str] = []

        any_imitation_cards: ResultLookup[ImitationCard] = self.get_imitation_card(unused_available_cards)

        success &= any_imitation_cards.flag
        errors.extend(any_imitation_cards.errors)

        any_cards_to_use_again: bool = len(used_available_cards) > 0

        if not any_cards_to_use_again:
            success = False
            errors.append("No cards have been used")

        result: ResultLookup[bool] = ResultLookup(success, success, errors)
        return result
