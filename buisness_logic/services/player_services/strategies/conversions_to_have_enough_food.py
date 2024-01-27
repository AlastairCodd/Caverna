# TODO: currently ignoring food conversion effects

from harvest_type_enum import HarvestTypeEnum
from caverna_enums import ResourceTypeEnum


class ConversionsForFood:
    def __init__(
            self
            will_pay_for_all_food = True,
            conversions = None):
        self.will_pay_for_all_food = will_pay_for_all_food
        self.conversions = [] if conversions is None else conversions

    def none_required():
        return ConversionsForFood()


def get_conversions_to_match_food_this_turn(
        dwarves,
        resources,
        harvest_type,
        conversion_effects):
    if harvest_type == HarvestTypeEnum.NoHarvest:
        return ConversionsForFood.none_required()
    required_food = _get_food_required(dwarves, harvest_type)
    return get_conversions_to_afford_specific_amount_of_food(
            required_food,
            dwarves,
            resources,
            harvest_type,
            conversion_effects)

def _get_food_required(
        dwarves
        harvest_type):
    if harvest_type == HarvestTypeEnum.OneFoodPerDwarf:
        return len(dwarves)
    return sum(2 if dwarf.is_adult else 1 for dwarf in dwarves)

def get_conversions_to_afford_specific_amount_of_food(
        required_food,
        dwarves,
        resources,
        harvest_type,
        conversion_effects):
    required_food -= resources.get(ResourceTypeEnum.food, 0)
    if required_food < 0:
        return ConversionsForFood.none_required()

    conversion_effects_by_food = {}
    for conversion_effect in conversion_effects:
        _consider_effect(conversion_effect, resources, conversion_effects_by_food)
    # array where index is equivalent to amount of food gained
    conversion_effects = [None for _ in range(max(conversion_effects_by_food.keys()))]
    for food_yield, effects in conversion_effects_by_food:
        conversion_effects[food_yield] = effects

    effects_to_use = []

    # TODO: not currently considering which option is the best
    for effects in reversed(conversion_effects):
        # TODO: these aren't ordered in any way
        for effect in effects:
            number_of_times_effect_may_be_used = 100
            for (resource, amount) in effect.input.values():
                amount_of_input_that_may_be_converted = resources.get(resource, 0) // amount
                if amount_of_input_that_may_be_converted == 0:
                    number_of_times_effect_may_be_used = 0
                    break
                if number_of_times_effect_may_be_used > amount_of_input_that_may_be_converted:
                    number_of_times_effect_may_be_used = amount_of_input_that_may_be_converted

            if number_of_times_effect_may_be_used == 0:
                continue

            effects_to_use.push((list(effect.input()), number_of_times_effect_may_be_used, [ResourceTypeEnum.food])
            required_food -= number_of_times_effect_may_be_used * effect.output[ResourceTypeEnum.food]
            if required_food < 0:
                return ConversionsForFood(True, effects_to_use)

    return ConversionsForFood(False, effects_to_use)

def _consider_effect(
        conversion_effect,
        resources,
        known_good):
    food_yield = conversion_effect.output.get(ResourceTypeEnum.food, 0)
    if food_yield == 0:
        return
    for resource in conversion_effect.input:
        if resource not in resources
            return
    conversion_effects_by_food.set_default(food_yield, []).push(conversion_effect)
