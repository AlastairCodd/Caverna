from abc import ABCMeta
from unittest import TestCase

from buisness_logic.services.processor_services.expedition_reward_action_choice_processor_service import ExpeditionRewardActionChoiceProcessorService


# noinspection PyPep8Naming
class Given_An_ExpeditionRewardActionChoiceProcessorService(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: ExpeditionRewardActionChoiceProcessorService = ExpeditionRewardActionChoiceProcessorService()
        self.because()

    def because(self) -> None:
        pass
