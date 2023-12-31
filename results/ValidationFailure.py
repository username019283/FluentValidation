
class ValidationFailure:

    def __init__(self
        ,PropertyName:str = None
        ,ErrorMessage:str = None
        ,AttemptedValue:object = None
        ,ErrorCode:str = None
        ):
        

        self._PropertyName:str = PropertyName
        self._ErrorMessage:str = ErrorMessage
        self._AttemptedValue:object = AttemptedValue

        self._CustomState:object = None
        self._ErrorCode:str = ErrorCode
        self._FormattedMessagePlaceholderValues:dict[str,object] = None

    @property
    def PropertyName(self)->str: return self._PropertyName
    @property
    def ErrorMessage(self)->str: return self._ErrorMessage
    @property
    def AttemptedValue(self)->object: return self._AttemptedValue
    @property
    def CustomState(self)->object: return self._CustomState
    @property
    def ErrorCode(self)->str: return self._ErrorCode
    
    @property
    def FormattedMessagePlaceholderValues(self)->dict[str,object]: return self._FormattedMessagePlaceholderValues





    def __str__(self) -> str:
        return self._ErrorMessage

