from abc import ABCMeta
from unittest import TestCase


# noinspection PyPep8Naming
from common.formatters.resource_container_formatter import ResourceContainerFormatter


class Given_A_ResourceContainerFormatter(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: ResourceContainerFormatter = ResourceContainerFormatter()
        self.because()

    def because(self) -> None:
        pass
