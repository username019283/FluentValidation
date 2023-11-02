from typing import override
from IValidationContext import ValidationContext
from validators.PropertyValidator import PropertyValidator


class NotNullValidator[T,TProperty](PropertyValidator):



    def is_valid(self, _: ValidationContext, value: TProperty) -> bool:
        return value is None
    
    @override
    def get_default_message_template(self, error_code: str) -> str:
        return f"El elemento no paso el validador {self.__class__.__name__}" 