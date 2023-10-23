from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import override

from validators.IpropertyValidator import IPropertyValidator
from IValidationContext import ValidationContext


class PropertyValidator[T,TProperty](IPropertyValidator[T,TProperty]):
    @property
    @abstractmethod
    def Name(self): ...

    @override
    def get_default_message_template(erro_code:str)->str: return "No default error message has been specified"

    @abstractmethod
    def is_valid(context:ValidationContext[T],value:TProperty): ...

