from typing import Callable, Self
from abc import ABC, abstractmethod

from internal.MessageFormatter import MessageFormatter

from results.ValidationFailure import ValidationFailure


class IValidationContext(ABC): 
    # @property
    # @abstractmethod
    # def ParentContext(self)->Self: ...
    
    @property
    @abstractmethod
    def instance_to_validate(self)->object: ...

    @property
    @abstractmethod
    def ThrowOnFailures(self)->bool: ...

    
    # @property
    # @abstractmethod
    # def InstanceToValidate(self)->object: ...
    
    # @property
    # @abstractmethod
    # def RootContextData(self)->dict[str, object]: ...
    
    # @property
    # @abstractmethod
    # def Selector(self)->IValidatorSelector: ...
    
    # @property
    # @abstractmethod
    # def IsChildContext(self)->bool: ...
    
    # @property
    # @abstractmethod
    # def IsChildCollectionContext(self)->bool: ...
    
    # @property
    # @abstractmethod
    # def ParentContext(self)->IValidationContext: ...
    
    # @property
    # @abstractmethod
    # def IsAsync(self)->bool: ...
    
    @property
    @abstractmethod
    def ThrowOnFailures(self)->bool: ...




class IHasFailures(ABC):
    @property
    @abstractmethod
    def Failures(self)->list[ValidationFailure]: ...




class ValidationContext[T](IValidationContext,IHasFailures):
    def __init__(self
        , instance_to_validate:T
        , failures:list[ValidationFailure] = []
        ) -> None:        

        self._instance_to_validate = instance_to_validate
        self._failures:list[ValidationFailure] = failures
        self._messageFormatter: MessageFormatter = MessageFormatter()
        self._property_path:str = None        
        self._displayNameFunc:str = None        

    @property
    def instance_to_validate(self)->object: return self._instance_to_validate

    @property
    def ThrowOnFailures(self)->bool: ...

    @property
    def Failures(self)->list[ValidationFailure]: return self._failures
    
    @property
    def MessageFormatter(self)->MessageFormatter: return self._messageFormatter

    @property
    def PropertyPath(self)->str: return self._property_path

    # def InitializeForPropertyValidator(self, propertyPath:str, displayNameFunc:Callable[[Self],str]):
    def InitializeForPropertyValidator(self, propertyPath:str):
        self._property_path = propertyPath
        # self._displayNameFunc = displayNameFunc