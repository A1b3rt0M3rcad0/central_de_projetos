#pylint:disable=C0103
from enum import Enum

class Role:
    class __Roles__(Enum):
        ASSESSOR = "ASSESSOR"
        VEREADOR = "VEREADOR"
        ADMIN = "ADMIN"

    def __init__(self, role: str) -> None:
        self.__role = role.upper()
        self.__validate_role()
    
    @property
    def role(self) -> __Roles__:
        return self.get_roles()[self.__role]

    @classmethod
    def get_roles(cls) -> __Roles__:
        return cls.__Roles__

    def __str__(self) -> str:
        return self.__role
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Role):
            return self.role.value == other.role.value
        if isinstance(other, str):
            return self.role.value == other.upper()
        return False

    def __validate_role(self) -> None:
        if self.__role not in self.__Roles__.__members__:
            raise ValueError(f"Invalid role: {self.__role}")