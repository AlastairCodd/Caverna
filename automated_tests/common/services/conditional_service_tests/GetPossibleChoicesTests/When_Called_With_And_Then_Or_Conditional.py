import unittest
from core.baseClasses.base_action import BaseAction
from core.enums.cavernaEnums import ActionCombinationEnum
from common.entities.multiconditional import Conditional
from common.services.conditional_service import ConditionalService

class When_Called_With_And_Then_Or_Conditional(unittest.TestCase):
    def setUp(self):
        self._SUT = ConditionalService()
    
        self._a = BaseAction()
        self._b = BaseAction()
    
        self._givenConditional = Conditional(
            ActionCombinationEnum.AndThenOr,
            a, b)
        self._result = self._SUT.get_possible_choices( self._givenConditional )
    
    def test_Then_The_Result_Should_Not_Be_Null(self):
        self.assertIsNotNone(self._result)
        
    def test_Then_The_Result_Should_Be_A_List(self):
        self.assertIsInstance(self._result, list)
    
    def test_Then_Result_Should_Not_Be_Empty(self):
        self.assertNotEqual(len(self._result), 0)
        
    def test_Then_Result_Should_Be_The_Correct_Length(self):
        self.assertEqual(len(self._result), 2)
        
    def test_Then_Result_Should_Contain_Given_Action(self):
        self.assertIn(self._given_action, self._result)
        
if __name__ == '__main__':
    print("check")
    unittest.main()