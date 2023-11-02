from abc import ABC
from typing import Any, Callable, List, TypeVar
import dis


from dataclasses import dataclass
from internal.MessageBuilderContext import MessageBuilderContext
from internal.RuleComponent import RuleComponent
from results.ValidationFailure import ValidationFailure


from validators.IpropertyValidator import IPropertyValidator
from results.ValidationResult import ValidationResult
from IValidationContext import ValidationContext
from IValidationRule import *
from syntax import *




TAbstractValidator = TypeVar("TAbstractValidator",bound="AbstractValidator")
TRuleBuilder = TypeVar("TRuleBuilder",bound="RuleBuilder")
TPropertyRule = TypeVar("TPropertyRule",bound="PropertyRule")

T = TypeVar("T")



class RuleBase[T,TProperty,TValue](IValidationRule[T,TValue]):
    def __init__(self,propertyFunc:Callable[[T],TProperty],type_to_validate:type):
        self._PropertyFunc = propertyFunc
        self._type_to_validate = type_to_validate
        
        self._components:List[RuleComponent[T, TProperty]] = []
        self._propertyName:str = {x.opname:x.argval for x in dis.Bytecode(propertyFunc)}["LOAD_ATTR"]
        self._displayName:str = self._propertyName

    @property
    def PropertyFunc(self): return self._PropertyFunc
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

    @property
    def MessageBuilder(self)-> Callable[[IMessageBuilderContext[T,TProperty]],str]: None


    @staticmethod
    def PrepareMessageFormatterForValidationError(context:ValidationContext[T], value:TValue)->None:
        # context.MessageFormatter.AppendPropertyName(context.DisplayName)
        context.MessageFormatter.AppendPropertyValue(value)
        # context.MessageFormatter.AppendArgument("PropertyPath", context.PropertyPath)



    def CreateValidationError(self, context:ValidationContext[T], value:TValue, component:RuleComponent[T, TValue])->ValidationFailure: 
        if self.MessageBuilder is not None:
            error =self.MessageBuilder(MessageBuilderContext[T,TProperty](context,value,component))
        else:
            error = component.GetErrorMessage(context,value)

        failure = ValidationFailure("context.PropertyPath por que no esta implmementado", error, value)

        # failure.FormattedMessagePlaceholderValues = context.MessageFormatter.PlaceholderValues
        failure._ErrorCode = component.ErrorCode # ?? ValidatorOptions.Global.ErrorCodeResolver(component.Validator);

        return failure



class PropertyRule[T,TProperty](RuleBase[T,TProperty,TProperty]):
    def __init__(self,func:Callable[[T],TProperty],type_to_validate:type):
        super().__init__(func,type_to_validate)

    @classmethod
    def create(cls, func:Callable[[T],TProperty]):
        return PropertyRule(func,type(TProperty))

    def AddValidator(self,validator:IPropertyValidator[T,TProperty])->None:
        component:RuleComponent = RuleComponent[T,TProperty](validator)
        self._components.append(component)
        return None
    
    def GetDisplayName(): ...


    def ValidateAsync(self, context:ValidationContext[T]):
        first = True
        for component in self.Components:
            context.MessageFormatter.Reset()
            if first:
                first = False
                propValue= self.PropertyFunc(context.instance_to_validate)

            # context.InitializeForPropertyValidator(context._PropertyName)
            valid:bool = component.ValidateAsync(context,propValue)
            if not valid:
                # super().PrepareMessageFormatterForValidationError(context,propValue)
                failure = self.CreateValidationError(context,propValue,component)
                context.Failures.append(failure)
        return
    

class RuleBuilder[T,TProperty](IRuleBuilder): # no implemento IRuleBuilderOptions por que el metodo no se que hace

    def __init__(self,rule:IValidationRuleInternal[T,TProperty], parent:TAbstractValidator):
        self.rule = rule
        self.parent_validator = parent

    def SetValidator(self,validator:IPropertyValidator[T,TProperty])->IRuleBuilder[T,TProperty]: # -> IRuleBuilderOptions[T,TProperty]
        self.rule.AddValidator(validator)
        return self
    

        

class AbstractValidator[T](ABC):
    def __init__(self) -> None:
        self._rules:list[PropertyRule] = []

    def validate(self, instance:T)->ValidationResult:
        return self.internal_validate(ValidationContext(instance))


    def internal_validate(self, context:ValidationContext)->ValidationResult:
        result:ValidationResult = ValidationResult(None,context.Failures)
        for rule in self._rules:
            rule.ValidateAsync(context)

        self.SetExecutedRuleSets(result,context)
        return result

    def RuleFor[TProperty](self,func:Callable[[T],TProperty])->IRuleBuilder[T,TProperty]: #IRuleBuilderInitial[T,TProperty]:
        rule:PropertyRule[T,TProperty] = PropertyRule.create(func)
        self._rules.append(rule)
        return RuleBuilder(rule,self)

    def SetExecutedRuleSets(result:ValidationResult, context:ValidationContext[T]):...
        # result.RuleSetExecuted = RulesetValidatorSelector.DefaultRuleSetNameInArray


# class RegexPattern(Enum):
#     Email = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+$"
#     PhoneNumber = "^\d{9}$"
#     PostalCode = "^\d{5}$"
#     Dni = "^[0-9]{8}[A-Z]$"







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
            self.RuleFor(lambda x: x.dni).NotNull().Matches("asdf").ExactLength(10).Length(5,15)


    person = Person(name="Pablo",dni="51527736P",email="p.hzamora@alumnos.upm.es")

    validator = PersonValidator()
    result = validator.validate(person)
    result.is_valid