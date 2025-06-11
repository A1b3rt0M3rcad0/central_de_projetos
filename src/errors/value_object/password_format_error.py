from src.errors.value_object.__base.base_value_object_error import BaseValueObjectError

class PasswordFormatError(BaseValueObjectError):

    def __init__(self, message, *args, **kwargs):
        super().__init__(
            title=self.__class__.__name__,
            message=message,
            *args,
            **kwargs
        )