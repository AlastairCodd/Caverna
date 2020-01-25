from enum import Enum, auto


class HarvestTypeEnum(Enum):
    NoHarvest = auto()
    Harvest = auto()
    OneFoodPerDwarf = auto()
    EitherFieldPhaseOrBreedingPhase = auto()
