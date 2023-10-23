from typing import Self
from abc import ABC, abstractmethod

from results.ValidationFailure import ValidationFailure


class IValidationContext(ABC): 
    @property
    @abstractmethod
    def ParentContext(self)->Self: ...
    
    @property
    @abstractmethod
    def instance_to_validate(self)->object: ...

    @property
    @abstractmethod
    def ThrowOnFailures(self)->bool: ...

    


class IHasFailures(ABC):
    @property
    @abstractmethod
    def Failures(self)->list[ValidationFailure]: ...




class ValidationContext[T](IValidationContext,ValidationFailure):
    def __init__(self
        , instance_to_validate:T
        , failures:list[ValidationFailure] = []
        ) -> None:        

        self._instance_to_validate = instance_to_validate,
        self._failures:list[ValidationFailure] = failures

    @property
    def ParentContext(self)->Self: return self._parentContext
        
    @property
    def instance_to_validate(self)->object: self._instance_to_validate

    @property
    def ThrowOnFailures(self)->bool: ...

    @property
    def Failures(self)->list[ValidationFailure]: return self._failures
