import re

class Email:

    def __init__(self, email: str) -> None:
        self.__email = email
        self.__validate()
    
    @property
    def email(self) -> str:
        return self.__email
    
    def __str__(self) -> str:
        return self.__email
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Email):
            return self.__email == other.email
        if isinstance(other, str):
            return self.__email == other
        return False
    
    def __repr__(self) -> str:
        return self.__email

    def __valid_email_format(self) -> None:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, self.__email):
            raise ValueError(f"Email '{self.__email}' is invalid.")
    
    def __valid_email_contains_empty_space(self) -> None:
        if " " in self.__email:
            raise ValueError(f"Email '{self.__email}' is invalid.")

    def __valid_email_contains_double_dot(self) -> None:
        if ".." in self.__email:
            raise ValueError(f"Email '{self.__email}' is invalid.")

    def __validate(self) -> None:
        self.__valid_email_format()
        self.__valid_email_contains_empty_space()
        self.__valid_email_contains_double_dot()