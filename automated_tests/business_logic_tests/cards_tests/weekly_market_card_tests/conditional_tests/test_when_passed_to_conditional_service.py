from typing import List
from automated_tests.business_logic_tests.cards_tests.weekly_market_card_tests.test_weeklyMarketCard import \
    Given_A_WeeklyMarketCard
from common.services.conditional_service import ConditionalService
from core.baseClasses.base_action import BaseAction


# noinspection PyPep8Naming
class Test_When_Passed_To_Conditional_Service(Given_A_WeeklyMarketCard):
    def because(self):
        conditionalService: ConditionalService = ConditionalService()
        self.possible_choices = conditionalService.get_possible_choices(self.SUT._actions)

    def test_misc(self):
        print(len(self.possible_choices))
        print()

        possible_choice: List[BaseAction]
        for possible_choice in self.possible_choices:
            result: str = "["
            count: int = 0
            for action in possible_choice:
                result += str(action)
                count += 1
                if count != len(possible_choice):
                    result += ", "
            result += "]"
            print(result)
