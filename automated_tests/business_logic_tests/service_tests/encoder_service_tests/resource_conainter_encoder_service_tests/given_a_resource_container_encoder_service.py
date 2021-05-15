from abc import ABCMeta
from unittest import TestCase


# noinspection PyPep8Naming
class Given_A_ResourceContainerEncoderService(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: ResourceContainerEncoderService = ResourceContainerEncoderService()
        self.because()

    def because(self) -> None:
        pass
