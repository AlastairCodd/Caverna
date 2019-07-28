from typing import List
from core.enums.caverna_enums import ResourceTypeEnum

class FarmAnimalResourceTypeDefault(object):

    def assign(self, input: List[ResourceTypeEnum]) -> List[ResourceTypeEnum]:
        if input is None: raise ValueError("input")
        input.clear()
        input.append( ResourceTypeEnum.sheep )
        input.append( ResourceTypeEnum.boar )
        input.append( ResourceTypeEnum.cow )
        input.append( ResourceTypeEnum.donkey )
        return input