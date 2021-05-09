from typing import Dict

from core.enums.caverna_enums import TileTypeEnum

open_close_tag_length: int = 5

resource_delta: str = "resource-delta"

tile_type_unavailable: str = "tile-type-unavailable"
tile_type_forest: str = "tile-type-forest"
tile_type_underground: str = "tile-type-underground"
tile_type_meadow: str = "tile-type-meadow"
tile_type_field: str = "tile-type-field"
tile_type_cavern: str = "tile-type-cavern"
tile_type_tunnel: str = "tile-type-tunnel"
tile_type_deepTunnel: str = "tile-type-deep-tunnel"
tile_type_pasture: str = "tile-type-pasture"
tile_type_furnishedCavern: str = "tile-type-furnished-cavern"
tile_type_furnishedDwelling: str = "tile-type-furnished-dwelling"
tile_type_oreMine: str = "tile-type-ore-mine"
tile_type_rubyMine: str = "tile-type-ruby-mine"

tile_type_tags: Dict[TileTypeEnum, str] = {
    TileTypeEnum.unavailable: tile_type_unavailable,
    TileTypeEnum.forest: tile_type_forest,
    TileTypeEnum.underground: tile_type_underground,
    TileTypeEnum.meadow: tile_type_meadow,
    TileTypeEnum.field: tile_type_field,
    TileTypeEnum.cavern: tile_type_cavern,
    TileTypeEnum.tunnel: tile_type_tunnel,
    TileTypeEnum.deepTunnel: tile_type_deepTunnel,
    TileTypeEnum.pasture: tile_type_pasture,
    TileTypeEnum.furnishedCavern: tile_type_furnishedCavern,
    TileTypeEnum.furnishedDwelling: tile_type_furnishedDwelling,
    TileTypeEnum.oreMine: tile_type_oreMine,
    TileTypeEnum.rubyMine: tile_type_rubyMine,
}