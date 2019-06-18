from typing import Tuple, Dict
from gym import Env
from numpy import array

class CavernaEnv(Env):
    
    def reset(self) -> array:
        raise NotImplementedError()
        
    def step(self, action: array) -> Tuple[array, float, bool, Dict]:
        if action is None:
            raise ValueError("action")
            
        