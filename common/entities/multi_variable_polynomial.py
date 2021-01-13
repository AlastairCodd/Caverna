import collections
import itertools
from typing import Union, Dict, Iterable, Set


class MultiVariablePolynomial(object):
    def __init__(self, val: Union['MultiVariablePolynomial', int, Dict['Monomial', int]]):
        """
        Create a MultiVariablePolynomial in one of three ways:

        p = MultiVariablePolynomial(poly)                                    # copy constructor
        p = MultiVariablePolynomial({Monomial(x): 1, Monomial(xy): 2, ...})  # base type
        p = MultiVariablePolynomial(1)                                       # from scalar
        """
        super(MultiVariablePolynomial, self).__init__()
        self._terms: Dict[Monomial, int] = {}

        if isinstance(val, MultiVariablePolynomial):  # copy constructor
            for term in val.terms:
                variable: Monomial = Monomial(term)
                coefficient: int = val.terms[term]
                self._terms[variable] = coefficient
        elif isinstance(val, dict):
            for term in val:
                variable: Monomial = Monomial(term)
                coefficient: int = val[term]
                self._terms[variable] = coefficient
        else:  # from single scalar
            self._terms[Monomial({})] = val + 0
        self.trim()

    @property
    def terms(self) -> Dict['Monomial', int]:
        return {Monomial(x): self._terms[x] for x in self._terms}

    def get_coefficient_for_variable(self, variable: 'Monomial') -> int:
        return self._terms.get(variable, 0)

    def __add__(self, val: Union['MultiVariablePolynomial', int]) -> 'MultiVariablePolynomial':
        "Return self+val"
        res: Dict[Monomial, int]
        if isinstance(val, self.__class__):  # add MultiVariablePolynomial
            dict1: Dict[Monomial, int] = self._terms
            dict2: Dict[Monomial, int] = val.terms
            res = {**dict1, **dict2}
            for key, value in res.items():
                if key in dict1 and key in dict2:
                    res[key] = value + dict2[key]
        else:  # add scalar
            constant: Monomial = Monomial({})
            if constant in self._terms:
                res = self.terms
                res += val
            else:
                res = self.terms
                res[constant] = val
        return self.__class__(res)

    def __eq__(self, val):
        "Test self==val"
        if isinstance(val, MultiVariablePolynomial):
            return self.coefficients == val.coefficients
        else:
            return len(self.coefficients) == 1 and self.coefficients[0] == val

    def __mul__(self, val):
        "Return self*val"
        res: Dict[Monomial, int]
        if isinstance(val, MultiVariablePolynomial):
            res = {}
            for selfmo, selfco in self._terms.items():
                for valmo, valco in val._terms.items():
                    resmo: Monomial = selfmo * valmo
                    resco: int = selfco * valco
                    if resmo in res:
                        resco += res[resmo]
                    res[resmo] = resco
        else:
            res = {mo: co * val for mo, co in self._terms.items()}
        return self.__class__(res)

    def __neg__(self):
        "Return -self"
        return self.__class__({mo: -co for mo, co in self._terms.items()})

    def __radd__(self, val):
        "Return val+self"
        return self + val

    def __rmul__(self, val):
        "Return val*self"
        return self * val

    def __rsub__(self, val):
        "Return val-self"
        return -self + val

    def __sub__(self, val):
        "Return self-val"
        return self.__add__(-val)

    def trim(self):
        "Remove trailing 0-coefficients"
        keys = list(self._terms.keys())
        index = len(keys) - 1
        if self._terms[keys[index]] == 0:
            del self._terms[keys[index]]


class Monomial(object):
    def __init__(self, value: Union['Monomial', Dict[str, int], str]) -> None:
        self._terms: Dict[str, int]
        if isinstance(value, self.__class__):
            self._terms = value.terms
        elif isinstance(value, dict):
            self._terms = value.copy()
        elif isinstance(value, str):
            variables: set[str] = set(value)
            self._terms = {v: value.count(v) for v in variables}

    def __mul__(self, other) -> 'Monomial':
        if not isinstance(other, self.__class__):
            raise TypeError()

        dict1: Dict[str, int] = self._terms
        dict2: Dict[str, int] = other._terms
        keys: Set[str] = set(self._terms.keys()).union(other._terms.keys())
        generating: Dict[str, int] = {}
        for key in keys:
            if key in dict1 and key in dict2:
                generating[key] = dict1[key] + dict2[key]
            elif key in dict1:
                generating[key] = dict1[key]
            else:
                generating[key] = dict2[key]
        result: 'Monomial' = self.__class__(generating)
        return result

    @property
    def terms(self) -> Dict[str, int]:
        return self._terms.copy()

    def exponent_for_variable(self, variable: str) -> int:
        if len(variable) != 1:
            raise ValueError()

        result: int = 0
        if variable in self._terms:
            result = self._terms[variable]

        return result

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self._terms == other.terms

    def __str__(self) -> str:
        result: str = ""
        l = sorted(self._terms)
        for variable in l:
            exponent: int = self._terms[variable]
            if exponent > 0:
                result += variable * exponent
        result = result
        return result
