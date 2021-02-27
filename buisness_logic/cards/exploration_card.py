from buisness_logic.actions.go_on_an_expedition_action import GoOnAnExpeditionAction
from core.baseClasses.base_card import BaseCard
from core.constants import card_ids


class ExplorationCard(BaseCard):
    def __init__(self):
        BaseCard.__init__(
            self, "Exploration", card_ids.ExplorationCardId, 3,
            GoOnAnExpeditionAction(4)
        )