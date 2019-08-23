from abc import abstractmethod, ABC

from core.containers.resource_container import ResourceContainer


class BaseAction(ABC):

    @abstractmethod
    def invoke(self, player: 'Player', active_card: ResourceContainer) -> bool:
        raise NotImplementedError("abstract base action class")

    @abstractmethod
    def new_turn_reset(self):
        pass