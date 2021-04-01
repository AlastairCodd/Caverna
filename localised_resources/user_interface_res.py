from typing import Dict

from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum

resource_plural_name: Dict[ResourceTypeEnum, str] = {
    ResourceTypeEnum.stone: "stone",
    ResourceTypeEnum.wood: "wood",
    ResourceTypeEnum.ore: "ore",
    ResourceTypeEnum.ruby: "rubies",

    ResourceTypeEnum.coin: "coins",
    ResourceTypeEnum.food: "food",

    ResourceTypeEnum.grain: "grain",
    ResourceTypeEnum.veg: "veg",

    ResourceTypeEnum.sheep: "sheep",
    ResourceTypeEnum.donkey: "donkeys",
    ResourceTypeEnum.boar: "boar",
    ResourceTypeEnum.cow: "cows",
    ResourceTypeEnum.dog: "dogs"
}

action_combination_readable: Dict[ActionCombinationEnum, str] = {
    ActionCombinationEnum.Or: "or",
    ActionCombinationEnum.AndOr: "and/or",
    ActionCombinationEnum.AndThen: "and then",
    ActionCombinationEnum.EitherOr: "either/or",
    ActionCombinationEnum.AndThenOr: "and then/or"
}