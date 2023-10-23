
class ValidationFailure:

    def __init__(self
        ,PropertyName:str = None
        ,ErrorMessage:str = None
        ,AttemptedValue:object = None
        ):
        

        self._PropertyName:str = PropertyName,
        self._ErrorMessage:str = ErrorMessage,
        self._AttemptedValue:object = AttemptedValue
        
        self._CustomState:object = None
        self._ErrorCode:str = None
        self._FormattedMessagePlaceholderValues:dict[str,object] = None

    def __str__(self) -> str:
        return self._ErrorMessage

