from abc import ABCMeta
from unittest import TestCase

# noinspection PyPep8Naming
from buisness_logic.actions.go_on_an_expedition_action import GoOnAnExpeditionAction


class Given_A_GoOnAnExpeditionAction(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self._level: int = 3
        self.SUT: GoOnAnExpeditionAction = GoOnAnExpeditionAction(self._level)

        self.because()

    def because(self) -> None:
        pass
