from common.entities.weapon import Weapon

class Dwarf(object):
    def __init__(self, isAdult: bool = False):
        self._isAdult = isAdult
        self._weapon = None
        self._currentCard = None
    
    def is_adult(self) -> bool:
        return self._isAdult
            
    def set_is_Adult(self, isAdult: bool) -> bool:
        self._isAdult = isAdult
        return self._isAdult
    
    def give_weapon(self, weapon: Weapon):
        if self._weapon is not None:
            raise ValueError("dwarf already has a weapon")
        
        self._weapon = weapon
        
    def get_weapon(self) -> Weapon:
        return self._weapon

    def has_weapon(self) -> bool:
        result = self._weapon is None
        return result
    
    def set_active(self, currentCard):
        if currentCard is None:
            raise ValueError("current card must not be none")
    
        if self._currentCard is not None:
            raise ValueError("already active")
        
        self._currentCard = currentCard
        
    def clear_active_card(self):
        self._currentCard = None
        
    def is_active(self) -> bool:
        isActive = self._currentCard is None
        return isActive