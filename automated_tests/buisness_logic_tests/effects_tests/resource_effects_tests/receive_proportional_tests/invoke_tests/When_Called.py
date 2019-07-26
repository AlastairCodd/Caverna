import unittest
from core.enums.caverna_enums import ResourceTypeEnum
from core.containers.resource_container import ResourceContainer
from buisness_logic.effects.resource_effects import ReceiveProportional

class When_Called(unittest.TestCase):
    def setUp(self):
        receiveProportional = ReceiveProportional( 
            {ResourceTypeEnum.wood: 2},
            {ResourceTypeEnum.stone: 5} )
        
        self._player = ResourceContainer()
        self._player.give_resource( ResourceTypeEnum.stone, 13 )
        
        receiveProportional.invoke(self._player)
        
    def test_Then_Player_Should_Have_4_Wood(self):
        self.assertEqual(
            self._player
                .get_resources()
                .get(ResourceTypeEnum.wood),
            4 )
                