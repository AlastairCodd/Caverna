from core.enums.caverna_enums import TriggerStateEnum


class BaseEffect(object):
    def __init__(self, trigger_state=TriggerStateEnum.UserChoice):
        self._triggerState = trigger_state