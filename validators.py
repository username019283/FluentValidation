
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




