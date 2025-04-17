class Password:

    def __init__(self, password:str):
        self.__password = password
        self.__validate()
    
    @property
    def password(self) -> str:
        return self.__password
    
    def __str__(self) -> str:
        return self.__password
    
    def __repr__(self) -> str:
        return f'Password({self.__password})'

    def __eq__(self, other) -> bool:
        if isinstance(other, Password):
            return self.__password == other.password
        if isinstance(other, str):
            return self.__password == other
        return False
    
    def __valid_password_length(self) -> None:
        if len(self.__password) < 8:
            raise ValueError('Password length must be at least 8 characters')

    def __valid_password_contains_uppercase(self) -> None:
        if not any(char.isupper() for char in self.__password):
            raise ValueError('Password must contain at least one uppercase letter')
    
    def __valid_password_contains_lowercase(self) -> None:
        if not any(char.islower() for char in self.__password):
            raise ValueError('Password must contain at least one lowercase letter')
    
    def __valid_password_contains_digit(self) -> None:
        if not any(char.isdigit() for char in self.__password):
            raise ValueError('Password must contain at least one digit')
    
    def __valid_password_contains_empty_space(self) -> None:
        if ' ' in self.__password:
            raise ValueError('Password must not contain empty spaces')

    def __validate(self) -> None:
        self.__valid_password_length()
        self.__valid_password_contains_uppercase()
        self.__valid_password_contains_lowercase()
        self.__valid_password_contains_digit()
        self.__valid_password_contains_empty_space()