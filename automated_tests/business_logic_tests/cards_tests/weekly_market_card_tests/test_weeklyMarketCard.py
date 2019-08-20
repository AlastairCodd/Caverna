from abc import ABC, abstractmethod
from unittest import TestCase
from buisness_logic.cards.weekly_market_card import WeeklyMarketCard


# noinspection PyPep8Naming
class Given_A_WeeklyMarketCard(ABC, TestCase):
    def setUp(self) -> None:
        self.SUT: WeeklyMarketCard = WeeklyMarketCard()
        self.because()

    @abstractmethod
    def because(self):
        pass
