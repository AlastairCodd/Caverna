from buisness_logic.effects.population_effects import *
from core.constants import game_constants
from core.enums.harvest_type_enum import HarvestTypeEnum
from core.enums.caverna_enums import ResourceTypeEnum


# TODO: actually look at the cards (some of them might have more than 3 food)
# TODO: this number is pulled out of thin air
ACHIEVABLE_FOOD_PER_TURN = 3

def get_desirability_of_dwarves(
        dwarves,
        resources,
        tiles,
        turn_descriptor)
    can_increase_capacity = True
    capacity = sum(effect.capacity for effect in tiles.effects for tile in tiles if isinstance(effect, IncreasePopulationCapacityEffect))
    if capacity > 5:
        capacity = 5
        if any(tile for effect in tile.effects for tile in tiles if isinstance(effect, IncreasePopulationMaximumEffect)):
            capacity = 6
            can_increase_capacity = False
        else:
            can_increase_capacity = any(tile for for effect in tile.effects for tile in turn_descriptor.tiles if isinstance(effect, IncreasePopulationMaximumEffect))

    already_has_room = len(dwarves) < capacity

    required_food = sum(
    has_food = resources.get(ResourceTypeEnum.food, 0) >= 

    number_of_remaining_turns = game_constants.number_of_rounds - turn_descriptor.round_index

    return 0.5

class DoesPlayerHaveFood:
    Yes = auto()
    NoButCanConvert = auto()
    NoButLikelyToBeAbleToReachIt = auto()
    NoAndNoTimeRemains = auto()

def does_player_have_food_to_feed_dwarves_this_turn:
    if harvest_type == HarvestTypeEnum.NoHarvest:
        return DoesPlayerHaveFood.Yes

    required_food_for_adults = 1 if harvest_type == HarvestTypeEnum.OneFoodPerDwarf else 2
    required_food = 1 + sum(required_food_for_adults if dwarf.is_adult else 1 for dwarf in dwarves)

    food_player_current_has = resources.get(ResourceTypeEnum.food, 0)
    if food_player_currently_has >= required_food:
        return DoesPlayerHaveFood.Yes

    # TODO: currently ignoring food conversion effects

    # TODO: resources here does not consider resources planted in fields
    food_conversions = conversions_to_have_enough_food.get_conversions_to_afford_specific_amount_of_food(
        required_food,
        dwarves,
        resources,
        harvest_type,
        conversion_effects)

    # len(food_conversions.conversions) == 0 implies that we don't have any resources to convert _into_ food
    #    all of the other reasons for that value to be returned are handled in this method instead 

    if food_conversions.will_pay_for_all_food:
        return DoesPlayerHaveFood.NoButCanConvert

    turns_remaining_this_round = len(dwarves) - turn_descriptor.turn_index
    if turns_remaining_this_round * ACHIEVABLE_FOOD_PER_TURN >= required_food:
        return DoesPlayerHaveFood.NoButLikelyToBeAbleToReachIt

    return DoesPlayerHaveFood.NoAndNoTimeRemains


