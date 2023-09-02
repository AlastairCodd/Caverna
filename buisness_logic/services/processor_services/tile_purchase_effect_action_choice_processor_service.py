from core.services.base_action_choice_processor_service import BaseActionChoiceProcessorService


class TilePurchaseEffectActionChoiceProcessorService(BaseActionChoiceProcessorService):
    def __init__(self) -> None:
        number_of_tile_purchase_effects: int = 2

        BaseActionChoiceProcessorService.__init__(self, 2)
