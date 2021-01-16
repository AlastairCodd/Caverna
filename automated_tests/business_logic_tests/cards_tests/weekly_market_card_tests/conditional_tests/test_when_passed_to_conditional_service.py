import unittest
from typing import List
from automated_tests.business_logic_tests.cards_tests.weekly_market_card_tests.test_weeklyMarketCard import \
    Given_A_WeeklyMarketCard
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.services.conditional_service import ConditionalService


# noinspection PyPep8Naming
class Test_When_Passed_To_Conditional_Service(Given_A_WeeklyMarketCard):
    def because(self):
        conditionalService: ConditionalService = ConditionalService()
        self.possible_choices: List[ActionChoiceLookup] = conditionalService.get_possible_choices(self.SUT._actions)

    @unittest.skip
    def test_misc(self):
        # TODO: Make this test assert things
        print(len(self.possible_choices))
        print()

        possible_choice: ActionChoiceLookup
        for possible_choice in self.possible_choices:
            result: str = "["
            count: int = 0
            for action in possible_choice.actions:
                result += str(action)
                count += 1
                if count != len(possible_choice.actions):
                    result += ", "
            result += "]"
            print(result)
