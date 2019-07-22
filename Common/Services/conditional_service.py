from typing import List
from core.base_classes.baseAction import BaseAction
from core.enums.caverna_enums import ActionCombinationEnum
from common.entities.multiconditional import Conditional

class ConditionalService(object):
    
    def __init__(self):
        """Ctor. Sets up action dictionary for conditional"""
        self._actionDictionary = {
            ActionCombinationEnum.EitherOr: self._combine_either_or
            ActionCombinationEnum.AndOr: self._combine_and_or
            ActionCombinationEnum.AndThenOr: self._combine_and_then_or
            ActionCombinationEnum.Or: self._combine_or
            ActionCombinationEnum.AndThen: self._combine_and_then
    
    def get_possible_choices(self, conditional) -> List[BaseAction]:
        """recurse through the conditional tree in order to find which possible action choices the agent may make
        
        params: 
            conditional. Either a conditional object or an action. This cannot be null
        
        returns: 
            a list containing all possible (base) actions which can be take. This will never be null."""
        if conditional is None: raise ValueError("conditional")
        if isinstance(conditional, BaseAction):
            return list(conditional)
        if not isinstance(conditional, Conditional):
            raise ValueError("input must be either multiconditional.Conditional or baseAction.BaseAction")
            
        left = get_possible_choices(conditional.get_left_branch())
        right = get_possible_choices(conditional.get_right_branch())
        choices = self._actionDictionary(conditional.get_combination_type())(left, right)
        
    def _combine_and_or(self, left: Iterable[BaseAction], right: Iterable[BaseAction]) -> List[BaseAction]:
        """Combine the left and right lists in an and way. (left or right or left and right)
        
        params:
            left: an enumerable of base actions. This cannot be null.
            right: an enumerable of base actions. This cannot be null.
        
        returns:
            a list containing the possible combined actions. This will never be null."""
        if left is None: raise ValueError("left")
        if right is None: raise ValueError("right")
        
        result = []
        
        for l in left:
            for r in right: 
                combination = [l, r]
                result.append(combination)
        
        return result
     
    def _combine_either_or(self, left: Iterable[BaseAction], right: Iterable[BaseAction]) -> List[BaseAction]:
        """Combine the left and right lists in an either or way. (left or right)
        
        params:
            left: an enumerable of base actions. This cannot be null.
            right: an enumerable of base actions. This cannot be null.
        
        returns:
            a list containing the possible combined actions. This will never be null."""
        if left is None: raise ValueError("left")
        if right is None: raise ValueError("right")
        
        result = []
        
        for l in left:
            result.append(l)
        
        for r in right:
            result.append(r)
        
        return result
        
    def _combine_and_then(self, left: Iterable[BaseAction], right: Iterable[BaseAction]) -> List[BaseAction]:
        """Combine the left and right lists in an and then way. (left or right)
        
        params:
            left: an enumerable of base actions. This cannot be null.
            right: an enumerable of base actions. This cannot be null.
        
        returns:
            a list containing the possible combined actions. This will never be null."""
        if left is None: raise ValueError("left")
        if right is None: raise ValueError("right")
        
        result = []
        
        for l in left:
            result.append(l)
        
        for r in right:
            result.append(r)
        
        return result
        