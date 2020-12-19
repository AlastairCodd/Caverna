from buisness_logic.actions.go_on_an_expedition_action import GoOnAnExpeditionAction
from core.baseClasses.base_card import BaseCard


class ExplorationCard(BaseCard):
    def __init__(self):
        BaseCard.__init__(
            self, "Exploration", 28, 3,
            GoOnAnExpeditionAction(4)
        )