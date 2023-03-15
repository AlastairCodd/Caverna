from typing import Dict

from automated_tests.business_logic_tests.service_tests.processor_service_tests.twin_tile_placement_action_choice_processor_service_tests.given_a_twin_tile_placement_action_choice_processor_service import \
    Given_A_TwinTilePlacementActionChoiceProcessorService
from buisness_logic.services.processor_services.twin_tile_placement_action_choice_processor_service import TwinPlacementActionChoice
from common.entities.tile_twin_placement_lookup import TileTwinPlacementLookup
from core.enums.caverna_enums import TileDirectionEnum


class test_when_index_is_within_range(Given_A_TwinTilePlacementActionChoiceProcessorService):
    def because(self) -> None:
        self._placements: Dict[int, TileTwinPlacementLookup] = {
            0: TileTwinPlacementLookup(0, TileDirectionEnum.right),
            1: TileTwinPlacementLookup(0, TileDirectionEnum.down),
            2: TileTwinPlacementLookup(7, TileDirectionEnum.down),
            3: TileTwinPlacementLookup(7, TileDirectionEnum.left),
            4: TileTwinPlacementLookup(40, TileDirectionEnum.up),
            5: TileTwinPlacementLookup(40, TileDirectionEnum.right),
            6: TileTwinPlacementLookup(47, TileDirectionEnum.up),
            7: TileTwinPlacementLookup(47, TileDirectionEnum.left),

            8: TileTwinPlacementLookup(1, TileDirectionEnum.right),
            9: TileTwinPlacementLookup(1, TileDirectionEnum.down),
            10: TileTwinPlacementLookup(1, TileDirectionEnum.left),
            11: TileTwinPlacementLookup(2, TileDirectionEnum.right),
            12: TileTwinPlacementLookup(2, TileDirectionEnum.down),
            13: TileTwinPlacementLookup(2, TileDirectionEnum.left),
            14: TileTwinPlacementLookup(3, TileDirectionEnum.right),
            15: TileTwinPlacementLookup(3, TileDirectionEnum.down),
            16: TileTwinPlacementLookup(3, TileDirectionEnum.left),
            17: TileTwinPlacementLookup(4, TileDirectionEnum.right),
            18: TileTwinPlacementLookup(4, TileDirectionEnum.down),
            19: TileTwinPlacementLookup(4, TileDirectionEnum.left),
            20: TileTwinPlacementLookup(5, TileDirectionEnum.right),
            21: TileTwinPlacementLookup(5, TileDirectionEnum.down),
            22: TileTwinPlacementLookup(5, TileDirectionEnum.left),
            23: TileTwinPlacementLookup(6, TileDirectionEnum.right),
            24: TileTwinPlacementLookup(6, TileDirectionEnum.down),
            25: TileTwinPlacementLookup(6, TileDirectionEnum.left),

            26: TileTwinPlacementLookup(41, TileDirectionEnum.up),
            27: TileTwinPlacementLookup(41, TileDirectionEnum.right),
            28: TileTwinPlacementLookup(41, TileDirectionEnum.left),
            29: TileTwinPlacementLookup(42, TileDirectionEnum.up),
            30: TileTwinPlacementLookup(42, TileDirectionEnum.right),
            31: TileTwinPlacementLookup(42, TileDirectionEnum.left),
            32: TileTwinPlacementLookup(43, TileDirectionEnum.up),
            33: TileTwinPlacementLookup(43, TileDirectionEnum.right),
            34: TileTwinPlacementLookup(43, TileDirectionEnum.left),
            35: TileTwinPlacementLookup(44, TileDirectionEnum.up),
            36: TileTwinPlacementLookup(44, TileDirectionEnum.right),
            37: TileTwinPlacementLookup(44, TileDirectionEnum.left),
            38: TileTwinPlacementLookup(45, TileDirectionEnum.up),
            39: TileTwinPlacementLookup(45, TileDirectionEnum.right),
            40: TileTwinPlacementLookup(45, TileDirectionEnum.left),
            41: TileTwinPlacementLookup(46, TileDirectionEnum.up),
            42: TileTwinPlacementLookup(46, TileDirectionEnum.right),
            43: TileTwinPlacementLookup(46, TileDirectionEnum.left),

            44: TileTwinPlacementLookup(8, TileDirectionEnum.up),
            45: TileTwinPlacementLookup(8, TileDirectionEnum.right),
            46: TileTwinPlacementLookup(8, TileDirectionEnum.down),
            47: TileTwinPlacementLookup(16, TileDirectionEnum.up),
            48: TileTwinPlacementLookup(16, TileDirectionEnum.right),
            49: TileTwinPlacementLookup(16, TileDirectionEnum.down),
            50: TileTwinPlacementLookup(24, TileDirectionEnum.up),
            51: TileTwinPlacementLookup(24, TileDirectionEnum.right),
            52: TileTwinPlacementLookup(24, TileDirectionEnum.down),
            53: TileTwinPlacementLookup(32, TileDirectionEnum.up),
            54: TileTwinPlacementLookup(32, TileDirectionEnum.right),
            55: TileTwinPlacementLookup(32, TileDirectionEnum.down),

            56: TileTwinPlacementLookup(15, TileDirectionEnum.up),
            57: TileTwinPlacementLookup(15, TileDirectionEnum.down),
            58: TileTwinPlacementLookup(15, TileDirectionEnum.left),
            59: TileTwinPlacementLookup(23, TileDirectionEnum.up),
            60: TileTwinPlacementLookup(23, TileDirectionEnum.down),
            61: TileTwinPlacementLookup(23, TileDirectionEnum.left),
            62: TileTwinPlacementLookup(31, TileDirectionEnum.up),
            63: TileTwinPlacementLookup(31, TileDirectionEnum.down),
            64: TileTwinPlacementLookup(31, TileDirectionEnum.left),
            65: TileTwinPlacementLookup(39, TileDirectionEnum.up),
            66: TileTwinPlacementLookup(39, TileDirectionEnum.down),
            67: TileTwinPlacementLookup(39, TileDirectionEnum.left),

            68: TileTwinPlacementLookup(9, TileDirectionEnum.up),
            69: TileTwinPlacementLookup(9, TileDirectionEnum.right),
            70: TileTwinPlacementLookup(9, TileDirectionEnum.down),
            71: TileTwinPlacementLookup(9, TileDirectionEnum.left),
            72: TileTwinPlacementLookup(10, TileDirectionEnum.up),
            73: TileTwinPlacementLookup(10, TileDirectionEnum.right),
            74: TileTwinPlacementLookup(10, TileDirectionEnum.down),
            75: TileTwinPlacementLookup(10, TileDirectionEnum.left),
            76: TileTwinPlacementLookup(11, TileDirectionEnum.up),
            77: TileTwinPlacementLookup(11, TileDirectionEnum.right),
            78: TileTwinPlacementLookup(11, TileDirectionEnum.down),
            79: TileTwinPlacementLookup(11, TileDirectionEnum.left),
            80: TileTwinPlacementLookup(12, TileDirectionEnum.up),
            81: TileTwinPlacementLookup(12, TileDirectionEnum.right),
            82: TileTwinPlacementLookup(12, TileDirectionEnum.down),
            83: TileTwinPlacementLookup(12, TileDirectionEnum.left),
            84: TileTwinPlacementLookup(13, TileDirectionEnum.up),
            85: TileTwinPlacementLookup(13, TileDirectionEnum.right),
            86: TileTwinPlacementLookup(13, TileDirectionEnum.down),
            87: TileTwinPlacementLookup(13, TileDirectionEnum.left),
            88: TileTwinPlacementLookup(14, TileDirectionEnum.up),
            89: TileTwinPlacementLookup(14, TileDirectionEnum.right),
            90: TileTwinPlacementLookup(14, TileDirectionEnum.down),
            91: TileTwinPlacementLookup(14, TileDirectionEnum.left),

            92: TileTwinPlacementLookup(17, TileDirectionEnum.up),
            93: TileTwinPlacementLookup(17, TileDirectionEnum.right),
            94: TileTwinPlacementLookup(17, TileDirectionEnum.down),
            95: TileTwinPlacementLookup(17, TileDirectionEnum.left),
            96: TileTwinPlacementLookup(18, TileDirectionEnum.up),
            97: TileTwinPlacementLookup(18, TileDirectionEnum.right),
            98: TileTwinPlacementLookup(18, TileDirectionEnum.down),
            99: TileTwinPlacementLookup(18, TileDirectionEnum.left),
            100: TileTwinPlacementLookup(19, TileDirectionEnum.up),
            101: TileTwinPlacementLookup(19, TileDirectionEnum.right),
            102: TileTwinPlacementLookup(19, TileDirectionEnum.down),
            103: TileTwinPlacementLookup(19, TileDirectionEnum.left),
            104: TileTwinPlacementLookup(20, TileDirectionEnum.up),
            105: TileTwinPlacementLookup(20, TileDirectionEnum.right),
            106: TileTwinPlacementLookup(20, TileDirectionEnum.down),
            107: TileTwinPlacementLookup(20, TileDirectionEnum.left),
            108: TileTwinPlacementLookup(21, TileDirectionEnum.up),
            109: TileTwinPlacementLookup(21, TileDirectionEnum.right),
            110: TileTwinPlacementLookup(21, TileDirectionEnum.down),
            111: TileTwinPlacementLookup(21, TileDirectionEnum.left),
            112: TileTwinPlacementLookup(22, TileDirectionEnum.up),
            113: TileTwinPlacementLookup(22, TileDirectionEnum.right),
            114: TileTwinPlacementLookup(22, TileDirectionEnum.down),
            115: TileTwinPlacementLookup(22, TileDirectionEnum.left),

            116: TileTwinPlacementLookup(25, TileDirectionEnum.up),
            117: TileTwinPlacementLookup(25, TileDirectionEnum.right),
            118: TileTwinPlacementLookup(25, TileDirectionEnum.down),
            119: TileTwinPlacementLookup(25, TileDirectionEnum.left),
            120: TileTwinPlacementLookup(26, TileDirectionEnum.up),
            121: TileTwinPlacementLookup(26, TileDirectionEnum.right),
            122: TileTwinPlacementLookup(26, TileDirectionEnum.down),
            123: TileTwinPlacementLookup(26, TileDirectionEnum.left),
            124: TileTwinPlacementLookup(27, TileDirectionEnum.up),
            125: TileTwinPlacementLookup(27, TileDirectionEnum.right),
            126: TileTwinPlacementLookup(27, TileDirectionEnum.down),
            127: TileTwinPlacementLookup(27, TileDirectionEnum.left),
            128: TileTwinPlacementLookup(28, TileDirectionEnum.up),
            129: TileTwinPlacementLookup(28, TileDirectionEnum.right),
            130: TileTwinPlacementLookup(28, TileDirectionEnum.down),
            131: TileTwinPlacementLookup(28, TileDirectionEnum.left),
            132: TileTwinPlacementLookup(29, TileDirectionEnum.up),
            133: TileTwinPlacementLookup(29, TileDirectionEnum.right),
            134: TileTwinPlacementLookup(29, TileDirectionEnum.down),
            135: TileTwinPlacementLookup(29, TileDirectionEnum.left),
            136: TileTwinPlacementLookup(30, TileDirectionEnum.up),
            137: TileTwinPlacementLookup(30, TileDirectionEnum.right),
            138: TileTwinPlacementLookup(30, TileDirectionEnum.down),
            139: TileTwinPlacementLookup(30, TileDirectionEnum.left),

            140: TileTwinPlacementLookup(33, TileDirectionEnum.up),
            141: TileTwinPlacementLookup(33, TileDirectionEnum.right),
            142: TileTwinPlacementLookup(33, TileDirectionEnum.down),
            143: TileTwinPlacementLookup(33, TileDirectionEnum.left),
            144: TileTwinPlacementLookup(34, TileDirectionEnum.up),
            145: TileTwinPlacementLookup(34, TileDirectionEnum.right),
            146: TileTwinPlacementLookup(34, TileDirectionEnum.down),
            147: TileTwinPlacementLookup(34, TileDirectionEnum.left),
            148: TileTwinPlacementLookup(35, TileDirectionEnum.up),
            149: TileTwinPlacementLookup(35, TileDirectionEnum.right),
            150: TileTwinPlacementLookup(35, TileDirectionEnum.down),
            151: TileTwinPlacementLookup(35, TileDirectionEnum.left),
            152: TileTwinPlacementLookup(36, TileDirectionEnum.up),
            153: TileTwinPlacementLookup(36, TileDirectionEnum.right),
            154: TileTwinPlacementLookup(36, TileDirectionEnum.down),
            155: TileTwinPlacementLookup(36, TileDirectionEnum.left),
            156: TileTwinPlacementLookup(37, TileDirectionEnum.up),
            157: TileTwinPlacementLookup(37, TileDirectionEnum.right),
            158: TileTwinPlacementLookup(37, TileDirectionEnum.down),
            159: TileTwinPlacementLookup(37, TileDirectionEnum.left),
            160: TileTwinPlacementLookup(38, TileDirectionEnum.up),
            161: TileTwinPlacementLookup(38, TileDirectionEnum.right),
            162: TileTwinPlacementLookup(38, TileDirectionEnum.down),
            163: TileTwinPlacementLookup(38, TileDirectionEnum.left),

            164: TileTwinPlacementLookup(0, TileDirectionEnum.right),
            165: TileTwinPlacementLookup(0, TileDirectionEnum.down),
            166: TileTwinPlacementLookup(7, TileDirectionEnum.down),
            167: TileTwinPlacementLookup(7, TileDirectionEnum.left),
            168: TileTwinPlacementLookup(40, TileDirectionEnum.up),
            169: TileTwinPlacementLookup(40, TileDirectionEnum.right),
            170: TileTwinPlacementLookup(47, TileDirectionEnum.up),
            171: TileTwinPlacementLookup(47, TileDirectionEnum.left),
        }

    def test_then_result_should_be_expected(self) -> None:
        for index, placement in self._placements.items():
            with self.subTest(position=index):
                calculated_placement: TwinPlacementActionChoice = self.SUT.convert_index_to_placement(index)
                self.assertEqual(placement, calculated_placement.placement)