from abc import abstractmethod, ABC
from typing import Self, TypeVar
from validators import *
from dataclasses import dataclass

from validators.IpropertyValidator import IPropertyValidator
from IValidator import IValidator


IIRuleBuilderOptions = TypeVar("IIRuleBuilderOptions",bound="IRuleBuilderOptions")


class IRuleBuilder[T, TProperty] (ABC): 
    @abstractmethod
    def SetValidator(validator: IPropertyValidator[T, TProperty])->IIRuleBuilderOptions: ...

@dataclass
class IRuleBuilderInitial[T,TProperty](IRuleBuilder[T, TProperty]):
    ...


class IRuleBuilderOptions[T,TProperty](IRuleBuilder[T, TProperty]):
    @abstractmethod
    def DependentRules(action)->Self: ...

