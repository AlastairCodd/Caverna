from typing import Dict

from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum

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

tile_name_short: Dict[TileTypeEnum, str] = {
    TileTypeEnum.unavailable: "na",
    TileTypeEnum.forest: "fo",
    TileTypeEnum.underground: "ug",
    TileTypeEnum.meadow: "m",
    TileTypeEnum.field: "fi",
    TileTypeEnum.cavern: "c",
    TileTypeEnum.tunnel: "t",
    TileTypeEnum.deepTunnel: "dt",
    TileTypeEnum.pasture: "p",
    TileTypeEnum.oreMine: "or",
    TileTypeEnum.rubyMine: "ru",
}

tile_name_long: Dict[TileTypeEnum, str] = {
    TileTypeEnum.unavailable: "N/A",
    TileTypeEnum.forest: "Forest",
    TileTypeEnum.underground: "Underground",
    TileTypeEnum.meadow: "Meadow",
    TileTypeEnum.field: "Field",
    TileTypeEnum.cavern: "Cavern",
    TileTypeEnum.tunnel: "Tunnel",
    TileTypeEnum.deepTunnel: "Deep Tunnel",
    TileTypeEnum.pasture: "Pasture",
    TileTypeEnum.oreMine: "Ore Mine",
    TileTypeEnum.rubyMine: "Ruby Mine",
}