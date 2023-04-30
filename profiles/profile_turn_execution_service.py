from buisness_logic.cards.weekly_market_card import WeeklyMarketCard
from buisness_logic.services.turn_execution_service import TurnExecutionService
from common.entities.resources_to_sow_lookup import ResourcesToSow
from common.entities.result_lookup import ResultLookup
from common.entities.tile_twin_placement_lookup import TileTwinPlacementLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.enums.caverna_enums import TileDirectionEnum, ResourceTypeEnum
from core.enums.harvest_type_enum import HarvestTypeEnum
from core.services.base_player_service import BasePlayerService


def main_exhaustive():
    from common.services.exhaustive_action_ordering_service import ExhaustiveActionOrderingService
    main(ExhaustiveActionOrderingService())

def main_pruning():
    from common.services.pruning_action_ordering_service import PruningActionOrderingService
    main(PruningActionOrderingService())

def main_bulk():
    from common.services.bulk_action_ordering_service import BulkActionOrderingService
    main(BulkActionOrderingService())

def main(ordering_service = None):
    turn_execution_service = TurnExecutionService(ordering_service)

    card = WeeklyMarketCard()
    player = DeterministicPlayer(card)

    turn_descriptor = TurnDescriptorLookup(
        [card],
        [],
        1,
        3,
        HarvestTypeEnum.Harvest)

    turn_result = turn_execution_service.take_turn(
        player,
        True,
        turn_descriptor)

class DeterministicPlayer(BasePlayerService):
    from core.baseClasses.base_card import BaseCard

    def __init__(self, card: BaseCard):
        from common.defaults.tile_container_default import TileContainerDefault
        BasePlayerService.__init__(self, 0, "Test", 0, TileContainerDefault())

        self._card = card
        self.give_resources({
            ResourceTypeEnum.food: 2,
            ResourceTypeEnum.coin: 3,
            ResourceTypeEnum.grain: 2
        })

        self._place_tiles()

    def get_player_choice_card_to_use(self, _cards, _turn_descriptor):
        return ResultLookup(True, self._card)

    def get_player_choice_actions_to_use(self, choices, _turn_descriptor):
        print(repr(choices[0]))
        return ResultLookup(True, choices[0])

    def get_player_choice_resources_to_sow(self, _turn_descriptor):
        return ResultLookup(True, ResourcesToSow(2, 0))

    def get_player_choice_conversions_to_perform(self, turn_descriptor):
        return [
            ([ResourceTypeEnum.coin], 2, [ResourceTypeEnum.food]),
            ([ResourceTypeEnum.sheep], 1, [ResourceTypeEnum.food]),
        ]

    def get_player_choice_market_items_to_purchase(self, _items_to_purchase, turn_descriptor):
        return ResultLookup(True, [ResourceTypeEnum.sheep, ResourceTypeEnum.donkey])

    def get_player_choice_weapon_level(self, turn_descriptor):
        raise NotImplementedError()

    def get_player_choice_animals_to_breed(self, animals_which_can_reproduce, possible_number_of_animals_to_reproduce, turn_descriptor):
        return ResultLookup(True, [])

    def get_player_choice_use_dwarf_out_of_order(self, dwarves, turn_descriptor):
        raise NotImplementedError()

    def get_player_choice_use_card_already_in_use(
            self,
            unused_available_cards,
            used_available_cards,
            amount_of_food_required,
            turn_descriptor):
        raise NotImplementedError()

    def get_player_choice_dwarf_to_use_out_of_order(self, dwarves, turn_descriptor):
        raise NotImplementedError()

    def get_player_choice_fences_to_build(
            self,
            place_pasture_action,
            place_twin_pasture_action,
            place_stable_action,
            turn_descriptor):
        raise NotImplementedError()

    def get_player_choice_tile_to_build(
            self,
            possible_tiles,
            turn_descriptor):
        raise NotImplementedError()

    def get_player_choice_expedition_reward(
            self,
            possible_expedition_rewards,
            expedition_level,
            is_first_expedition_action,
            turn_descriptor):
        raise NotImplementedError()

    def get_player_choice_location_to_build(self, tile, turn_descriptor):
        raise NotImplementedError()

    def get_player_choice_location_to_build_twin(self, tile_type, turn_descriptor):
        raise NotImplementedError()

    def get_player_choice_location_to_build_stable(self, turn_descriptor):
        raise NotImplementedError()

    def get_player_choice_effects_to_use_for_cost_discount(self, tile_cost, possible_effects, turn_descriptor):
        raise NotImplementedError()

    def get_player_choice_use_harvest_action_instead_of_breeding(self, turn_descriptor):
        raise NotImplementedError()

    def get_player_choice_effect_to_use_for_feeding_dwarves(self,turn_descriptor):
        return ResultLookup(True, [])

    def _place_tiles(self):
        from buisness_logic.tiles.mine_tiles import CavernTile, TunnelTile
        from buisness_logic.tiles.outdoor_tiles import MeadowTile, FieldTile
        from common.services.tile_service import TileService
        from core.enums.caverna_enums import TileTypeEnum

        tile_service = TileService()
        tile_service.place_single_tile(self, CavernTile(), 12)
        tile_service.place_single_tile(self, CavernTile(), 13)
        tile_service.place_single_tile(self, TunnelTile(), 20)
        tile_service.place_single_tile(self, TunnelTile(), 21)

        tile_service.place_single_tile(self, MeadowTile(), 27)
        tile_service.place_single_tile(self, FieldTile(), 34)
        tile_service.place_single_tile(self, FieldTile(), 35)

if __name__ == "__main__":
    import cProfile

#    cProfile.run("main_exhaustive()", "profiles/turn_execution_service_profile.exhaustive")
    cProfile.run("main_pruning()", "profiles/turn_execution_service_profile.pruning")
    cProfile.run("main_bulk()", "profiles/turn_execution_service_profile.bulk")
