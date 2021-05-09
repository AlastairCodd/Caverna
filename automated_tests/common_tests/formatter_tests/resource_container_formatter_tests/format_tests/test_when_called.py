from typing import Dict, List

from automated_tests.common_tests.formatter_tests.given_a_resource_container_formatter import Given_A_ResourceContainerFormatter
from core.constants import html_tags
from core.containers.resource_container import ResourceContainer
from core.enums.caverna_enums import ResourceTypeEnum


class test_when_called(Given_A_ResourceContainerFormatter):
    def because(self) -> None:
        self.maxDiff = None

        resource_container: ResourceContainer = ResourceContainer()
        resources: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.stone: 4,
            ResourceTypeEnum.wood: 0,
            ResourceTypeEnum.ore: 6,
            ResourceTypeEnum.ruby: 0,
            ResourceTypeEnum.coin: 10,
            ResourceTypeEnum.food: 1,
            ResourceTypeEnum.grain: 7,
            ResourceTypeEnum.veg: 10,
            ResourceTypeEnum.sheep: 3,
            ResourceTypeEnum.donkey: 3,
            ResourceTypeEnum.cow: 1,
            ResourceTypeEnum.boar: 7,
            ResourceTypeEnum.dog: 11,
        }
        resource_container.give_resources(resources)

        resource_delta: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.stone: 0,
            ResourceTypeEnum.wood: -3,
            ResourceTypeEnum.ore: 0,
            ResourceTypeEnum.ruby: 0,
            ResourceTypeEnum.coin: 0,
            ResourceTypeEnum.food: 0,
            ResourceTypeEnum.grain: 0,
            ResourceTypeEnum.veg: -2,
            ResourceTypeEnum.sheep: 0,
            ResourceTypeEnum.donkey: 1,
            ResourceTypeEnum.cow: -2,
            ResourceTypeEnum.boar: -1,
            ResourceTypeEnum.dog: -1,
        }

        self._result: str = self.SUT.format(resource_container, resource_delta)

        expected_lines: List[str] = [
            f"stone:   4          food:    1          cow:     1  <{html_tags.resource_delta}>(-2)</{html_tags.resource_delta}>",
            f"wood:    0  <{html_tags.resource_delta}>(-3)</{html_tags.resource_delta}>    grain:   7          boar:    7  <{html_tags.resource_delta}>(-1)</{html_tags.resource_delta}>",
            f"ore:     6          veg:    10  <{html_tags.resource_delta}>(-2)</{html_tags.resource_delta}>    dog:    11  <{html_tags.resource_delta}>(-1)</{html_tags.resource_delta}>",
            f"ruby:    0          sheep:   3",
            f"coin:   10          donkey:  3  <{html_tags.resource_delta}>(+1)</{html_tags.resource_delta}>",
        ]

        self._expected_result: str = "\n".join(expected_lines)

    def test_then_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_should_be_expected(self) -> None:
        self.assertEqual(self._expected_result, self._result)
