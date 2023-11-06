from typing import override
from IValidationContext import ValidationContext
from validators.PropertyValidator import PropertyValidator


class NotNullValidator[T,TProperty](PropertyValidator):

    def is_valid(self, _: ValidationContext, value: TProperty) -> bool:
        return value is not None
    