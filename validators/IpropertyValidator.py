from abc import ABC, abstractmethod
from dataclasses import dataclass

from IValidationContext import ValidationContext

@dataclass
class IPropertyValidator[T,TProperty](ABC):
    @property
    @abstractmethod
    def Name(self)->str:...

    @abstractmethod
    def get_default_message_template(erro_code:str)->str: ...

    @abstractmethod
    def is_valid(context:ValidationContext[T],value:TProperty): ...

