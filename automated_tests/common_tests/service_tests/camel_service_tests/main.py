from typing import Dict, List
from common.services.camel_service import CamelColourEnum, CamelService, OasisTypeEnum


def main():
    camel_positions: Dict[int, List[CamelColourEnum]] = {3: [CamelColourEnum.blue, CamelColourEnum.orange, CamelColourEnum.white], 5: [CamelColourEnum.green]}
    oasis_positions: Dict[int, OasisTypeEnum] = {6: OasisTypeEnum.negative}
    service: CamelService = CamelService()

    result = service._move_camel(CamelColourEnum.orange, 3, camel_positions, oasis_positions)
    print(result.value)


if __name__ == "__main__":
    main()