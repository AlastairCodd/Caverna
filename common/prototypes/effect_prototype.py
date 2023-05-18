from typing import Dict, Type, Callable

from buisness_logic.effects.allow_farming_effect import AllowFarmingEffect
from core.baseClasses.base_effect import BaseEffect
from core.baseClasses.base_prototype import BaseImmutablePrototype


class EffectPrototype(BaseImmutablePrototype[BaseEffect]):
    def __init__(self) -> None:
        self._complex_effect_generation_methods: Dict[Type, Callable[[BaseEffect], BaseEffect]] = {
            AllowFarmingEffect: self._clone_allow_farming_effect
        }

    def clone(self, source: BaseEffect) -> BaseEffect:
        if source is None:
            raise ValueError("Source may not be None")

        if not source.holds_state:
            return source

        result = self._complex_effect_generation_methods[source.__class__](source)
        return result

    def _clone_allow_farming_effect(
            self,
            source: BaseEffect) -> AllowFarmingEffect:
        if source is None:
            raise ValueError("Source may not be None")
        if not isinstance(source, AllowFarmingEffect):
            raise ValueError("Source must be an AllowFarmingEffect")

        result: AllowFarmingEffect = AllowFarmingEffect(
            source.planted_resource_type,
            source.planted_resource_amount)

        return result
