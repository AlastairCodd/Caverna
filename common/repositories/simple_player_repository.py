from core.repositories.base_player_repository import BasePlayerRepository


class SimplePlayerRepository(BasePlayerRepository):
    def __init__(
            self,
            player_id: int,
            turn_index: int) -> None:
        BasePlayerRepository.__init__(self, player_id, turn_index)
