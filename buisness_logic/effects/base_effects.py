from abc import ABCMeta, abstractmethod

from core.baseClasses.base_effect import BaseEffect
from core.repositories.base_player_repository import BasePlayerRepository


class BaseOnPurchaseEffect(BaseEffect, metaclass=ABCMeta):
    @abstractmethod
    def invoke(
            self,
            player: BasePlayerRepository) -> bool:
        raise NotImplementedError("base resource effect class")
