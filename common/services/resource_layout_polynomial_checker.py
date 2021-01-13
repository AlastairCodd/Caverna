from functools import reduce
from typing import Dict, Iterable, Tuple, Optional, List

from common.entities.multi_variable_polynomial import MultiVariablePolynomial, Monomial
from core.constants import resource_types
from core.enums.caverna_enums import ResourceTypeEnum
from core.services.resource_layout_check_service import ResourceLayoutCheckService


class ResourceLayoutPolynomialChecker(ResourceLayoutCheckService):
    def __init__(self) -> None:
        self._variable_to_animal: Dict[str, ResourceTypeEnum] = {resource.name[0]: resource for resource in resource_types.farm_animals}

    def check_resource_layout(
            self,
            resource_layout: Dict[int, Dict[ResourceTypeEnum, int]],
            current_resources: Dict[ResourceTypeEnum, int]) \
            -> Iterable[Tuple[
                bool,
                Dict[int, Optional[ResourceTypeEnum]],
                Dict[ResourceTypeEnum, int],
                Dict[ResourceTypeEnum, int]
            ]]:
        tiles_as_polynomials: List[MultiVariablePolynomial] = self._convert_resource_layout_to_polynomials(resource_layout)
        resultant_polynomial: MultiVariablePolynomial = reduce(lambda x, y: x * y, tiles_as_polynomials)
        for term in resultant_polynomial.terms:
            success, remaining, excess = self._compare_term_against_resources(term, current_resources)
            yield success, {}, remaining, excess

    def _convert_resource_layout_to_polynomials(
            self,
            resource_layout: Dict[int, Dict[ResourceTypeEnum, int]]) -> List[MultiVariablePolynomial]:
        result: List[MultiVariablePolynomial] = []
        for location, resources in resource_layout.items():
            terms: Dict[Monomial, int] = {}
            for resource in resources:
                if resources[resource] > 0:
                    term: Monomial = Monomial({resource.name[0]: resources[resource]})
                    terms[term] = 1
            polynomial: MultiVariablePolynomial = MultiVariablePolynomial(terms)
            result.append(polynomial)
        return result

    def _compare_term_against_resources(
            self,
            term: Monomial,
            current_resources: Dict[ResourceTypeEnum, int]) \
            -> Tuple[bool,
                     Dict[ResourceTypeEnum, int],
                     Dict[ResourceTypeEnum, int]]:
        success: bool = True
        excess: Dict[ResourceTypeEnum, int] = {}
        remaining: Dict[ResourceTypeEnum, int] = {}
        for animal, number_of_animals in current_resources.items():
            exponent: int = term.exponent_for_variable(animal.name[0])
            if number_of_animals > exponent:
                success = False
                remaining[animal] = number_of_animals - exponent
            else:
                excess[animal] = exponent - number_of_animals

        return success, remaining, excess
