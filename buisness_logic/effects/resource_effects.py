from common.entities.player import Player
from core.baseClasses.base_effect import BaseEffect
from core.enums.caverna_enums import TriggerStateEnum

class BaseResourceEffect(BaseEffect):
    def invoke(self, player: Player) -> bool:
        raise NotImplementedException("base resource effect class")
    
class Receive(BaseResourceEffect):
    def __init__(self, output):
        self._output = output
    
class ReceiveConditional(BaseResourceEffect):
    def __init__(self, increaseBy: int, triggerState: TriggerStateEnum = TriggerStateEnum.StartOfTurn):
        self._increaseBy = increaseBy
        self._triggerState = triggerState

    def invoke(self, player: Player) -> bool:
        raise NotImplementedException()

class ReceiveConditional(BaseResourceEffect):
    def __init__(self, input, condition, triggerState:  TriggerStateEnum = TriggerStateEnum.StartOfTurn):
        """Recieve some input when some condition is true."""
        self._input = input
        self._condition = condition
        super().__init__(self, triggerState