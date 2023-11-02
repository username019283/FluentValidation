from abc import abstractmethod, ABC
from typing import Self, TypeVar

from validators.IpropertyValidator import IPropertyValidator
from validators.LengthValidator import *

TIRuleBuilder = TypeVar("TIRuleBuilder",bound="IRuleBuilder")


from validators.NotNullValidator import NotNullValidator
from validators.RegularExpressionValidator import RegularExpressionValidator


class DefaultValidatorExtensions:
	"""
	ruleBuilder actua como self, ya que es la instancia padre que se le pasa a traves de la herencia
	"""
	def NotNull[T, TProperty](ruleBuilder:TIRuleBuilder)->TIRuleBuilder:
		return ruleBuilder.SetValidator(NotNullValidator[T,TProperty]())

	def Matches[T](ruleBuilder:TIRuleBuilder, pattern:str)->TIRuleBuilder:
		return ruleBuilder.SetValidator(RegularExpressionValidator[T](pattern))

	def Length[T](ruleBuilder:TIRuleBuilder, min:int,max:int)->TIRuleBuilder:
		return ruleBuilder.SetValidator(LengthValidator[T](min,max))

	def ExactLength[T](ruleBuilder:TIRuleBuilder, exactLength:int)->TIRuleBuilder:
		return ruleBuilder.SetValidator(ExactLengthValidator[T](exactLength))

	def MaxLength[T](ruleBuilder:TIRuleBuilder, MaxLength:int)->TIRuleBuilder:
		return ruleBuilder.SetValidator(MaximumLengthValidator[T](MaxLength))

	def MinLength[T](ruleBuilder:TIRuleBuilder, MinLength:int)->TIRuleBuilder:
		return ruleBuilder.SetValidator(MinimumLengthValidator[T](MinLength))








class IRuleBuilder[T, TProperty] (ABC, DefaultValidatorExtensions): 
    @abstractmethod
    def SetValidator(validator: IPropertyValidator[T, TProperty])->Self: ...



class IRuleBuilderOptions[T,TProperty](IRuleBuilder[T, TProperty]):
    @abstractmethod
    def DependentRules(action)->Self: ...

