from abc import ABC, abstractmethod
import inspect

from typing import Iterable, Callable,Any, TypeVar
from internal.IRuleComponent import IRuleComponent
from IValidationContext import IValidationContext
from validators.IpropertyValidator import IPropertyValidator

IIValidationRule = TypeVar("IIValidationRule",bound="IValidationRule")


class IValidatoinRule_no_args(ABC):   
    @property
    @abstractmethod
    def Components(self)-> Iterable[IRuleComponent]: ...
    
    
    @property
    @abstractmethod
    def PropertyName(self)-> str: ...
    

    @property
    @abstractmethod
    def TypeToValidate(self)-> type: ...
    
    
    @abstractmethod
    def GetDisplayName(context:IValidationContext)-> str: ...





class IValidationRule[T,TProperty](IValidatoinRule_no_args): 
    @property
    @abstractmethod
    def Current(self)->IRuleComponent: ...
    
    @abstractmethod
    def AddValidator(validator:IPropertyValidator[T,TProperty]): ...




class IValidationRuleInternal[T,TProperty](IValidationRule[T,TProperty]):
    ...