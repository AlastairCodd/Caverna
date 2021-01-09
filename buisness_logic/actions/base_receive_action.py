class BaseReceiveAction(BasePlayerChoiceAction, metaclass=ABCMeta):
    def set_player_choice(
        self,
        player: BasePlayerRepository,
        dwarf: Dwarf,
        turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        action_choice: ActionChoiceLookup
        if any(map(lambda animal: animal in self._receive, resource_types.farm_animals)):
            action: BaseAction = CheckAnimalStorageAction(self)
            preceeds_constraint: BaseConstraint = PreceedsConstraint(self, action)
            action_choice = ActionChoiceLookup([action], [preceeds_constraint])
        else:
            action_choice = ActionChoiceLookup([])
        result: ResultLookup[ActionChoiceLookup] = ResultLookup(True, action_choice)
        return result


class CheckAnimalStorageAction(BasePlayerChoiceAction):
    def set_player_choice(
        self,
        player: BasePlayerRepository,
        dwarf: Dwarf,
        turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        return ActionChoiceLookup([], [UniqueConstraint(self)])


class UniqueConstraint(BaseConstraint):
    # TODO: Might require changing BaseConstraint signature
    pass
