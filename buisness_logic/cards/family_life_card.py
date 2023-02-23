from typing import List, Optional

from buisness_logic.actions.get_a_baby_dwarf_action import GetABabyDwarfAction
from buisness_logic.actions.sow_action import SowAction
from buisness_logic.cards.wish_for_children_card import WishForChildrenCard, UrgentWishForChildrenCard
from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.constants import card_ids
from core.enums.caverna_enums import ActionCombinationEnum
from core.exceptions.invalid_operation_error import InvalidOperationError


class FamilyLifeCard(BaseCard):
    def __init__(self):
        BaseCard.__init__(
            self, "Family Life", card_ids.FamilyLifeCardId, 3,
            Conditional(
                ActionCombinationEnum.AndOr,
                GetABabyDwarfAction(),
                SowAction()
            )
        )

    def reveal_card(
            self,
            cards: List[BaseCard]) -> None:
        if cards is None:
            raise ValueError("Cards cannot be None")
        BaseCard.reveal_card(self, cards)

        wish_for_children_card: Optional[WishForChildrenCard] = None
        urgent_wish_for_children_card: Optional[UrgentWishForChildrenCard] = None

        for card in cards:
            if isinstance(card, WishForChildrenCard):
                wish_for_children_card = card
            if isinstance(card, UrgentWishForChildrenCard):
                urgent_wish_for_children_card = card
            if wish_for_children_card is not None and urgent_wish_for_children_card is not None:
                break

        if wish_for_children_card is not None and urgent_wish_for_children_card is not None:
            wish_for_children_card.hide_card()
            urgent_wish_for_children_card.reveal_card(cards)
        else:
            raise InvalidOperationError("Wish for Children or Urgent Wish for Children missing")
