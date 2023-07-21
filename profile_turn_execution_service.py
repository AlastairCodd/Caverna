from buisness_logic.cards.weekly_market_card import WeeklyMarketCard
from buisness_logic.services.turn_execution_service import TurnExecutionService
from common.entities.resources_to_sow_lookup import ResourcesToSow
from common.entities.result_lookup import ResultLookup
from common.entities.tile_twin_placement_lookup import TileTwinPlacementLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.enums.caverna_enums import TileDirectionEnum, ResourceTypeEnum
from core.enums.harvest_type_enum import HarvestTypeEnum
from core.services.base_player_service import BasePlayerService, InvalidActionCombinationResponse


def main_exhaustive():
    from common.services.exhaustive_action_ordering_service import ExhaustiveActionOrderingService
    main(ExhaustiveActionOrderingService())

def main_pruning():
    from common.services.pruning_action_ordering_service import PruningActionOrderingService
    main(PruningActionOrderingService())

def main_configurable():
    from common.services.configurable_action_ordering_service import ConfigurableActionOrderingService
    main(ConfigurableActionOrderingService())

def main_allocation_free_list_permutation():
    from common.forges.allocation_free_list_permutation_forge import AllocationFreeListPermutationForge
    from common.services.configurable_action_ordering_service import ConfigurableActionOrderingService

    ordering_service = ConfigurableActionOrderingService(
        permutation_forge = AllocationFreeListPermutationForge())

    main(ordering_service)

def main_single_loop_validator():
    from common.services.single_loop_constraint_validator import SingleLoopConstraintValidator
    from common.services.configurable_action_ordering_service import ConfigurableActionOrderingService

    validator = None
    ordering_service = ConfigurableActionOrderingService(
        constraint_validator_func = lambda constraints: SingleLoopConstraintValidator(constraints))

    main(ordering_service)

def main_bitmanipulation_validator():
    from common.services.bitmanip_constraint_validator import BitmanipConstraintValidator
    from common.services.configurable_action_ordering_service import ConfigurableActionOrderingService

    validator = None
    ordering_service = ConfigurableActionOrderingService(
        constraint_validator_func = lambda constraints: BitmanipConstraintValidator(constraints))

    main(ordering_service)

def main_current_fastest():
    from common.services.bitmanip_constraint_validator import BitmanipConstraintValidator
    from common.forges.allocation_free_list_permutation_forge import AllocationFreeListPermutationForge
    from common.services.configurable_action_ordering_service import ConfigurableActionOrderingService

    validator = None
    ordering_service = ConfigurableActionOrderingService(
        permutation_forge = AllocationFreeListPermutationForge(),
        constraint_validator_func = lambda constraints: BitmanipConstraintValidator(constraints))

    main(ordering_service)

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

    def report_action_choice_failed(
            self,
            actions) -> InvalidActionCombinationResponse:
        raise NotImplementedError()

    def get_player_choice_card_to_use(self, _cards, _turn_descriptor):
        return ResultLookup(True, self._card)

    def get_player_choice_actions_to_use(self, choices, _turn_descriptor):
        print(repr(choices[0]))
        return ResultLookup(True, choices[0])

    def get_player_choice_free_actions_to_use(self, _turn_descriptor):
        return []

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
        self._place_tile(tile_service, TunnelTile(), 20)
        self._place_tile(tile_service, TunnelTile(), 21)
        self._place_tile(tile_service, CavernTile(), 12)
        self._place_tile(tile_service, CavernTile(), 13)

        self._place_tile(tile_service, FieldTile(), 35)
        self._place_tile(tile_service, MeadowTile(), 27)
        self._place_tile(tile_service, FieldTile(), 34)

    def _place_tile(self, tile_service, tile, location):
        if not (result := tile_service.place_single_tile(self, tile, location)).flag:
            for error in result.errors:
                print(error)


if __name__ == "__main__":
    import cProfile
    import logging
    from core.constants.logging import VERBOSE_LOG_LEVEL

    logging.basicConfig(
#            filename="profiles/debug.log",
            format='[%(levelname)-8s] %(message)s',
            level=VERBOSE_LOG_LEVEL)
    logging.addLevelName(VERBOSE_LOG_LEVEL, "VERBOSE")

#    cProfile.run("main_exhaustive()", "profiles/turn_execution_service_profile.exhaustive")
#    cProfile.run("main_pruning()", "profiles/turn_execution_service_profile.pruning")
#    cProfile.run("main_configurable()", "profiles/turn_execution_service_profile.configurable")
#    cProfile.run("main_allocation_free_list_permutation()", "profiles/turn_execution_service_profile.alloc_free_permutations")
#    cProfile.run("main_single_loop_validator()", "profiles/turn_execution_service_profile.single_loop_validator")
#    cProfile.run("main_bitmanipulation_validator()", "profiles/turn_execution_service_profile.bitmanip_validator")
    cProfile.run("main_current_fastest()", "profiles/turn_execution_service_profile")
