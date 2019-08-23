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
    def __init__(self, input, condition, trigger_state:  TriggerStateEnum = TriggerStateEnum.StartOfTurn):
        """Recieve some input when some condition is true."""
        self._input = input
        self._condition = condition
        super().__init__(trigger_state)
        
    def invoke(self, player):
        numberOfTimesConditionMet = self._condition(player)
        if numberOfTimesConditionMet == 0:
            return False
        resources = {key: self._input[key] * numberOfTimesConditionMet for key in self._input}
        player.give_resources( resources )
        return True
        
class ReceiveProportional(BaseResourceEffect):
    def __init__(self, input, proportionalTo, trigger_state:  TriggerStateEnum = TriggerStateEnum.StartOfTurn):
        """Recieve some x input per x "proportionalTo"."""
        self._input = input
        self._proportionalTo = proportionalTo
        super().__init__(trigger_state)
        
    def invoke(self, player):
        playerResources = player.resources
        numberOfProportionalResources = count_dictionary_contains(playerResources, self._proportionalTo)
        for _ in range(numberOfProportionalResources):
            player.give_resources( self._input )
            
def does_dictionary_contain(inDict, containedDict):
    isContained = True
    for key in containedDict:
        isContained &= inDict.get(key, 0) >= containedDict[key]
    return isContained
    
def count_dictionary_contains(inDict, containedDict):
    count = 0
    while True:
        if not does_dictionary_contain(inDict, containedDict):
            return count
        count += 1
        for key in containedDict:
            inDict[key] -= containedDict[key]