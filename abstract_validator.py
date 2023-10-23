from abc import ABC
from typing import Any, Callable, Generic, Self, TypeVar, NewType
from enum import Enum
import inspect
import dis


from dataclasses import dataclass
import re

from typing import List
from collections import defaultdict
from validators.IpropertyValidator import IPropertyValidator

from results.ValidationResult import ValidationResult
from IValidationContext import ValidationContext
from IValidationRule import *
from syntax import *

from validators.RegularExpressionValidator import RegularExpressionValidator

TAbstractValidator = TypeVar("TAbstractValidator",bound="AbstractValidator")
TRuleBuilder = TypeVar("TRuleBuilder",bound="RuleBuilder")
TPropertyRule = TypeVar("TPropertyRule",bound="PropertyRule")

T = TypeVar("T")

class RuleComponent[T,TProperty](IRuleComponent):
    def __init__(self,property_validator:IPropertyValidator[T,TProperty]) -> None:
        self._property_validator:IPropertyValidator[T,TProperty]= property_validator
        self._validator:IPropertyValidator = None
        self._error_message:str = None


    @property
    def ErroCode(self)->str: return self._error_message
    
    @property
    def Validator(self)-> IPropertyValidator: return self._validator

    def set_error_message(self,error_message:str)-> None:
        self._error_message = error_message


class RuleBase_abc[T,TProperty,TValue](IValidationRule[T,TValue]):
    def __init__(self,func:Callable[[T],TProperty],type_to_validate:type):
        self._func = func
        self._type_to_validate = type_to_validate
        
        self._components:List[RuleComponent[T, TProperty]] = []
        self._propertyName:str = {x.opname:x.argval for x in dis.Bytecode(func)}["LOAD_ATTR"]
        self._displayName:str = self._propertyName


    @property
    def Func(self): return self._func
    @property
    def TypeToValidate(self): return self._type_to_validate

    @property
    def Components(self): return self._components

    @property
    def PropertyName(self): return self._propertyName
    @property
    def displayName(self): return self._displayName

    @property
    def Current(self)->IRuleComponent: return self._components[-1]




class PropertyRule[T,TProperty](RuleBase_abc[T,TProperty,TProperty]):
    def __init__(self,func:Callable[[T],TProperty],type_to_validate:type):
        super().__init__(func,type_to_validate)

    @classmethod
    def create(cls, func:Callable[[T],TProperty]):
        return PropertyRule(func,type(TProperty))

    def AddValidator(self,validator:IPropertyValidator[T,TProperty])->None:
        component:RuleComponent = RuleComponent(validator)
        self._components.append(component)
        return None
    
    def GetDisplayName(): ...




@dataclass
class RuleBuilder[T,TProperty](IRuleBuilderInitial):
    rule:PropertyRule
    parent_validator:TAbstractValidator

    def __init__(self,rule:IValidationRuleInternal[T,TProperty], parent:TAbstractValidator):
        self.rule = rule
        self.parent_validator = parent

    def SetValidator(self,validator:IPropertyValidator[T,TProperty])->IRuleBuilderOptions[T,TProperty]:
        self.rule.AddValidator(validator)
        return self
    

    def Matches(self,pattern:str)->IRuleBuilderInitial[T,str]:
        return self.SetValidator(RegularExpressionValidator(pattern))


        

class AbstractValidator[T](ABC):
    def __init__(self) -> None:
        self._rules:list[PropertyRule] = []

    def validate(self, instance:T)->ValidationResult:
        return self.internal_validate(ValidationContext(instance))


    def internal_validate(self, context:ValidationContext):
        result:ValidationResult = ValidationResult(None,context.Failures)

        for rules in self._rules:
            rules.Func(rules.PropertyName)
            raise KeyError(f"El tipo de dato '{prop_name}' no se encuentra en la clase {context.InstanceToValidate}")
            
            value = getattr(context.InstanceToValidate,  prop_name)
            if not func(value):
                
                errors[prop_name] = f"Invalid value for {prop_name}" if not msg else msg



    def RuleFor[TProperty](self,func:Callable[[T],TProperty]): #IRuleBuilderInitial[T,TProperty]:
        rule:PropertyRule[T,TProperty] = PropertyRule.create(func)
        self._rules.append(rule)
        return RuleBuilder(rule,self)




class RegexPattern(Enum):
    Email = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+$"
    PhoneNumber = "^\d{9}$"
    PostalCode = "^\d{5}$"
    Dni = "^[0-9]{8}[A-Z]$"







if __name__ == "__main__":
    @dataclass
    class Person():
        name:str
        dni:str
        email:str
        person_id:int =None


    class PersonValidator(AbstractValidator[Person]):
        def __init__(self) -> None:
            super().__init__()
            self.RuleFor()
            self.RuleFor(lambda x: x.dni).Matches(r"^51527736PP$")


    person = Person(name="Pablo",dni="51527736P",email="p.hzamora@alumnos.upm.es")

    validator = PersonValidator()
    result = validator.validate(person)
    result.is_valid