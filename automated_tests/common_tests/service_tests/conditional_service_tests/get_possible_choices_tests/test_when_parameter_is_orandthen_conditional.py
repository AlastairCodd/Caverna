from typing import List

from automated_tests.common_tests.service_tests.conditional_service_tests.test_conditionalService import Given_A_Conditional_Service
from buisness_logic.cards.fence_building_card import FenceBuildingLargeCard
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.multiconditional import Conditional
from common.entities.precedes_constraint import PrecedesConstraint
from core.baseClasses.base_action import BaseAction


class test_when_parameter_is_orandthen_conditional(Given_A_Conditional_Service):
    def because(self) -> None:
        card: FenceBuildingLargeCard = FenceBuildingLargeCard()

        conditional: Conditional = card.actions
        take_accumulated_action: BaseAction = card.actions.get_left_branch()
        place_pasture_action: BaseAction = card.actions.get_right_branch().get_left_branch()
        place_twin_pasture_action: BaseAction = card.actions.get_right_branch().get_right_branch()

        self.combinations: List[ActionChoiceLookup] = [
            ActionChoiceLookup([take_accumulated_action]),
            ActionChoiceLookup(
                [take_accumulated_action, place_pasture_action],
                [PrecedesConstraint(
                    take_accumulated_action,
                    place_pasture_action)]),
            ActionChoiceLookup(
                [take_accumulated_action, place_twin_pasture_action],
                [PrecedesConstraint(
                    take_accumulated_action,
                    place_twin_pasture_action)]),
            ActionChoiceLookup(
                [
                    take_accumulated_action,
                    place_pasture_action,
                    place_twin_pasture_action
                ],
                [
                    PrecedesConstraint(
                        take_accumulated_action,
                        place_pasture_action),
                    PrecedesConstraint(
                        take_accumulated_action,
                        place_twin_pasture_action)
                ]),
        ]

        self.result: List[ActionChoiceLookup] = self.SUT.get_possible_choices(conditional)

    def test_then_the_result_should_not_be_null(self):
        self.assertIsNotNone(self.result)

    def test_then_the_result_should_not_be_empty(self):
        self.assertGreater(len(self.result), 0)

    def test_then_the_result_should_contain_one_item(self):
        self.assertEqual(len(self.result), len(self.combinations))

    def test_then_the_result_should_contain_the_expected_combinations(self):
        for combination in self.combinations:
            with self.subTest(combination):
                self.assertContains(combination, self.result)

    def assertContains(self, expected, collection) -> None:
        if expected is None:
            raise ValueError
        if collection is None:
            raise ValueError

        for item in collection:
            actionsEqual: bool = expected.actions == item.actions
            constraintsEqual: bool = expected.constraints == item.constraints
            if actionsEqual and constraintsEqual:
                return

        raise AssertionError("Collection should contain element satisfying predicate, but does not.")
