from abc import ABC
from dataclasses import dataclass

import re
from typing import Any, override
from IValidationContext import ValidationContext

from validators.PropertyValidator import PropertyValidator


class IRegularExpressionValidator():
    _expression:str
    _regex_func:re.Pattern

@dataclass
class RegularExpressionValidator[T](PropertyValidator[T,str],IRegularExpressionValidator): 

    def __init__(self,expression:str|re.Pattern, options:re.RegexFlag=None):
        if isinstance(expression,str):
            self.__init__exp_str(expression)
        elif isinstance(expression,re.Pattern) and options is not None:
            self.__init__exp_re_pattern(expression)
        elif isinstance(expression,re.Pattern) and options is None:
            self.__init__exp_re_pattern_options(expression,options)


    def __init__exp_str(self,expression:str):
        self._expression = expression
        self._regex_func = re.compile(expression)

    def __init__exp_re_pattern(self,expression:re.Pattern):
        self._regex_func = expression

    def __init__exp_re_pattern_options(self,expression:str,options:re.RegexFlag):
        self._expression = expression
        self._regex_func = re.compile(expression,options)

    @property
    def Name(self): return self.__class__.__name__

    @override
    def is_valid(self,context: ValidationContext[T], value: str):
        if value is None:
            return True
        
        regex:re.Pattern= self._regex_func(context.instance_to_validate)

        if not regex.match(value):
            return False
        return True 
    
    @override
    def get_default_message_template(self, error_code:str):
        return f"RegularExpreesion {self.Name} failed"