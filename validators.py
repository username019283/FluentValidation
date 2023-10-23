
from abc import ABC, abstractmethod

import re
from typing import Any, Callable, TypeVar

from IValidationContext import ValidationContext



class PropertyValidator(ABC):
    # @property
    # @abstractmethod
    # def name(self)-> str: ...

    @abstractmethod
    def is_valid(context:ValidationContext, value:Any): ...





class IRegularExpressionValidator(ABC):
    @property
    @abstractmethod
    def pattern(self): ...


class RegularExpressionValidator[T](PropertyValidator,IRegularExpressionValidator):
    _regex_func:Callable[[T],type(re)]

    def __init__(self,pattern:str) -> None:
        self._pattern:str = pattern
        self._regex_func = re.compile(pattern)

    @property
    def pattern(self): return self._pattern
    @pattern.setter
    def pattern(self, pattern):
        self._expression:str = pattern
